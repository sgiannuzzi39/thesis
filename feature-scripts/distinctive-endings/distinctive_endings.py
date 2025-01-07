"""
SETUP: conda activate py39
Code co-authored with ChatGPT
"""
import os
import spacy
from gensim.models import KeyedVectors
from nltk.tokenize import word_tokenize

human_stories_dir = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/human-stories"
generated_stories_dir = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/generated-stories"
human_results_file = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/distinctive-endings/results/human_quarters_results.txt"
generated_results_file = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/distinctive-endings/results/generated_quarters_results.txt"

nlp = spacy.load("en_core_web_md")

model = KeyedVectors(vector_size=300)
for token in nlp.vocab:
    if token.has_vector:
        model.add_vector(token.text, token.vector)

def calculate_wmd(text_a, text_b):
    tokens_a = [token for token in word_tokenize(text_a) if token.isalpha()]
    tokens_b = [token for token in word_tokenize(text_b) if token.isalpha()]

    if not tokens_a or not tokens_b:
        return float('inf')

    return model.wmdistance(tokens_a, tokens_b)

def split_into_quarters(text):
    words = word_tokenize(text)
    total_words = len(words)
    quarter_size = total_words // 4

    quarters = [
        " ".join(words[:quarter_size]),
        " ".join(words[quarter_size:2 * quarter_size]),
        " ".join(words[2 * quarter_size:3 * quarter_size]),
        " ".join(words[3 * quarter_size:])
    ]

    return quarters

def process_story(file_path):
    with open(file_path, "r") as f:
        content = f.read()

    quarters = split_into_quarters(content)

    if len(quarters) < 4:
        return None, "Insufficient content for WMD calculation"

    wmd_results = []

    for i in range(len(quarters) - 1):
        wmd = calculate_wmd(quarters[i], quarters[i + 1])
        wmd_results.append(f"Quarter {i + 1} to Quarter {i + 2}: WMD = {wmd:.4f}")

    return os.path.basename(file_path), "\n".join(wmd_results)

def analyze_folder(folder_path, results_file):
    results = []

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path) and file_name.endswith(".txt"):
            title, wmd_results = process_story(file_path)
            if title:
                results.append(f"Title: {title}\n{wmd_results}\n\n")

    with open(results_file, "w") as f:
        f.write("### Analysis Results for Each File ###\n\n")
        f.writelines(results)

analyze_folder(human_stories_dir, human_results_file)
analyze_folder(generated_stories_dir, generated_results_file)

print("Analysis complete. Results saved.")
