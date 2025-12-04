class ConfidenceCalculator:
    """Tính toán confidence score cho schedule"""
    
    def __init__(self):
        self.weights = {
            'has_time': 0.3,      # Có thời gian cụ thể
            'has_date': 0.2,      # Có ngày cụ thể
            'has_location': 0.15, # Có địa điểm
            'has_event': 0.2,     # Có tên sự kiện rõ ràng
            'time_valid': 0.15,   # Thời gian hợp lệ
        }
    
    def calculate(self, schedule, debug_info):
        """
        Tính confidence score (0-100%)
        
        Args:
            schedule (dict): Schedule object
            debug_info (dict): Debug information
            
        Returns:
            float: Confidence score (0-100)
        """
        score = 0
        details = {}
        
        # Check 1: Có thời gian cụ thể (giờ:phút)
        time_components = debug_info.get('rule_result', {}).get('time_components', {})
        has_hour = time_components.get('hour') is not None
        has_minute = time_components.get('minute') is not None
        
        if has_hour and has_minute:
            score += self.weights['has_time']
            details['has_time'] = True
        elif has_hour:
            score += self.weights['has_time'] * 0.7
            details['has_time'] = 'partial'
        
        # Check 2: Có ngày cụ thể
        has_date = (
            time_components.get('date') or
            time_components.get('weekday') or
            time_components.get('relative_day')
        )
        if has_date:
            score += self.weights['has_date']
            details['has_date'] = True
        
        # Check 3: Có địa điểm
        location = schedule.get('location', '').strip()
        if location:
            score += self.weights['has_location']
            details['has_location'] = True
        
        # Check 4: Có tên sự kiện rõ ràng
        event = schedule.get('event', '').strip()
        if event and len(event) > 3:
            score += self.weights['has_event']
            details['has_event'] = True
        
        # Check 5: Thời gian hợp lệ
        if schedule.get('start_time'):
            score += self.weights['time_valid']
            details['time_valid'] = True
        
        # Convert to percentage
        confidence = score * 100
        
        return confidence, details
    
    def get_quality_level(self, confidence):
        """
        Phân loại chất lượng dựa trên confidence
        
        Returns:
            str: 'excellent', 'good', 'fair', 'poor'
        """
        if confidence >= 80:
            return 'excellent'
        elif confidence >= 60:
            return 'good'
        elif confidence >= 40:
            return 'fair'
        else:
            return 'poor'