from src.utils import clean_text

def preprocess_story(text):
    lines = text.split('\n')
    title = lines[0].replace('Title: ', '').strip()
    author = lines[1].replace('Author: ', '').strip()
    content = ' '.join(lines[3:]).strip()
    content = clean_text(content)
    return {'title': title, 'author': author, 'content': content}

def preprocess_stories(stories):
    return [preprocess_story(story) for story in stories]