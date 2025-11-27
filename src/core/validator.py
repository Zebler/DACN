from datetime import datetime
import sys
import os

# Fix import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.utils.time_utils import get_current_datetime


class ScheduleValidator:
    """Validate và hợp nhất kết quả từ các components"""
    
    def __init__(self):
        self.required_fields = ['event', 'start_time']
        self.optional_fields = ['end_time', 'location', 'reminder_minutes']
    
    def validate_event(self, event):
        """
        Kiểm tra event hợp lệ
        
        Args:
            event (str): Tên sự kiện
            
        Returns:
            tuple: (is_valid, error_message)
        """
        if not event or not event.strip():
            return False, "Event không được để trống"
        
        if len(event) > 200:
            return False, "Event quá dài (tối đa 200 ký tự)"
        
        return True, None
    
    def validate_start_time(self, start_time):
        """
        Kiểm tra start_time hợp lệ
        
        Args:
            start_time (str): ISO format datetime string
            
        Returns:
            tuple: (is_valid, error_message)
        """
        if not start_time:
            return False, "Start time không được để trống"
        
        try:
            # Parse ISO format
            dt = datetime.fromisoformat(start_time)
            
            # Kiểm tra không được là thời điểm quá khứ (trừ trong hôm nay)
            from src.utils.time_utils import get_current_datetime
            current = get_current_datetime()
            
            # Make both timezone-aware or both naive for comparison
            if dt.tzinfo is None and current.tzinfo is not None:
                from src.utils.time_utils import VN_TZ
                dt = VN_TZ.localize(dt)
            elif dt.tzinfo is not None and current.tzinfo is None:
                current = current.replace(tzinfo=dt.tzinfo)
            
            # Start of current day
            current_start = current.replace(hour=0, minute=0, second=0, microsecond=0)
            
            if dt < current_start:
                return False, "Start time không được là quá khứ"
            
            return True, None
        
        except ValueError as e:
            return False, f"Start time format không hợp lệ: {e}"
    
    def validate_location(self, location):
        """
        Kiểm tra location hợp lệ
        
        Args:
            location (str): Địa điểm
            
        Returns:
            tuple: (is_valid, error_message)
        """
        if location and len(location) > 200:
            return False, "Location quá dài (tối đa 200 ký tự)"
        
        return True, None
    
    def validate_reminder_minutes(self, reminder_minutes):
        """
        Kiểm tra reminder_minutes hợp lệ
        
        Args:
            reminder_minutes (int): Số phút nhắc trước
            
        Returns:
            tuple: (is_valid, error_message)
        """
        if reminder_minutes is None:
            return True, None  # Optional field
        
        if not isinstance(reminder_minutes, int):
            return False, "Reminder minutes phải là số nguyên"
        
        if reminder_minutes < 0:
            return False, "Reminder minutes không được âm"
        
        if reminder_minutes > 1440:  # 24 giờ
            return False, "Reminder minutes không được vượt quá 24 giờ (1440 phút)"
        
        return True, None
    
    def merge_results(self, preprocessed, ner_result, rule_result, parsed_time):
        """
        Hợp nhất kết quả từ tất cả các components
        
        Args:
            preprocessed (dict): Kết quả từ Preprocessor
            ner_result (dict): Kết quả từ NER Extractor
            rule_result (dict): Kết quả từ Rule Extractor
            parsed_time (str): Kết quả từ Time Parser (ISO format)
            
        Returns:
            dict: Schedule object hoàn chỉnh
        """
        # Extract event
        event = rule_result.get('event', preprocessed.get('original', ''))
        
        # Extract location
        location_from_rule = rule_result.get('location_components', {}).get('full_location', '')
        location_from_ner = ', '.join(ner_result.get('location', []))
        location = location_from_rule or location_from_ner or ''
        
        # Extract start_time
        start_time = parsed_time
        
        # Extract reminder
        reminder_minutes = rule_result.get('reminder_minutes', 15)
        
        # Create schedule object
        schedule = {
            'event': event.strip(),
            'start_time': start_time,
            'end_time': None,  # Có thể mở rộng sau
            'location': location.strip(),
            'reminder_minutes': reminder_minutes
        }
        
        return schedule
    
    def validate_schedule(self, schedule):
        """
        Validate toàn bộ schedule object
        
        Args:
            schedule (dict): Schedule object cần validate
            
        Returns:
            tuple: (is_valid, errors)
                is_valid (bool): True nếu hợp lệ
                errors (list): Danh sách lỗi (nếu có)
        """
        errors = []
        
        # Validate event
        is_valid, error = self.validate_event(schedule.get('event'))
        if not is_valid:
            errors.append(error)
        
        # Validate start_time
        is_valid, error = self.validate_start_time(schedule.get('start_time'))
        if not is_valid:
            errors.append(error)
        
        # Validate location
        is_valid, error = self.validate_location(schedule.get('location'))
        if not is_valid:
            errors.append(error)
        
        # Validate reminder_minutes
        is_valid, error = self.validate_reminder_minutes(schedule.get('reminder_minutes'))
        if not is_valid:
            errors.append(error)
        
        return len(errors) == 0, errors
    
    def create_schedule(self, preprocessed, ner_result, rule_result, parsed_time):
        """
        Pipeline chính: Merge + Validate
        
        Returns:
            tuple: (schedule, is_valid, errors)
        """
        # Step 1: Merge
        schedule = self.merge_results(preprocessed, ner_result, rule_result, parsed_time)
        
        # Step 2: Validate
        is_valid, errors = self.validate_schedule(schedule)
        
        return schedule, is_valid, errors


