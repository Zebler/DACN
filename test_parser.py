import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from src.nlp.preprocessor import Preprocessor
from src.nlp.rule_extractor import RuleExtractor
from src.core.parser import TimeParser

def debug_case(text):
    """Debug một test case cụ thể"""
    print("\n" + "="*80)
    print(f"DEBUG: {text}")
    print("="*80)
    
    # Step 1: Preprocess
    preprocessor = Preprocessor()
    preprocessed = preprocessor.process(text)
    normalized = preprocessed['normalized']
    print(f"\n1. Normalized: {normalized}")
    
    # Step 2: Extract
    extractor = RuleExtractor()
    rule_result = extractor.extract_all(normalized)
    time_components = rule_result['time_components']
    
    print(f"\n2. Time Components:")
    for key, value in time_components.items():
        if value and key != 'raw_matches':
            print(f"   {key}: {value}")
    
    # Step 3: Parse
    parser = TimeParser()
    
    # Debug internal steps
    print(f"\n3. Parser Internal Steps:")
    base_date = parser.current_time.replace(hour=0, minute=0, second=0, microsecond=0)
    print(f"   Base date: {base_date}")
    
    # Parse date
    target_date = parser._parse_date(time_components, base_date)
    print(f"   Target date: {target_date}")
    
    # Parse time
    hour, minute = parser._parse_time(time_components)
    print(f"   Hour: {hour}, Minute: {minute}")
    
    # Final result
    result = parser.parse(time_components)
    print(f"\n4. Final Result: {result}")
    
    if result is None:
        print("   ❌ FAILED: Parser returned None")
        print("   Possible reasons:")
        if hour is None:
            print("   - Hour is None (no time extracted)")
        if target_date is None:
            print("   - Target date is None")
    else:
        print("   ✅ SUCCESS")


# Test failed cases
failed_cases = [
    "Họp nhóm 10 giờ sáng mai ở phòng 302",
    "Gặp team 9h thứ 2 tuần sau",
    "Training chiều mai phòng 101",
    "Họp sếp 15h tòa B",
    "Seminar 9 giờ sáng thứ 6",
]

for text in failed_cases:
    debug_case(text)