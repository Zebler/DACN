import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from src.core.scheduler import PersonalScheduleAssistant
import json


def load_test_cases(file_path='data/test_cases.json'):
    """Load test cases từ JSON"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        # Fallback: test cases mặc định
        return generate_default_test_cases()


def generate_default_test_cases():
    """Tạo 30 test cases mặc định"""
    return [
        {"id": 1, "input": "Họp nhóm 10 giờ sáng mai ở phòng 302"},
        {"id": 2, "input": "Meeting khách hàng 14:30 chiều nay tại tầng 5"},
        {"id": 3, "input": "Gặp team 9h thứ 2 tuần sau"},
        {"id": 4, "input": "Training chiều mai phòng 101"},
        {"id": 5, "input": "Họp sếp 15h tòa B"},
        {"id": 6, "input": "Seminar 9 giờ sáng thứ 6"},
        {"id": 7, "input": "Call với client 10:30"},
        {"id": 8, "input": "Review code 2h chiều"},
        {"id": 9, "input": "Họp định kỳ 9h thứ 2 hàng tuần"},
        {"id": 10, "input": "Phỏng vấn ứng viên 3h chiều mai"},
        {"id": 11, "input": "Họp 10h30 sáng 01/12/2025"},
        {"id": 12, "input": "Gặp đối tác tầng 3 tòa A 14h"},
        {"id": 13, "input": "Workshop sáng thứ 7"},
        {"id": 14, "input": "Học tiếng Anh 7h tối"},
        {"id": 15, "input": "Họp team chiều thứ 4"},
        {"id": 16, "input": "Meeting 9:30 phòng họp lớn"},
        {"id": 17, "input": "Thảo luận dự án 2h chiều mai"},
        {"id": 18, "input": "Báo cáo sếp 4h chiều hôm nay"},
        {"id": 19, "input": "Training nhân viên mới 9h sáng"},
        {"id": 20, "input": "Gặp khách VIP 10h tòa B tầng 10"},
        {"id": 21, "input": "Họp quý 3h chiều thứ 6"},
        {"id": 22, "input": "Review performance 9h30 sáng mai"},
        {"id": 23, "input": "Call zoom 2pm"},
        {"id": 24, "input": "Họp gấp 15h hôm nay"},
        {"id": 25, "input": "Seminar AI 9h thứ 7 tuần sau"},
        {"id": 26, "input": "Ăn trưa với đồng nghiệp 12h"},
        {"id": 27, "input": "Đánh giá nhân viên 2h chiều thứ 5"},
        {"id": 28, "input": "Presentation 10h phòng 201"},
        {"id": 29, "input": "Họp ban giám đốc 8h30 sáng"},
        {"id": 30, "input": "Training Excel 3h chiều mai"},
    ]


def evaluate():
    """Chạy evaluation"""
    assistant = PersonalScheduleAssistant()
    test_cases = load_test_cases()
    
    results = []
    success_count = 0
    confidence_scores = []
    
    print("="*80)
    print("EVALUATION - 30 TEST CASES")
    print("="*80)
    
    for test in test_cases:
        test_id = test['id']
        text = test['input']
        
        result = assistant.process(text)
        
        # Đánh giá
        success = result['success']
        confidence = result.get('confidence', 0)
        quality = result.get('quality', 'poor')
        
        if success:
            success_count += 1
        
        confidence_scores.append(confidence)
        
        # Display
        status = "✅" if success else "❌"
        print(f"\n[{test_id:2d}] {status} {text}")
        print(f"     Confidence: {confidence:.0f}% ({quality})")
        
        if success:
            schedule = result['schedule']
            print(f"     Event: {schedule['event']}")
            print(f"     Time: {schedule['start_time']}")
            if schedule.get('location'):
                print(f"     Location: {schedule['location']}")
        else:
            print(f"     Errors: {result['errors']}")
        
        results.append({
            'id': test_id,
            'input': text,
            'success': success,
            'confidence': confidence,
            'quality': quality,
            'output': result['schedule'] if success else None
        })
    
    # Statistics
    accuracy = (success_count / len(test_cases)) * 100
    avg_confidence = sum(confidence_scores) / len(confidence_scores)
    
    print("\n" + "="*80)
    print("📊 STATISTICS")
    print("="*80)
    print(f"Total Tests:          {len(test_cases)}")
    print(f"Successful:           {success_count}")
    print(f"Failed:               {len(test_cases) - success_count}")
    print(f"Accuracy:             {accuracy:.1f}%")
    print(f"Avg Confidence:       {avg_confidence:.1f}%")
    print("="*80)
    
    # Save results
    with open('evaluation_results.json', 'w', encoding='utf-8') as f:
        json.dump({
            'accuracy': accuracy,
            'avg_confidence': avg_confidence,
            'results': results
        }, f, ensure_ascii=False, indent=2)
    
    print("\n💾 Results saved to: evaluation_results.json")
    
    return accuracy >= 80  # Pass if >= 80%


if __name__ == "__main__":
    passed = evaluate()
    sys.exit(0 if passed else 1)