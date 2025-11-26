import sys
sys.path.append('.')

from src.nlp.preprocessor import Preprocessor
from src.nlp.ner_extractor import NERExtractor
from src.nlp.rule_extractor import RuleExtractor


def test_pipeline():
    """Test toàn bộ pipeline của 3 components"""
    
    # Khởi tạo
    preprocessor = Preprocessor()
    ner_extractor = NERExtractor()
    rule_extractor = RuleExtractor()
    
    # Test case
    text = "Họp nhóm 10 giờ sáng mai ở phòng 302, nhắc trước 15 phút"
    
    print("=" * 70)
    print("PIPELINE TEST: Component 1 → 2 → 3")
    print("=" * 70)
    print(f"\n📝 Input: {text}\n")
    
    # Component 1: Preprocessing
    print("🔹 COMPONENT 1: PREPROCESSOR")
    preprocessed = preprocessor.process(text)
    print(f"Normalized: {preprocessed['normalized']}")
    print(f"Tokens: {preprocessed['tokens']}\n")
    
    # Component 2: NER Extraction
    print("🔹 COMPONENT 2: NER EXTRACTOR")
    ner_result = ner_extractor.extract(preprocessed['normalized'])
    print(f"TIME entities: {ner_result['time']}")
    print(f"LOCATION entities: {ner_result['location']}\n")
    
    # Component 3: Rule-based Extraction
    print("🔹 COMPONENT 3: RULE EXTRACTOR")
    rule_result = rule_extractor.extract_all(preprocessed['normalized'])
    print(f"Event: {rule_result['event']}")
    print(f"Time: hour={rule_result['time_components']['hour']}, "
          f"period={rule_result['time_components']['period']}")
    print(f"Location: {rule_result['location_components']['full_location']}")
    print(f"Reminder: {rule_result['reminder_minutes']} phút\n")
    
    print("=" * 70)


if __name__ == "__main__":
    test_pipeline()