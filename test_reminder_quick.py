import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from src.core.scheduler import PersonalScheduleAssistant
from datetime import datetime

assistant = PersonalScheduleAssistant()

test_cases = [
    # Test AM/PM conversion
    ("Họp 6h tối hôm nay", "Should be 18:00 today"),
    ("Meeting 8h tối mai", "Should be 20:00 tomorrow"),
    ("Gặp team 2h chiều", "Should be 14:00"),
    ("Training 9h sáng", "Should be 09:00"),
    ("Họp 11h trưa", "Should be 11:00"),
    
    # Test "hôm nay" 
    ("Họp 15h hôm nay", "Should be 15:00 TODAY, not tomorrow"),
    ("Meeting 10h sáng hôm nay", "Should be 10:00 TODAY"),
    ("Gặp 14h chiều nay", "Should be 14:00 TODAY"),
    
    # Test without "hôm nay" - should auto +1 if past
    ("Họp 9h sáng", "Auto +1 day if past 9am"),
    ("Meeting 14h", "Auto +1 day if past 2pm"),
]

print("=" * 80)
print("🧪 TIME PARSING TEST")
print("=" * 80)
print(f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

for i, (text, expected) in enumerate(test_cases, 1):
    print(f"[Test {i}] {text}")
    print(f"Expected: {expected}")
    
    result = assistant.process(text)
    
    if result['success']:
        schedule = result['schedule']
        start_time = schedule['start_time']
        
        # Parse and display
        dt = datetime.fromisoformat(start_time)
        print(f"✅ Result: {dt.strftime('%Y-%m-%d %H:%M')} ({dt.strftime('%A')})")
        
        # Check period
        debug = result.get('debug_info', {})
        time_comp = debug.get('rule_result', {}).get('time_components', {})
        print(f"   Extracted: hour={time_comp.get('hour')}, period={time_comp.get('period')}")
    else:
        print(f"❌ Failed: {result['errors']}")
    
    print()

print("=" * 80)