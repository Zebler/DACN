import sys
import os

# Fix import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.nlp.preprocessor import Preprocessor
from src.nlp.ner_extractor import NERExtractor
from src.nlp.rule_extractor import RuleExtractor
from src.core.parser import TimeParser
from src.core.validator import ScheduleValidator


class PersonalScheduleAssistant:
    """
    Main class kết hợp tất cả 5 components
    Pipeline: Input → Preprocessor → NER → Rule → Parser → Validator → Output
    """
    
    def __init__(self):
        # Khởi tạo tất cả components
        self.preprocessor = Preprocessor()
        self.ner_extractor = NERExtractor()
        self.rule_extractor = RuleExtractor()
        self.time_parser = TimeParser()
        self.validator = ScheduleValidator()
    
    def calculate_confidence(self, schedule, debug_info):
        """
        Tính confidence score đơn giản
        
        Returns:
            tuple: (confidence_score, quality_level)
        """
        score = 0
        
        # Has specific time
        time_comp = debug_info.get('rule_result', {}).get('time_components', {})
        if time_comp.get('hour') is not None:
            score += 30
        if time_comp.get('minute') is not None:
            score += 10
        
        # Has date/day
        if time_comp.get('date') or time_comp.get('weekday') or time_comp.get('relative_day'):
            score += 20
        
        # Has location
        if schedule.get('location', '').strip():
            score += 15
        
        # Has clear event
        if schedule.get('event', '').strip() and len(schedule['event']) > 3:
            score += 15
        
        # Has valid start_time
        if schedule.get('start_time'):
            score += 10
        
        # Quality level
        if score >= 80:
            quality = 'excellent'
        elif score >= 60:
            quality = 'good'
        elif score >= 40:
            quality = 'fair'
        else:
            quality = 'poor'
        
        return score, quality
    
    def process(self, text):
        """
        Xử lý câu tiếng Việt tự nhiên thành schedule object
        
        Args:
            text (str): Câu tiếng Việt (VD: "Họp nhóm 10 giờ sáng mai ở phòng 302")
            
        Returns:
            dict: {
                'success': bool,
                'schedule': dict hoặc None,
                'errors': list,
                'confidence': float,
                'quality': str,
                'debug_info': dict (optional)
            }
        """
        try:
            # Component 1: Preprocessing
            preprocessed = self.preprocessor.process(text)
            normalized_text = preprocessed['normalized']
            
            # Component 2: NER Extraction
            ner_result = self.ner_extractor.extract(normalized_text)
            
            # Component 3: Rule-based Extraction
            rule_result = self.rule_extractor.extract_all(normalized_text)
            
            # Component 4: Time Parsing
            time_components = rule_result.get('time_components', {})
            parsed_time = self.time_parser.parse(time_components)
            
            # Component 5: Validation & Merging
            schedule, is_valid, errors = self.validator.create_schedule(
                preprocessed, ner_result, rule_result, parsed_time
            )
            
            # Calculate confidence
            debug_info = {
                'preprocessed': preprocessed,
                'ner_result': ner_result,
                'rule_result': rule_result,
                'parsed_time': parsed_time
            }
            confidence, quality = self.calculate_confidence(schedule, debug_info)
            
            # Return result
            return {
                'success': is_valid,
                'schedule': schedule if is_valid else None,
                'errors': errors,
                'confidence': confidence,
                'quality': quality,
                'debug_info': debug_info
            }
        
        except Exception as e:
            return {
                'success': False,
                'schedule': None,
                'errors': [f"Lỗi xử lý: {str(e)}"],
                'confidence': 0,
                'quality': 'poor',
                'debug_info': None
            }
    
    def process_batch(self, texts):
        """
        Xử lý nhiều câu cùng lúc
        
        Args:
            texts (list): Danh sách các câu
            
        Returns:
            list: Danh sách kết quả
        """
        results = []
        for text in texts:
            result = self.process(text)
            results.append(result)
        return results


# Test code
if __name__ == "__main__":
    assistant = PersonalScheduleAssistant()
    
    test_cases = [
        "Họp nhóm 10 giờ sáng mai ở phòng 302, nhắc trước 15 phút",
        "Meeting khách hàng 14:30 chiều nay tại tầng 5 tòa A",
        "Gặp team 9h thứ 2 tuần sau văn phòng B",
        "Họp 10:00 sáng 01/12/2025 hội trường",
        "Training chiều mai",
    ]
    
    print("=" * 80)
    print("TEST FULL PIPELINE - PERSONAL SCHEDULE ASSISTANT")
    print("=" * 80)
    
    for i, text in enumerate(test_cases, 1):
        print(f"\n{'='*80}")
        print(f"[Test {i}] Input: {text}")
        print('='*80)
        
        result = assistant.process(text)
        
        if result['success']:
            print("✅ SUCCESS")
            schedule = result['schedule']
            print(f"\n📅 Schedule Output:")
            print(f"   Event:            {schedule['event']}")
            print(f"   Start Time:       {schedule['start_time']}")
            print(f"   End Time:         {schedule['end_time']}")
            print(f"   Location:         {schedule['location']}")
            print(f"   Reminder (mins):  {schedule['reminder_minutes']}")
        else:
            print("❌ FAILED")
            print(f"Errors: {result['errors']}")
        
        # Debug info
        if result.get('debug_info'):
            print(f"\n🔍 Debug Info:")
            debug = result['debug_info']
            print(f"   Normalized:  {debug['preprocessed']['normalized']}")
            print(f"   NER Location: {debug['ner_result'].get('location', [])}")
            print(f"   Parsed Time: {debug['parsed_time']}")
    
    print("\n" + "=" * 80)
    print("✅ ALL TESTS COMPLETED!")
    print("=" * 80)