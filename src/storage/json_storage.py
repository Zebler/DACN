import json
import os
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


# Test
if __name__ == "__main__":
    storage = JSONStorage()
    
    # Test save
    test_schedule = {
        'event': 'Test meeting',
        'start_time': '2025-12-01T10:00:00',
        'location': 'Room 302',
        'reminder_minutes': 15
    }
    
    schedule_id = storage.save(test_schedule)
    print(f"Saved with ID: {schedule_id}")
    
    # Test load
    all_schedules = storage.load_all()
    print(f"Total schedules: {len(all_schedules)}")
    
    # Test search
    results = storage.search('test')
    print(f"Search results: {len(results)}")