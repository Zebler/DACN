from underthesea import ner
import re


class NERExtractor:
    """Trích xuất thực thể TIME và LOCATION bằng NER"""
    
    def __init__(self):
        self.time_keywords = [
            'giờ', 'phút', 'sáng', 'chiều', 'tối', 'trưa', 'đêm',
            'mai', 'mốt', 'kia', 'hôm nay', 'ngày mai',
            'tuần', 'tháng', 'năm',
            'thứ hai', 'thứ ba', 'thứ tư', 'thứ năm', 'thứ sáu', 'thứ bảy', 'chủ nhật'
        ]
        
        self.location_keywords = [
            'phòng', 'tòa', 'tầng', 'văn phòng', 'hội trường',
            'công ty', 'cơ quan', 'trụ sở', 'chi nhánh',
            'quán', 'nhà hàng', 'cafe', 'khách sạn'
        ]
    
    def extract_with_ner(self, text):
        """
        Sử dụng underthesea NER để trích xuất thực thể
        
        Args:
            text (str): Văn bản đầu vào
            
        Returns:
            dict: {
                'time_entities': [...],
                'location_entities': [...],
                'all_entities': [...]
            }
        """
        try:
            # Chạy NER
            entities = ner(text)
            
            time_entities = []
            location_entities = []
            all_entities = []
            
            # Phân loại entities - xử lý cả tuple và list format
            for item in entities:
                # underthesea có thể trả về (word, tag) hoặc [word, tag] hoặc (word, pos, tag)
                if isinstance(item, (tuple, list)):
                    if len(item) == 2:
                        word, tag = item
                    elif len(item) >= 3:
                        word, _, tag = item[0], item[1], item[2]
                    else:
                        continue
                else:
                    continue
                
                entity_info = {
                    'word': word,
                    'tag': tag
                }
                all_entities.append(entity_info)
                
                # Lọc TIME entities
                if tag and ('TIME' in str(tag) or tag == 'B-TIME' or tag == 'I-TIME'):
                    time_entities.append(word)
                
                # Lọc LOCATION entities
                if tag and ('LOC' in str(tag) or tag == 'B-LOC' or tag == 'I-LOC'):
                    location_entities.append(word)
            
            return {
                'time_entities': time_entities,
                'location_entities': location_entities,
                'all_entities': all_entities
            }
        
        except Exception as e:
            print(f"Lỗi NER extraction: {e}")
            return {
                'time_entities': [],
                'location_entities': [],
                'all_entities': []
            }
    
    def extract_time_phrases(self, text):
        """
        Trích xuất cụm từ thời gian bằng keyword matching
        (Backup method khi NER không hoạt động tốt)
        
        Args:
            text (str): Văn bản đầu vào
            
        Returns:
            list: Danh sách cụm từ thời gian
        """
        time_phrases = []
        
        # Pattern 1: Giờ cụ thể (10h, 10 giờ, 10:30)
        patterns = [
            r'\d{1,2}:\d{2}',  # 10:30, 14:00
            r'\d{1,2}\s*giờ\s*\d{0,2}\s*phút?',  # 10 giờ 30 phút
            r'\d{1,2}h\d{0,2}',  # 10h30
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text)
            time_phrases.extend(matches)
        
        # Pattern 2: Từ khóa thời gian
        for keyword in self.time_keywords:
            if keyword in text:
                # Lấy ngữ cảnh xung quanh
                match = re.search(rf'\S*\s*{keyword}\s*\S*', text)
                if match:
                    time_phrases.append(match.group())
        
        return list(set(time_phrases))  # Loại trùng
    
    def extract_location_phrases(self, text):
        """
        Trích xuất cụm từ địa điểm bằng keyword matching
        
        Args:
            text (str): Văn bản đầu vào
            
        Returns:
            list: Danh sách cụm từ địa điểm
        """
        location_phrases = []
        
        # Pattern: "phòng 302", "tầng 5", "tòa A"
        patterns = [
            r'phòng\s+\w+',
            r'tầng\s+\w+',
            r'tòa\s+\w+',
            r'văn phòng\s+\w+',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text)
            location_phrases.extend(matches)
        
        # Từ khóa địa điểm
        for keyword in self.location_keywords:
            if keyword in text:
                match = re.search(rf'{keyword}\s+\S+', text)
                if match:
                    location_phrases.append(match.group())
        
        return list(set(location_phrases))
    
    def extract(self, text):
        """
        Pipeline chính: Kết hợp NER + keyword matching
        
        Args:
            text (str): Văn bản đầu vào
            
        Returns:
            dict: Kết quả trích xuất TIME và LOCATION
        """
        # Method 1: NER
        ner_result = self.extract_with_ner(text)
        
        # Method 2: Keyword matching (backup)
        time_phrases = self.extract_time_phrases(text)
        location_phrases = self.extract_location_phrases(text)
        
        # Merge results
        all_time = list(set(ner_result['time_entities'] + time_phrases))
        all_location = list(set(ner_result['location_entities'] + location_phrases))
        
        return {
            'time': all_time,
            'location': all_location,
            'ner_result': ner_result['all_entities']
        }