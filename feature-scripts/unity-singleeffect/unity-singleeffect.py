import os
import re
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from collections import Counter
import chardet

generated_dir = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/generated-stories"
human_dir = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/human-stories"
generated_output = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/unity-singleeffect/results/generated_results.txt"
human_output = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/unity-singleeffect/results/human_results.txt"

stemmer = PorterStemmer()

def process_file(file_path):
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

    token_counts = Counter(stemmed_tokens)
    vvi = sum(1 / count for count in token_counts.values()) / len(token_counts) if token_counts else 0

    return title, vvi

def analyze_directory(directory, output_file):
    results = []

    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        if os.path.isfile(file_path):
            try:
                title, vvi = process_file(file_path)
                results.append((title, vvi))
            except Exception as e:
                print(f"Error processing file {file_path}: {e}")

    with open(output_file, 'w') as output:
        output.write("### Analysis Results for Each File ###\n\n")
        for title, vvi in results:
            output.write(f"Title: {title}\nVVI: {vvi:.4f}\n\n")

analyze_directory(generated_dir, generated_output)
analyze_directory(human_dir, human_output)

print("Analysis complete! Results saved.")
