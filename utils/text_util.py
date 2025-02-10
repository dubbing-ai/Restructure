import re
from pythainlp.util import maiyamok

def clean_text_cv(text, replace_dict=None):
    """
    Cleans text by.
    - Removing spaces around specific punctuation marks
    - Replacing certain characters with spaces
    - Replacing words based on a provided dictionary
    - Removing extra spaces
    
    Args:
        text (str): Input text to clean
        replace_dict (dict, optional): Word replacement mapping
        
    Returns:
        str: Cleaned text with removed punctuation and applied replacements
        
    Example:
        clean_text_cv("Hello, world!", {"Hello": "Hi"})
        # Returns: "Hi world"
    """
    chars_to_cutspace = r'["\'‘’“”]'
    chars_to_replace = r'[!"\',\-.:;?_|~—‘’“”]'

    # Remove spaces around chars_to_cutspace
    cleaned_text = re.sub(r'\s*([' + chars_to_cutspace[1:-1] + r'])\s*', '', text)
    
    # Replace chars_to_replace with space
    cleaned_text = re.sub(chars_to_replace, ' ', cleaned_text)

    # Replace words based on the provided dictionary
    if replace_dict:
        for word, replacement in replace_dict.items():
            cleaned_text = re.sub(r'\b' + re.escape(word) + r'\b', replacement, cleaned_text)
        for word, replacement in replace_dict.items():
            cleaned_text = re.sub(r'\s*([' + replacement + r'])\s*', r'\1', cleaned_text)

    # Remove extra spaces
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()

    return cleaned_text

"""
TODO: Use the dict in real code
"""
# exceptions = {
#     'เธอเป็นคนดีมาก ๆ': 'เธอเป็นคนดีมากมาก',
#     'ให้ประสานงานกับสมาชิกคนอื่น ๆ และหารือเกี่ยวกับปัญหานี้ในภายหลัง': 'ให้ประสานงานกับสมาชิกคนอื่นคนอื่น และหารือเกี่ยวกับปัญหานี้ในภายหลัง',
#     'ช่างเป็นสวนหลังบ้านที่ดีงามมาก ๆ จริง ๆ คุณนาย !': 'ช่างเป็นสวนหลังบ้านที่ดีงามมากมาก จริงจริง คุณนาย !',
#     'ฉันอาจจะผ่านเรื่องเล็ก ๆ น้อย ๆ นั้นไปได้ด้วยดี': 'ฉันอาจจะผ่านเรื่องเล็กเล็ก น้อยน้อย นั้นไปได้ด้วยดี',
#     'มันทำให้รู้สึกสดชื่นจริง ๆ ที่ได้นั่งท่ามกลางบรรยากาศที่มีแต่ลมพัดเย็น ๆ ที่แสนสบาย': 'มันทำให้รู้สึกสดชื่นจริงจริง ที่ได้นั่งท่ามกลางบรรยากาศที่มีแต่ลมพัดเย็นเย็น ที่แสนสบาย',
#     'ซาลกำลังทำให้คนอื่น ๆ โกรธ': 'ซาลกำลังทำให้คนอื่นอื่น โกรธ',
#     'มีทันตแพทย์และแพทย์คนอื่น ๆ ในคลินิกนี้': 'มีทันตแพทย์และแพทย์คนอื่นอื่น ในคลินิกนี้',
#     'ใครพูดรัว ๆ ติดกันได้นาน ๆ บอกเราด้วย': 'ใครพูดรัวรัว ติดกันได้นานนาน บอกเราด้วย',
#     '“ผมเสียใจจริง ๆ ที่ต้องไปครับท่าน” ฉันตอบกลับ': '“ผมเสียใจจริงจริง ที่ต้องไปครับท่าน” ฉันตอบกลับ',
#     'ใจเย็น ๆ ค่ะ ไม่ต้องตื่นเต้น': 'ใจเย็นเย็น ค่ะ ไม่ต้องตื่นเต้น',
#     'เรื่องนี้มันดีมาก ๆ': 'เรื่องนี้มันดีมากมาก',
#     'คุณผู้หญิงเหมือนเด็กเล็ก ๆ': 'คุณผู้หญิงเหมือนเด็กเล็กเล็ก',
#     "'ช่างเป็นดอกไม้ดอกใหญ่ ๆ สมอย่างที่ต้องเป็นจริง ๆ !' เธอแสดงความคิดต่อมาของเธอ": "'ช่างเป็นดอกไม้ดอกใหญ่ใหญ่ สมอย่างที่ต้องเป็นจริงจริง !' เธอแสดงความคิดต่อมาของเธอ",
#     'คนอื่น ๆ เดินตามรอยของเขา' :'คนอื่นอื่น เดินตามรอยของเขา'
# }

def handle_maiyamok(text: str, exceptions: dict = None) -> str:
    text = text.strip()
    if 'ๆ' not in text:
        return text
    if exceptions:
        if text in exceptions:
            return exceptions[text]
    chunks = maiyamok(text)
    processed_text = ''.join(chunks)
    return processed_text