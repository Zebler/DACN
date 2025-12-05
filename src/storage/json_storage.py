import json
import os
import sys
from datetime import datetime


class JSONStorage:
    """Quản lý lưu trữ schedule bằng JSON"""
    
    def __init__(self, file_path='data/schedules.json'):
        self.file_path = file_path
        self.ensure_file_exists()
   
    def ensure_file_exists(self):
        """Đảm bảo file tồn tại"""
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=2)

    def _overwrite_internal(self, data):
        """Ghi đè dữ liệu vào file schedules.json nội bộ."""
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def export_to_file(self, data, external_path):
        """
        Xuất dữ liệu schedule ra một file JSON bất kỳ.
        
        Args:
            data (list): Danh sách schedules để xuất.
            external_path (str): Đường dẫn file đích.
        
        Returns:
            tuple: (success: bool, error_message: str hoặc None)
        """
        try:
            with open(external_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True, None
        except Exception as e:
            return False, f"Lỗi khi xuất file: {e}"

    def import_from_file(self, external_path):
        """
        Nhập dữ liệu schedule từ một file JSON bất kỳ và ghi đè nội bộ.
        
        Args:
            external_path (str): Đường dẫn file nguồn.
            
        Returns:
            tuple: (imported_data: list hoặc None, error_message: str hoặc None)
        """
        try:
            with open(external_path, 'r', encoding='utf-8') as f:
                imported_data = json.load(f)
            
            # Kiểm tra định dạng cơ bản
            if not isinstance(imported_data, list):
                return None, "Định dạng file không hợp lệ (File không chứa danh sách lịch trình)"
            
            # Ghi đè dữ liệu vào file gốc (nội bộ)
            self._overwrite_internal(imported_data)
            
            return imported_data, None
        except FileNotFoundError:
            return None, "File không tồn tại."
        except json.JSONDecodeError:
            return None, "Lỗi định dạng JSON: Nội dung file không hợp lệ."
        except Exception as e:
            return None, f"Lỗi khi nhập file: {e}"

    def load_all(self):
        """Load tất cả schedules"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Lỗi load: {e}")
            return []
    
    def save(self, schedule):
        """
        Lưu schedule mới
        
        Args:
            schedule (dict): Schedule object
            
        Returns:
            str: ID của schedule
        """
        schedules = self.load_all()
        
        # Generate ID
        if schedules:
            max_id = max(int(s.get('id', 0)) for s in schedules)
            schedule['id'] = str(max_id + 1)
        else:
            schedule['id'] = '1'
        
        # Add created timestamp
        schedule['created_at'] = datetime.now().isoformat()
        
        # Add to list
        schedules.append(schedule)
        
        # Save
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(schedules, f, ensure_ascii=False, indent=2)
        
        return schedule['id']
    
    def delete(self, schedule_id):
        """Xóa schedule theo ID"""
        schedules = self.load_all()
        schedules = [s for s in schedules if s.get('id') != str(schedule_id)]
        
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(schedules, f, ensure_ascii=False, indent=2)
    
    def update(self, schedule_id, updated_schedule):
        """Cập nhật schedule"""
        schedules = self.load_all()
        
        for i, s in enumerate(schedules):
            if s.get('id') == str(schedule_id):
                updated_schedule['id'] = str(schedule_id)
                updated_schedule['updated_at'] = datetime.now().isoformat()
                schedules[i] = updated_schedule
                break
        
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(schedules, f, ensure_ascii=False, indent=2)
    
    def search(self, keyword):
        """Tìm kiếm schedule"""
        schedules = self.load_all()
        keyword = keyword.lower()
        
        return [
            s for s in schedules
            if keyword in s.get('event', '').lower() or
               keyword in s.get('location', '').lower()
        ]
    def ensure_file_exists(self):
        """Đảm bảo file tồn tại"""
        # Get app data directory
        if getattr(sys, 'frozen', False):
            # Running as exe - use app directory
            app_dir = os.path.dirname(sys.executable)
        else:
            # Running as script
            app_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Create data folder next to exe
        data_dir = os.path.join(app_dir, 'data')
        os.makedirs(data_dir, exist_ok=True)
        
        self.file_path = os.path.join(data_dir, 'schedules.json')
        
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=2)