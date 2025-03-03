# preprocess.py
import re

def clean_story(text):
    # Remove common non-story elements
    text = re.sub(r'Rating:.*', '', text)
    text = re.sub(r'Genre:.*', '', text)
    text = re.sub(r'Author:.*', '', text)
    text = re.sub(r'Title:.*', '', text)
    # Any other cleanup based on your data
    return text.strip()

def preprocess_stories(stories):
    preprocessed_stories = []
    for story in stories:
        # Assuming each story is just a plain text string
        cleaned_story = clean_story(story)
        preprocessed_stories.append({
            'title': 'Unknown Title',  # You can set a default or extract it if needed
            'author': 'Unknown Author',  # You can set a default or extract it if needed
            'content': cleaned_story
        })
    return preprocessed_stories
