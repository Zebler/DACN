from underthesea import word_tokenize
import re


class Preprocessor:
    """Xử lý và chuẩn hóa văn bản tiếng Việt đầu vào"""
    
    def __init__(self):
        # Từ điển chuẩn hóa các biến thể
        self.time_normalize = {
            'h': 'giờ',
            'g': 'giờ',
            'phút': 'phút',
            'ph': 'phút',
            'p': 'phút',
            'min': 'phút',
            'mins': 'phút',
            'rưỡi': 'rưỡi',
            'kém': 'kém',
        }
        
        self.day_normalize = {
            't2': 'thứ hai',
            't3': 'thứ ba',
            't4': 'thứ tư',
            't5': 'thứ năm',
            't6': 'thứ sáu',
            't7': 'thứ bảy',
            'cn': 'chủ nhật',
            'thu 2': 'thứ hai',
            'thu 3': 'thứ ba',
            'thu 4': 'thứ tư',
            'thu 5': 'thứ năm',
            'thu 6': 'thứ sáu',
            'thu 7': 'thứ bảy',
        }
        
        # Chuẩn hóa các từ viết tắt địa điểm
        self.location_normalize = {
            'vp': 'văn phòng',
            'p.': 'phòng',
            'p': 'phòng',
        }
        
        # Chuẩn hóa sự kiện
        self.event_normalize = {
            'mtg': 'meeting',
            'meet': 'meeting',
        }
    
    def clean_text(self, text):
        """
        Làm sạch văn bản đầu vào
        
        Args:
            text (str): Văn bản gốc
            
        Returns:
            str: Văn bản đã làm sạch
        """
        if not text:
            return ""
        
        # Chuyển về lowercase
        text = text.lower().strip()
        
        # Xóa ký tự đặc biệt thừa (giữ lại dấu câu cần thiết)
        text = re.sub(r'\s+', ' ', text)  # Xóa khoảng trắng thừa
        
        # Chuẩn hóa dấu hai chấm trong giờ
        text = re.sub(r'(\d+)\s*:\s*(\d+)', r'\1:\2', text)  # 10 : 30 -> 10:30
        
        return text
    
    def normalize_terms(self, text):
        """
        Chuẩn hóa các từ viết tắt và biến thể
        
        Args:
            text (str): Văn bản đầu vào
            
        Returns:
            str: Văn bản đã chuẩn hóa
        """
        # IMPORTANT: Bảo vệ "phòng" khỏi bị chuẩn hóa thành "p"
        # Chuẩn hóa thời gian (CHỈ khi đứng riêng hoặc có số đằng sau)
        text = re.sub(r'\b(\d+)\s*h\b', r'\1 giờ', text)  # 10h -> 10 giờ
        text = re.sub(r'\b(\d+)\s*g\b', r'\1 giờ', text)  # 10g -> 10 giờ
        
        # Chuẩn hóa ngày trong tuần
        for abbr, full in self.day_normalize.items():
            text = re.sub(r'\b' + abbr + r'\b', full, text)
        
        return text
    
    def tokenize(self, text):
        """
        Phân đoạn từ tiếng Việt
        
        Args:
            text (str): Văn bản đầu vào
            
        Returns:
            list: Danh sách tokens
        """
        try:
            tokens = word_tokenize(text, format="text")
            return tokens
        except Exception as e:
            print(f"Lỗi tokenize: {e}")
            return text  # Fallback: trả về text gốc
    
    def process(self, text):
        """
        Xử lý toàn bộ pipeline preprocessing
        
        Args:
            text (str): Câu tiếng Việt tự nhiên
            
        Returns:
            dict: {
                'original': văn bản gốc,
                'cleaned': văn bản đã làm sạch,
                'normalized': văn bản đã chuẩn hóa,
                'tokens': tokens đã phân đoạn
            }
        """
        # Step 1: Làm sạch
        cleaned = self.clean_text(text)
        
        # Step 2: Chuẩn hóa
        normalized = self.normalize_terms(cleaned)
        
        # Step 3: Tokenize
        tokens = self.tokenize(normalized)
        
        return {
            'original': text,
            'cleaned': cleaned,
            'normalized': normalized,
            'tokens': tokens
        }