# Test code
if __name__ == "__main__":
    validator = ScheduleValidator()
    
    # Test case 1: Valid schedule
    print("=" * 70)
    print("TEST COMPONENT 5: VALIDATOR")
    print("=" * 70)
    
    test_schedule_valid = {
        'event': 'Họp nhóm',
        'start_time': '2025-12-01T10:00:00',
        'end_time': None,
        'location': 'phòng 302',
        'reminder_minutes': 15
    }
    
    print("\n[Test 1] Valid Schedule")
    print(f"Input: {test_schedule_valid}")
    is_valid, errors = validator.validate_schedule(test_schedule_valid)
    print(f"Valid: {is_valid}")
    print(f"Errors: {errors}")
    
    # Test case 2: Invalid schedule (missing event)
    test_schedule_invalid = {
        'event': '',
        'start_time': '2025-12-01T10:00:00',
        'end_time': None,
        'location': 'phòng 302',
        'reminder_minutes': 15
    }
    
    print("\n[Test 2] Invalid Schedule (empty event)")
    print(f"Input: {test_schedule_invalid}")
    is_valid, errors = validator.validate_schedule(test_schedule_invalid)
    print(f"Valid: {is_valid}")
    print(f"Errors: {errors}")
    
    # Test case 3: Invalid reminder
    test_schedule_invalid2 = {
        'event': 'Họp team',
        'start_time': '2025-12-01T10:00:00',
        'end_time': None,
        'location': 'phòng 302',
        'reminder_minutes': -10
    }
    
    print("\n[Test 3] Invalid Schedule (negative reminder)")
    print(f"Input: {test_schedule_invalid2}")
    is_valid, errors = validator.validate_schedule(test_schedule_invalid2)
    print(f"Valid: {is_valid}")
    print(f"Errors: {errors}")
    
    # Test merge
    print("\n" + "=" * 70)
    print("TEST MERGE FUNCTION")
    print("=" * 70)
    
    mock_preprocessed = {'original': 'Họp nhóm 10 giờ sáng mai ở phòng 302'}
    mock_ner = {'location': ['phòng 302']}
    mock_rule = {
        'event': 'Họp nhóm',
        'location_components': {'full_location': 'phòng 302'},
        'reminder_minutes': 15
    }
    mock_parsed_time = '2025-12-01T10:00:00'
    
    schedule, is_valid, errors = validator.create_schedule(
        mock_preprocessed, mock_ner, mock_rule, mock_parsed_time
    )
    
    print(f"\nMerged Schedule: {schedule}")
    print(f"Valid: {is_valid}")
    print(f"Errors: {errors}")