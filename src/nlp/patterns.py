TIME_PATTERNS = {
    # Giờ cụ thể: 10h, 10 giờ, 10:30, 14h30, 10g, 10g30
    'hour_minute': [
        r'(\d{1,2}):(\d{2})',  # 10:30, 14:00
        r'(\d{1,2})h(\d{2})',  # 10h30, 14h00
        r'(\d{1,2})g(\d{2})',  # 10g30 (viết tắt)
        r'(\d{1,2})\s*giờ\s*(\d{2})\s*phút',  # 10 giờ 30 phút
        r'(\d{1,2})\s*giờ\s*rưỡi',  # 10 giờ rưỡi -> 10:30
        r'(\d{1,2})\s*giờ\s*kém\s*(\d{1,2})',  # 11 giờ kém 15 (10:45)
        r'(\d{1,2})\s*giờ',  # 10 giờ, 14 giờ
        r'(\d{1,2})h',  # 10h, 14h
        r'(\d{1,2})g',  # 10g (viết tắt giờ)
    ],
    
    # Buổi trong ngày: sáng, chiều, tối, trưa
    'period': r'(sáng|buổi sáng|sáng sớm|chiều|buổi chiều|tối|buổi tối|tối muộn|trưa|buổi trưa|đêm|nửa đêm|khuya)',
    
    # Ngày tương đối
    'relative_day': r'(hôm nay|hôm qua|hqua|mai|ngày mai|ngày hôm nay|mốt|ngày mốt|ngày kia|tuần sau|tuần tới|tuần này|tháng sau|tháng tới|tháng này|năm sau|năm tới)',
    
    # Thứ trong tuần
    'weekday': r'(thứ\s*(hai|ba|bốn|tư|năm|sáu|bảy|2|3|4|5|6|7)|chủ nhật|chủ nhật|cn|t2|t3|t4|t5|t6|t7)',
    
    # Ngày cụ thể: 01/11, 1/11/2025, 1-11, 1.11
    'date': r'(\d{1,2})[\/\-\.](\d{1,2})([\/\-\.](\d{2,4}))?',
    
    # Khoảng thời gian: từ 10h đến 11h, 10h-11h
    'time_range': r'(từ\s*)?(\d{1,2}):?(\d{2})?\s*(đến|tới|-)\s*(\d{1,2}):?(\d{2})?',
}

# ============= LOCATION PATTERNS =============

LOCATION_PATTERNS = {
    # Phòng: phòng 302, phòng A, phòng họp, P302
    'room': r'(phòng|p\.?|room)\s*(\w+|\d+)',
    
    # Tầng: tầng 5, tầng 1, lầu 2
    'floor': r'(tầng|lầu|floor)\s*(\w+|\d+)',
    
    # Tòa nhà: tòa A, tòa B, toà nhà A
    'building': r'(tòa|toà|tòa nhà|toà nhà|building)\s*(\w+)',
    
    # Văn phòng: văn phòng A, văn phòng công ty, VP
    'office': r'(văn\s*phòng|vp|office)\s*(\w+)',
    
    # Địa điểm chung: tại, ở, tại địa chỉ
    'location_marker': r'(tại|ở|tại\s*tại|địa chỉ|address)\s+([^\s,]+(?:\s+[^\s,]+)*)',
    
    # Hội trường, phòng họp, khu vực
    'meeting_space': r'(hội trường|phòng họp|khu vực|khu|area)\s*(\w+)?',
    
    # Địa danh cụ thể
    'venue': r'(khách sạn|hotel|cafe|cà phê|nhà hàng|quán|công ty|trường|trung tâm|center)\s+([^\s,]+(?:\s+[^\s,]+)*)',
}

# ============= EVENT PATTERNS =============

EVENT_PATTERNS = {
    # Động từ sự kiện
    'action_verb': r'(họp|gặp|meeting|meet|thảo luận|làm việc|training|train|học|seminar|workshop|presentation|present|trình bày|báo cáo|review|đánh giá|phỏng vấn|interview|call|gọi điện|video call|zoom|conference|hội nghị|buổi|sự kiện|event)',
    
    # Đối tượng
    'object': r'(khách hàng|client|customer|team|nhóm|đội|group|đối tác|partner|sếp|boss|giám đốc|director|manager|quản lý|anh|chị|bạn|colleague|đồng nghiệp|phòng ban|department|công ty|company)',
    
    # Loại cuộc họp
    'meeting_type': r'(họp\s*(gấp|khẩn|quan trọng|định kỳ|tuần|tháng|quý|1-1|one on one|nội bộ|internal|external|bên ngoài))',
}

# ============= REMINDER PATTERNS =============

REMINDER_PATTERNS = {
    # Nhắc trước: nhắc trước 15 phút, nhắc 30 phút trước, remind 1h before
    'remind_before': r'(nhắc|remind|thông báo|notify)\s*(trước|before)?\s*(\d+)\s*(phút|minutes?|min|giờ|hours?|h)',
    
    # Mặc định: mặc định 15 phút
    'default_minutes': 15,
    
    # Nhắc nhiều lần
    'multiple_reminders': r'nhắc\s*(\d+)\s*lần',
}

# ============= HELPER DICTIONARIES =============

WEEKDAY_MAP = {
    'thứ hai': 0, 'thứ 2': 0, 't2': 0, 'thu 2': 0,
    'thứ ba': 1, 'thứ 3': 1, 't3': 1, 'thu 3': 1,
    'thứ tư': 2, 'thứ 4': 2, 't4': 2, 'thứ bốn': 2, 'thu 4': 2,
    'thứ năm': 3, 'thứ 5': 3, 't5': 3, 'thu 5': 3,
    'thứ sáu': 4, 'thứ 6': 4, 't6': 4, 'thu 6': 4,
    'thứ bảy': 5, 'thứ 7': 5, 't7': 5, 'thu 7': 5,
    'chủ nhật': 6, 'chủ nhật': 6, 'cn': 6, 'sunday': 6,
}

PERIOD_HOUR_MAP = {
    'sáng': (6, 11),
    'buổi sáng': (6, 11),
    'sáng sớm': (6, 8),
    'trưa': (11, 13),
    'buổi trưa': (11, 13),
    'chiều': (13, 18),
    'buổi chiều': (13, 18),
    'tối': (18, 22),
    'buổi tối': (18, 22),
    'tối muộn': (20, 23),
    'đêm': (22, 6),
    'nửa đêm': (0, 2),
    'khuya': (22, 2),
}

RELATIVE_DAY_MAP = {
    'hôm nay': 0,
    'ngày hôm nay': 0,
    'hôm qua': -1,
    'hqua': -1,
    'mai': 1,
    'ngày mai': 1,
    'mốt': 2,
    'ngày mốt': 2,
    'ngày kia': 2,
    'tuần này': 0,
    'tuần sau': 7,
    'tuần tới': 7,
    'tháng này': 0,
    'tháng sau': 30,
    'tháng tới': 30,
    'năm sau': 365,
    'năm tới': 365,
}

# ============= SPECIAL TIME PHRASES =============

SPECIAL_TIME_MAP = {
    'giờ rưỡi': 30,  # minutes to add
    'kém 15': -15,
    'kém mười lăm': -15,
    'kém tư': -15,
}

# ============= VALIDATION RULES =============

VALIDATION_RULES = {
    'hour_range': (0, 23),
    'minute_range': (0, 59),
    'day_range': (1, 31),
    'month_range': (1, 12),
    'max_event_length': 200,
    'max_location_length': 200,
    'max_reminder_hours': 24,
}