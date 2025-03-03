import os

def load_txt_files(directory):
    stories = []
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r', encoding='utf-8') as file:
                stories.append(file.read())
    return stories