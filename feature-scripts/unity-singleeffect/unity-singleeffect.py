''' 
    SETUP: conda activate spacy_env
    Code co-authored with ChatGPT

'''

import os
import re
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from collections import Counter
import chardet
import numpy as np

generated_dir = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/generated-stories"
human_dir = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/human-stories"
generated_output = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/unity-singleeffect/results/generated_results.txt"
human_output = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/unity-singleeffect/results/human_results.txt"

stemmer = PorterStemmer()

def compute_moving_ttr(tokens, window_size=100, step=1):
    moving_ttr = []
    if len(tokens) < window_size:
        ttr = len(set(tokens)) / len(tokens) if tokens else 0
        moving_ttr.append(ttr)
    else:
        for i in range(0, len(tokens) - window_size + 1, step):
            window = tokens[i:i+window_size]
            ttr_window = len(set(window)) / window_size
            moving_ttr.append(ttr_window)
    return moving_ttr

def process_file(file_path, window_size=100, step=1):
    with open(file_path, 'rb') as file: 
        raw_data = file.read()
        encoding = chardet.detect(raw_data)['encoding']

    with open(file_path, 'r', encoding=encoding, errors='replace') as file:
        content = file.read()

    title_match = re.search(r"Title:\s*(.*)", content)
    title = title_match.group(1).strip() if title_match else "Untitled"

    story_text = content.split("\n", 1)[-1].strip() if '\n' in content else ""

    print(f"Processing file: {file_path}\nTitle: {title}\nExtracted Text (first 100 chars): {story_text[:100]}")

    tokens = word_tokenize(story_text)
    stemmed_tokens = [stemmer.stem(token.lower()) for token in tokens if token.isalnum()]

    print(f"Token count: {len(tokens)} | Stemmed tokens count: {len(stemmed_tokens)}")

    moving_ttr_list = compute_moving_ttr(stemmed_tokens, window_size=window_size, step=step)
    avg_moving_ttr = np.mean(moving_ttr_list) if moving_ttr_list else 0

    return title, avg_moving_ttr

def analyze_directory(directory, output_file, window_size=100, step=1):
    results = []

    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        if os.path.isfile(file_path):
            try:
                title, avg_moving_ttr = process_file(file_path, window_size, step)
                results.append((title, avg_moving_ttr))
            except Exception as e:
                print(f"Error processing file {file_path}: {e}")

    with open(output_file, 'w') as output:
        output.write("### Analysis Results for Each File ###\n\n")
        for title, avg_moving_ttr in results:
            output.write(f"Title: {title}\nMoving TTR: {avg_moving_ttr:.4f}\n\n")

analyze_directory(generated_dir, generated_output)
analyze_directory(human_dir, human_output)

print("Analysis complete! Results saved.")
