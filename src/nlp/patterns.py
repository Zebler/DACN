TIME_PATTERNS = {
    # Giờ cụ thể: 10h, 10 giờ, 10:30, 14h30
    'hour_minute': [
        r'(\d{1,2}):(\d{2})',  # 10:30, 14:00
        r'(\d{1,2})h(\d{2})',  # 10h30, 14h00
        r'(\d{1,2})\s*giờ\s*(\d{2})\s*phút',  # 10 giờ 30 phút
        r'(\d{1,2})\s*giờ',  # 10 giờ, 14 giờ
        r'(\d{1,2})h',  # 10h, 14h
    ],
    
    # Buổi trong ngày: sáng, chiều, tối, trưa
    'period': r'(sáng|chiều|tối|trưa|đêm)',
    
    # Ngày tương đối: hôm nay, mai, ngày mai, tuần sau
    'relative_day': r'(hôm nay|hôm qua|mai|ngày mai|mốt|ngày kia|tuần sau|tuần tới|tháng sau|tháng tới)',
    
    # Thứ trong tuần: thứ 2, thứ hai, t2
    'weekday': r'(thứ\s*(hai|ba|bốn|tư|năm|sáu|bảy|2|3|4|5|6|7)|chủ nhật|cn)',
    
    # Ngày cụ thể: 01/11, 1/11/2025
    'date': r'(\d{1,2})[\/\-](\d{1,2})([\/\-](\d{2,4}))?',
}

# ============= LOCATION PATTERNS =============

LOCATION_PATTERNS = {
    # Phòng: phòng 302, phòng A, phòng họp
    'room': r'phòng\s+(\w+|\d+)',
    
    # Tầng: tầng 5, tầng 1
    'floor': r'tầng\s+(\w+|\d+)',
    
    # Tòa nhà: tòa A, tòa B
    'building': r'tòa\s+(\w+)',
    
    # Văn phòng: văn phòng A, văn phòng công ty
    'office': r'văn\s*phòng\s+(\w+)',
    
    # Địa điểm chung: tại, ở
    'location_marker': r'(tại|ở|tại\s*tại)\s+([^\s,]+(?:\s+[^\s,]+)*)',
}

# ============= EVENT PATTERNS =============

EVENT_PATTERNS = {
    # Động từ sự kiện: họp, gặp, meeting, họp team
    'action_verb': r'(họp|gặp|meeting|meet|thảo luận|làm việc|training|học|seminar)',
    
    # Đối tượng: khách hàng, team, nhóm
    'object': r'(khách hàng|team|nhóm|đối tác|sếp|giám đốc|anh|chị)',
}

# ============= REMINDER PATTERNS =============

REMINDER_PATTERNS = {
    # Nhắc trước: nhắc trước 15 phút, nhắc 30 phút trước
    'remind_before': r'nhắc\s*(trước)?\s*(\d+)\s*(phút|giờ)',
    
    # Mặc định: mặc định 15 phút
    'default_minutes': 15
}

# ============= HELPER DICTIONARIES =============

WEEKDAY_MAP = {
    'thứ hai': 0, 'thứ 2': 0, 't2': 0,
    'thứ ba': 1, 'thứ 3': 1, 't3': 1,
    'thứ tư': 2, 'thứ 4': 2, 't4': 2, 'thứ bốn': 2,
    'thứ năm': 3, 'thứ 5': 3, 't5': 3,
    'thứ sáu': 4, 'thứ 6': 4, 't6': 4,
    'thứ bảy': 5, 'thứ 7': 5, 't7': 5,
    'chủ nhật': 6, 'cn': 6,
}

PERIOD_HOUR_MAP = {
    'sáng': (6, 11),
    'trưa': (11, 13),
    'chiều': (13, 18),
    'tối': (18, 22),
    'đêm': (22, 6),
}

RELATIVE_DAY_MAP = {
    'hôm nay': 0,
    'hôm qua': -1,
    'mai': 1,
    'ngày mai': 1,
    'mốt': 2,
    'ngày kia': 2,
}

# ============= VALIDATION RULES =============

VALIDATION_RULES = {
    'hour_range': (0, 23),
    'minute_range': (0, 59),
    'day_range': (1, 31),
    'month_range': (1, 12),
}   