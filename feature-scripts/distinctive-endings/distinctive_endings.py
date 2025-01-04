"""
SETUP: conda activate py39
Code co-authored with ChatGPT
"""
import os
import spacy
from gensim.models import KeyedVectors
from nltk.tokenize import sent_tokenize

# File paths
human_stories_dir = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/human-stories"
generated_stories_dir = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/generated-stories"
human_results_file = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/distinctive-endings/results/human_endings_results.txt"
generated_results_file = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/distinctive-endings/results/generated_endings_results.txt"

# Load language model for embeddings
nlp = spacy.load("en_core_web_md")

# Function to calculate Word Mover's Distance
def calculate_wmd(text_a, text_b, nlp):
    tokens_a = [token.text for token in nlp(text_a) if not token.is_stop and token.is_alpha]
    tokens_b = [token.text for token in nlp(text_b) if not token.is_stop and token.is_alpha]
    
    if not tokens_a or not tokens_b:
        return float('inf')  # If one of the sets is empty, return infinity
    
    model = KeyedVectors(vector_size=300)  # Initialize empty embeddings (mock if needed)
    for token in nlp.vocab:
        if token.has_vector:
            model.add_vector(token.text, token.vector)
    
    # Calculate Word Mover's Distance
    return model.wmdistance(tokens_a, tokens_b)

# Function to process a single story
def process_story(file_path):
    with open(file_path, "r") as f:
        content = f.read()
    
    sentences = sent_tokenize(content)

    if len(sentences) < 20:
        return None, "Insufficient content"
    
    beginning = " ".join(sentences[:-20])
    ending = " ".join(sentences[-20:])
    min_change = calculate_wmd(beginning, ending, nlp)

    return os.path.basename(file_path), min_change

# Function to process a folder and write results
def analyze_folder(folder_path, results_file):
    results = []

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path) and file_name.endswith(".txt"):
            title, min_change = process_story(file_path)
            if title:
                results.append(f"Title: {title}\nMin Change: {min_change}\n")

    # Write results to file
    with open(results_file, "w") as f:
        f.write("### Analysis Results for Each File ###\n\n")
        f.writelines(results)

# Run analysis
analyze_folder(human_stories_dir, human_results_file)
analyze_folder(generated_stories_dir, generated_results_file)

print("Analysis complete. Results saved.")
