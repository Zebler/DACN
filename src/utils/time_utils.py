from datetime import datetime, timedelta
import pytz


# Timezone Việt Nam
VN_TZ = pytz.timezone('Asia/Ho_Chi_Minh')


def get_current_datetime():
    """
    Lấy datetime hiện tại theo timezone Việt Nam
    
    Returns:
        datetime: Datetime hiện tại
    """
    return datetime.now(VN_TZ)


def get_weekday_offset(weekday_name):
    """
    Tính offset từ hôm nay đến thứ được chỉ định
    
    Args:
        weekday_name (str): Tên thứ (VD: "thứ hai", "thứ 2")
        
    Returns:
        int: Số ngày cần cộng thêm
    """
    weekday_map = {
        'thứ hai': 0, 'thứ 2': 0, 't2': 0,
        'thứ ba': 1, 'thứ 3': 1, 't3': 1,
        'thứ tư': 2, 'thứ 4': 2, 't4': 2, 'thứ bốn': 2,
        'thứ năm': 3, 'thứ 5': 3, 't5': 3,
        'thứ sáu': 4, 'thứ 6': 4, 't6': 4,
        'thứ bảy': 5, 'thứ 7': 5, 't7': 5,
        'chủ nhật': 6, 'cn': 6,
    }
    
    target_weekday = weekday_map.get(weekday_name.lower())
    if target_weekday is None:
        return 0
    
    current = get_current_datetime()
    current_weekday = current.weekday()
    
    # Tính số ngày cần cộng
    offset = (target_weekday - current_weekday) % 7
    if offset == 0:
        offset = 7  # Nếu cùng thứ, lấy tuần sau
    
    return offset


def get_relative_day_offset(relative_term):
    """
    Tính offset từ hôm nay dựa trên từ tương đối
    
    Args:
        relative_term (str): "hôm nay", "mai", "tuần sau"...
        
    Returns:
        int: Số ngày cần cộng
    """
    relative_map = {
        'hôm nay': 0,
        'hôm qua': -1,
        'mai': 1,
        'ngày mai': 1,
        'mốt': 2,
        'ngày kia': 2,
        'tuần sau': 7,
        'tuần tới': 7,
        'tháng sau': 30,
        'tháng tới': 30,
    }
    
    return relative_map.get(relative_term.lower(), 0)


def parse_period_to_hour(period):
    """
    Chuyển đổi buổi trong ngày thành giờ mặc định
    
    Args:
        period (str): "sáng", "chiều", "tối"...
        
    Returns:
        int: Giờ mặc định
    """
    period_hour_map = {
        'sáng': 9,
        'buổi sáng': 9,
        'sáng sớm': 7,
        'trưa': 12,
        'buổi trưa': 12,
        'chiều': 14,
        'buổi chiều': 14,
        'tối': 19,
        'buổi tối': 19,
        'tối muộn': 21,
        'đêm': 22,
        'khuya': 23,
        'nửa đêm': 0,
    }
    
    return period_hour_map.get(period.lower(), 9)


def format_datetime(dt, format_str='%Y-%m-%d %H:%M:%S'):
    """
    Format datetime thành string
    
    Args:
        dt (datetime): Datetime object
        format_str (str): Format string
        
    Returns:
        str: Datetime đã format
    """
    if dt is None:
        return None
    return dt.strftime(format_str)


def format_datetime_iso(dt):
    """
    Format datetime theo ISO 8601 format
    
    Args:
        dt (datetime): Datetime object
        
    Returns:
        str: ISO format string (VD: "2025-11-01T10:00:00")
    """
    if dt is None:
        return None
    return dt.strftime('%Y-%m-%dT%H:%M:%S')


def is_valid_time(hour, minute=0):
    """
    Kiểm tra giờ và phút hợp lệ
    
    Args:
        hour (int): Giờ
        minute (int): Phút (default 0)
        
    Returns:
        bool: True nếu hợp lệ
    """
    if hour is None:
        return False
    
    # Cho phép minute là None, mặc định = 0
    if minute is None:
        minute = 0
    
    try:
        return (0 <= hour <= 23) and (0 <= minute <= 59)
    except (TypeError, ValueError):
        return False


def calculate_reminder_time(start_time, reminder_minutes):
    """
    Tính thời gian nhắc nhở
    
    Args:
        start_time (datetime): Thời gian bắt đầu
        reminder_minutes (int): Số phút nhắc trước
        
    Returns:
        datetime: Thời gian nhắc nhở
    """
    if start_time is None:
        return None
    return start_time - timedelta(minutes=reminder_minutes)