"""
    SETUP: conda activate spacy_env
    Code co-authored with ChatGPT
"""

import os
import re
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize, sent_tokenize
from collections import Counter
import chardet
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.spatial.distance import euclidean

# Paths to directories and output files
generated_dir = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/generated-stories"
human_dir = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/human-stories"
generated_output = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/unity-singleeffect/results/generated_results.txt"
human_output = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/unity-singleeffect/results/human_results.txt"

# Initialize stemmer
stemmer = PorterStemmer()

# Initialize TF-IDF vectorizer
vectorizer = TfidfVectorizer()

def process_file(file_path):
    """
    Process a single file: read, tokenize, stem, calculate TTR, VVI, and average Euclidean distance between paragraphs.
    """
    # Detect encoding
    with open(file_path, 'rb') as file:  # Open in binary mode
        raw_data = file.read()
        encoding = chardet.detect(raw_data)['encoding']

    # Open file with detected encoding
    with open(file_path, 'r', encoding=encoding, errors='replace') as file:
        content = file.read()

    # Extract title and story text
    title_match = re.search(r"Title:\s*(.*)", content)
    title = title_match.group(1).strip() if title_match else "Untitled"

    # Extract story text: Assume the story starts after the first line containing 'Title:'
    story_text = content.split("\n", 1)[-1].strip() if '\n' in content else ""

    # Debug logging
    print(f"Processing file: {file_path}\nTitle: {title}\nExtracted Text (first 100 chars): {story_text[:100]}")

    # Split story into paragraphs
    paragraphs = [p.strip() for p in story_text.split("\n\n") if p.strip()]

    # Tokenize and stem words
    tokens = word_tokenize(story_text)
    stemmed_tokens = [stemmer.stem(token.lower()) for token in tokens if token.isalnum()]

    # Debug logging for tokens
    print(f"Token count: {len(tokens)} | Stemmed tokens count: {len(stemmed_tokens)}")

    # Calculate TTR
    types = set(stemmed_tokens)
    ttr = len(types) / len(stemmed_tokens) if stemmed_tokens else 0

    # Calculate VVI
    token_counts = Counter(stemmed_tokens)
    vvi = sum(1 / count for count in token_counts.values()) / len(token_counts) if token_counts else 0

    # Calculate average Euclidean distance between paragraphs
    if len(paragraphs) > 1:
        tfidf_matrix = vectorizer.fit_transform(paragraphs).toarray()
        distances = []
        for i in range(len(tfidf_matrix)):
            for j in range(i + 1, len(tfidf_matrix)):
                distances.append(euclidean(tfidf_matrix[i], tfidf_matrix[j]))
        avg_distance = sum(distances) / len(distances) if distances else 0
    else:
        avg_distance = 0

    return title, ttr, vvi, avg_distance

def analyze_directory(directory, output_file):
    """
    Analyze all files in a directory and write results to an output file.
    """
    results = []

    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        if os.path.isfile(file_path):
            try:
                title, ttr, vvi, avg_distance = process_file(file_path)
                results.append((title, ttr, vvi, avg_distance))
            except Exception as e:
                print(f"Error processing file {file_path}: {e}")

    # Write results to the output file
    with open(output_file, 'w') as output:
        output.write("### Analysis Results for Each File ###\n\n")
        for title, ttr, vvi, avg_distance in results:
            output.write(f"Title: {title}\nTTR: {ttr:.4f}\nVVI: {vvi:.4f}\nAverage Paragraph Distance: {avg_distance:.4f}\n\n")

# Run analysis
analyze_directory(generated_dir, generated_output)
analyze_directory(human_dir, human_output)

print("Analysis complete! Results saved.")
