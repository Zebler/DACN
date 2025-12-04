from datetime import datetime, timedelta
import re
import sys
import os

# Fix import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.utils.time_utils import (
    get_current_datetime,
    get_weekday_offset,
    get_relative_day_offset,
    parse_period_to_hour,
    is_valid_time,
    format_datetime_iso
)


class TimeParser:
    """Parse các thành phần thời gian thành datetime object"""
    
    def __init__(self):
        self.current_time = get_current_datetime()
    
    def parse_time_components(self, time_components):
        """
        Chuyển đổi time_components thành datetime
        
        Args:
            time_components (dict): Output từ RuleExtractor
                {
                    'hour': int,
                    'minute': int,
                    'period': str,
                    'weekday': str,
                    'relative_day': str,
                    'date': str
                }
        
        Returns:
            datetime: Datetime object hoàn chỉnh hoặc None
        """
        # Bắt đầu với ngày hiện tại
        base_date = self.current_time.replace(hour=0, minute=0, second=0, microsecond=0)
        
        # 1. Xử lý ngày (date, weekday, relative_day)
        target_date = self._parse_date(time_components, base_date)
        
        # 2. Xử lý giờ và phút
        hour, minute = self._parse_time(time_components)
        
        # 3. Kết hợp ngày + giờ
        if target_date and hour is not None:
            result = target_date.replace(hour=hour, minute=minute or 0)
            
            # CHỈ tự động +1 ngày khi:
            # - Thời gian đã qua
            # - KHÔNG có date cụ thể
            # - KHÔNG phải "hôm nay" (relative_day != 'hôm nay')
            relative_day = time_components.get('relative_day', '').lower()
            has_explicit_date = time_components.get('date') is not None
            is_today = relative_day in ['hôm nay', 'ngày hôm nay']
            
            if result < self.current_time and not has_explicit_date and not is_today:
                result = result + timedelta(days=1)
            
            return result
        
        return None
    
    def _parse_date(self, time_components, base_date):
        """
        Parse ngày từ các thành phần
        
        Returns:
            datetime: Base date đã điều chỉnh
        """
        # Priority 1: Date cụ thể (01/12, 01/12/2025)
        if time_components.get('date'):
            parsed_date = self._parse_specific_date(time_components['date'])
            if parsed_date:
                return parsed_date
        
        # Priority 2: Weekday (thứ 2, thứ 6) - CHÚ Ý: Phải xử lý trước relative_day
        if time_components.get('weekday'):
            offset = get_weekday_offset(time_components['weekday'])
            result = base_date + timedelta(days=offset)
            
            # Nếu có "tuần sau", cộng thêm 7 ngày
            if time_components.get('relative_day') and 'tuần sau' in str(time_components.get('relative_day')):
                result = result + timedelta(days=7)
            
            return result
        
        # Priority 3: Relative day (mai, tuần sau)
        if time_components.get('relative_day'):
            offset = get_relative_day_offset(time_components['relative_day'])
            return base_date + timedelta(days=offset)
        
        # Default: hôm nay
        return base_date
    
    def _parse_specific_date(self, date_str):
        """
        Parse ngày cụ thể từ string (01/12, 01/12/2025)
        
        Args:
            date_str (str): String ngày
            
        Returns:
            datetime hoặc None
        """
        # Pattern: dd/mm hoặc dd/mm/yyyy
        patterns = [
            (r'(\d{1,2})/(\d{1,2})/(\d{4})', '%d/%m/%Y'),  # 01/12/2025
            (r'(\d{1,2})/(\d{1,2})/(\d{2})', '%d/%m/%y'),  # 01/12/25
            (r'(\d{1,2})/(\d{1,2})', '%d/%m'),  # 01/12
        ]
        
        for pattern, format_str in patterns:
            match = re.match(pattern, date_str)
            if match:
                try:
                    if '%Y' in format_str or '%y' in format_str:
                        result = datetime.strptime(date_str, format_str)
                    else:
                        # Không có năm, dùng năm hiện tại
                        current_year = self.current_time.year
                        date_with_year = f"{date_str}/{current_year}"
                        result = datetime.strptime(date_with_year, '%d/%m/%Y')
                        
                        # Nếu ngày đã qua trong năm, lấy năm sau
                        # Convert to timezone-aware for comparison
                        current_naive = self.current_time.replace(tzinfo=None)
                        if result < current_naive:
                            result = result.replace(year=current_year + 1)
                    
                    # Add timezone info
                    from src.utils.time_utils import VN_TZ
                    result = VN_TZ.localize(result)
                    return result
                except ValueError:
                    continue
        
        return None
    
    def _parse_time(self, time_components):
        """
        Parse giờ và phút (IMPROVED with better AM/PM logic)
        
        Returns:
            tuple: (hour, minute)
        """
        hour = time_components.get('hour')
        minute = time_components.get('minute')
        period = time_components.get('period')
        
        # Set default minute to 0 if None
        if minute is None:
            minute = 0
        
        # Case 1: Có giờ rõ ràng
        if hour is not None:
            # Xử lý AM/PM conversion
            if period:
                period_lower = period.lower()
                
                # CHIỀU/TỐI: Giờ từ 1-11 -> cộng 12
                if period_lower in ['chiều', 'buổi chiều', 'tối', 'buổi tối', 'tối muộn']:
                    if 1 <= hour <= 11:
                        hour += 12
                    # 12h chiều = 12h (noon), không đổi
                    # 13h-23h giữ nguyên
                
                # ĐÊM/KHUYA: Giữ nguyên (0-5h) hoặc convert nếu > 12
                elif period_lower in ['đêm', 'khuya', 'nửa đêm']:
                    if hour >= 12:
                        hour = hour - 12  # 12h đêm = 0h
                    # 0-5h giữ nguyên
                
                # SÁNG: Giữ nguyên 0-11h
                # 12h sáng = 0h (midnight)
                elif period_lower in ['sáng', 'buổi sáng', 'sáng sớm']:
                    if hour == 12:
                        hour = 0
                    # 1-11h giữ nguyên
                
                # TRƯA: 12h hoặc 11-13h
                elif period_lower in ['trưa', 'buổi trưa']:
                    # 12h trưa = 12h (noon)
                    pass
            
            # Validate
            if is_valid_time(hour, minute):
                return hour, minute
        
        # Case 2: Không có giờ nhưng có period
        if hour is None and period:
            hour = parse_period_to_hour(period)
            return hour, 0
        
        # Case 3: Không có gì cả - return None
        return None, None
    
    def parse(self, time_components):
        """
        Public method để parse time components
        
        Args:
            time_components (dict): Time components từ RuleExtractor
            
        Returns:
            str: ISO format datetime string hoặc None
        """
        dt = self.parse_time_components(time_components)
        return format_datetime_iso(dt) if dt else None