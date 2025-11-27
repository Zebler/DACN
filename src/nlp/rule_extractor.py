import re
import sys
import os

# Fix import path
try:
    from .patterns import (
        TIME_PATTERNS, LOCATION_PATTERNS, EVENT_PATTERNS,
        REMINDER_PATTERNS, WEEKDAY_MAP, PERIOD_HOUR_MAP
    )
except ImportError:
    # Nếu chạy trực tiếp file này
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
    from src.nlp.patterns import (
        TIME_PATTERNS, LOCATION_PATTERNS, EVENT_PATTERNS,
        REMINDER_PATTERNS, WEEKDAY_MAP, PERIOD_HOUR_MAP
    )


class RuleExtractor:
    """Trích xuất thông tin bằng rule-based (regex)"""
    
    def __init__(self):
        self.time_patterns = TIME_PATTERNS
        self.location_patterns = LOCATION_PATTERNS
        self.event_patterns = EVENT_PATTERNS
        self.reminder_patterns = REMINDER_PATTERNS
    
    def extract_event(self, text):
        """
        Trích xuất tên sự kiện (IMPROVED)
        
        Args:
            text (str): Văn bản đầu vào
            
        Returns:
            str: Tên sự kiện
        """
        # Tìm động từ sự kiện
        action_pattern = self.event_patterns['action_verb']
        object_pattern = self.event_patterns['object']
        
        action_match = re.search(action_pattern, text, re.IGNORECASE)
        object_match = re.search(object_pattern, text, re.IGNORECASE)
        
        # Strategy 1: Có cả action và object
        if action_match and object_match:
            # Lấy cả context xung quanh
            start = min(action_match.start(), object_match.start())
            end = max(action_match.end(), object_match.end())
            event_context = text[start:end]
            return event_context.strip()
        
        # Strategy 2: Chỉ có action
        elif action_match:
            # Lấy 3-5 từ sau action
            start = action_match.start()
            end = min(action_match.end() + 30, len(text))
            event_context = text[start:end]
            # Cắt ở dấu phẩy hoặc "tại", "ở"
            for marker in [',', ' tại ', ' ở ', ' lúc ', ' vào ']:
                if marker in event_context:
                    event_context = event_context.split(marker)[0]
                    break
            return event_context.strip()
        
        # Strategy 3: Không có pattern -> lấy phần đầu câu
        else:
            # Lấy 5-7 từ đầu tiên (trước dấu phẩy hoặc marker)
            words = text.split()
            event_words = []
            for word in words[:7]:
                if word in [',', 'tại', 'ở', 'lúc', 'vào']:
                    break
                event_words.append(word)
            return ' '.join(event_words) if event_words else text[:50]
    
    def extract_time_components(self, text):
        """
        Trích xuất các thành phần thời gian (IMPROVED)
        
        Returns:
            dict: {
                'hour': int hoặc None,
                'minute': int hoặc None,
                'period': str hoặc None (sáng/chiều/tối),
                'weekday': str hoặc None,
                'relative_day': str hoặc None,
                'date': str hoặc None
            }
        """
        result = {
            'hour': None,
            'minute': None,
            'period': None,
            'weekday': None,
            'relative_day': None,
            'date': None,
            'raw_matches': []
        }
        
        # Extract hour:minute - TRY ALL PATTERNS
        for pattern in self.time_patterns['hour_minute']:
            match = re.search(pattern, text)
            if match:
                groups = match.groups()
                result['raw_matches'].append(match.group())
                
                # Parse based on pattern
                if len(groups) >= 1 and groups[0]:
                    try:
                        result['hour'] = int(groups[0])
                    except (ValueError, TypeError):
                        pass
                
                if len(groups) >= 2 and groups[1]:
                    try:
                        result['minute'] = int(groups[1])
                    except (ValueError, TypeError):
                        result['minute'] = 0
                
                # If found, break
                if result['hour'] is not None:
                    break
        
        # Special case: "giờ rưỡi" -> :30
        if 'rưỡi' in text and result['hour'] is not None:
            result['minute'] = 30
        
        # Extract period (sáng/chiều/tối)
        period_match = re.search(self.time_patterns['period'], text)
        if period_match:
            result['period'] = period_match.group()
        
        # Extract relative day
        relative_match = re.search(self.time_patterns['relative_day'], text)
        if relative_match:
            result['relative_day'] = relative_match.group()
        
        # Extract weekday
        weekday_match = re.search(self.time_patterns['weekday'], text)
        if weekday_match:
            result['weekday'] = weekday_match.group()
        
        # Extract date
        date_match = re.search(self.time_patterns['date'], text)
        if date_match:
            result['date'] = date_match.group()
        
        return result
    
    def extract_location_components(self, text):
        """
        Trích xuất các thành phần địa điểm
        
        Returns:
            dict: {
                'room': str hoặc None,
                'floor': str hoặc None,
                'building': str hoặc None,
                'office': str hoặc None,
                'full_location': str
            }
        """
        result = {
            'room': None,
            'floor': None,
            'building': None,
            'office': None,
            'full_location': '',
            'raw_matches': []
        }
        
        # Extract room
        room_match = re.search(self.location_patterns['room'], text)
        if room_match:
            result['room'] = room_match.group()
            result['raw_matches'].append(room_match.group())
        
        # Extract floor
        floor_match = re.search(self.location_patterns['floor'], text)
        if floor_match:
            result['floor'] = floor_match.group()
            result['raw_matches'].append(floor_match.group())
        
        # Extract building
        building_match = re.search(self.location_patterns['building'], text)
        if building_match:
            result['building'] = building_match.group()
            result['raw_matches'].append(building_match.group())
        
        # Extract office
        office_match = re.search(self.location_patterns['office'], text)
        if office_match:
            result['office'] = office_match.group()
            result['raw_matches'].append(office_match.group())
        
        # Combine full location
        location_parts = [v for v in [result['room'], result['floor'], 
                                      result['building'], result['office']] if v]
        result['full_location'] = ', '.join(location_parts)
        
        return result
    
    def extract_reminder(self, text):
        """
        Trích xuất thời gian nhắc nhở
        
        Returns:
            int: Số phút nhắc trước (mặc định 15)
        """
        remind_match = re.search(self.reminder_patterns['remind_before'], text)
        
        if remind_match:
            groups = remind_match.groups()
            if len(groups) >= 2:
                minutes = int(groups[1])
                unit = groups[2] if len(groups) >= 3 else 'phút'
                
                if unit == 'giờ':
                    return minutes * 60
                return minutes
        
        # Mặc định
        return self.reminder_patterns['default_minutes']
    
    def extract_all(self, text):
        """
        Pipeline chính: Trích xuất tất cả thông tin
        
        Args:
            text (str): Văn bản đầu vào
            
        Returns:
            dict: Tất cả thông tin đã trích xuất
        """
        return {
            'event': self.extract_event(text),
            'time_components': self.extract_time_components(text),
            'location_components': self.extract_location_components(text),
            'reminder_minutes': self.extract_reminder(text)
        }


# Test code
if __name__ == "__main__":
    extractor = RuleExtractor()
    
    test_cases = [
        "Họp nhóm 10 giờ sáng mai ở phòng 302, nhắc trước 15 phút",
        "Meeting khách hàng 14:30 chiều nay tại tầng 5 tòa A",
        "Gặp team 9h thứ 2 tuần sau văn phòng B",
        "Họp 10:00 sáng 01/12/2025 hội trường",
    ]
    
    print("=" * 60)
    print("TEST COMPONENT 3: RULE-BASED EXTRACTOR")
    print("=" * 60)
    
    for i, text in enumerate(test_cases, 1):
        print(f"\n[Test {i}] Input: {text}")
        result = extractor.extract_all(text)
        
        print(f"Event: {result['event']}")
        print(f"Time Components:")
        for key, value in result['time_components'].items():
            if value and key != 'raw_matches':
                print(f"  - {key}: {value}")
        
        print(f"Location Components:")
        loc = result['location_components']
        if loc['full_location']:
            print(f"  - Full: {loc['full_location']}")
        
        print(f"Reminder: {result['reminder_minutes']} phút")