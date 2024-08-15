import re

def clean_text(text):
    text = re.sub(r'\n+', ' ', text)
    text = text.replace('\n', ' ')
    return text.strip()