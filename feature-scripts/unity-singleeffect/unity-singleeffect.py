''' 
    SETUP: conda activate spacy_env
    Code co-authored with ChatGPT

'''
import nltk
nltk.download('punkt')
import os
import re
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from collections import Counter

# Paths to directories and output files
generated_dir = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/generated-stories"
human_dir = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/human-stories"
generated_output = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/unity-singleeffect/results/generated_results.txt"
human_output = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/unity-singleeffect/results/human_results.txt"

# Initialize stemmer
stemmer = PorterStemmer()

def process_file(file_path):
    """
    Process a single file: read, tokenize, stem, and calculate TTR and VVI.
    """
    with open(file_path, 'r') as file:
        content = file.read()

    # Extract title and story text
    title_match = re.search(r"Title:\s*(.*)", content)
    title = title_match.group(1).strip() if title_match else "Untitled"
    story_text = re.sub(r"Title:.*", "", content, flags=re.DOTALL).strip()

    # Tokenize and stem words
    tokens = word_tokenize(story_text)
    stemmed_tokens = [stemmer.stem(token.lower()) for token in tokens if token.isalnum()]

    # Calculate TTR
    types = set(stemmed_tokens)
    ttr = len(types) / len(stemmed_tokens) if stemmed_tokens else 0

    # Calculate VVI
    token_counts = Counter(stemmed_tokens)
    vvi = sum(1 / count for count in token_counts.values()) / len(token_counts) if token_counts else 0

    return title, ttr, vvi

def analyze_directory(directory, output_file):
    """
    Analyze all files in a directory and write results to an output file.
    """
    results = []

    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        if os.path.isfile(file_path):
            title, ttr, vvi = process_file(file_path)
            results.append((title, ttr, vvi))

    # Write results to the output file
    with open(output_file, 'w') as output:
        output.write("### Analysis Results for Each File ###\n\n")
        for title, ttr, vvi in results:
            output.write(f"Title: {title}\nTTR: {ttr:.4f}\nVVI: {vvi:.4f}\n\n")

# Run analysis
analyze_directory(generated_dir, generated_output)
analyze_directory(human_dir, human_output)

print("Analysis complete! Results saved.")
