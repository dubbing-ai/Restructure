import re
def clean_text_cv(text, replace_dict=None):
    """
    Cleans the input text by:
    - Removing spaces around specific punctuation marks
    - Replacing certain characters with spaces
    - Replacing words based on a provided dictionary
    - Removing extra spaces
    
    Parameters:
    text (str): The input text to clean.
    replace_dict (dict, optional): Dictionary where keys are words to be replaced and values are replacements.
    
    Returns:
    str: The cleaned text.
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

# replace_dict = {
#     "Facebook": "เฟซบุ๊ก",
#     "softmax": "ซอฟต์แม็กซ์",
#     "Astroturf": "แอสโตรเทิร์ฟ",
#     "Burke": "เบิร์ก",
#     "whilst": "ไวล์สท์",
#     "Kenny": "เคนนี",
#     "Flickr": "ฟลิกเกอร์",
#     "Asperger": "แอสเพอร์เกอร์",
#     "Johanna": "โจแอนนา",
#     "C" : "ซี",
#     "section": "เซคชัน",
#     "Mr Lincoln": "มิสเตอร์ ลินคอล์น",
#     "Brexiteers": "เบร็กซิทเทียร์ส",
#     "Brexit": "เบร็กซิท"
# }