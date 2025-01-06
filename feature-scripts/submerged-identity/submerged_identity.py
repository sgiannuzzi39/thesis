"""
SETUP: conda activate py39
Code co-authored with ChatGPT
"""

import os
import re
from textblob import TextBlob
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from collections import Counter
from tqdm import tqdm

generated_dir = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/generated-stories"
human_dir = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/human-stories"
output_dir = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/submerged-identity/results"
os.makedirs(output_dir, exist_ok=True)

generated_output_file = os.path.join(output_dir, "generated_si_scores.txt")
human_output_file = os.path.join(output_dir, "human_si_scores.txt")

submerged_words = {"forgotten", "invisible", "unseen", "neglected", "lost", "despair", "isolation", "downtrodden", "inadequate"}
stop_words = set(stopwords.words('english'))

def compute_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity

def lexical_density(text):
    words = word_tokenize(text)
    meaningful_words = [word for word in words if word.lower() not in stop_words and word.isalnum()]
    return len(set(meaningful_words)) / len(meaningful_words) if meaningful_words else 0

def submerged_score(text):
    sentences = sent_tokenize(text)
    sentiment_score = sum(compute_sentiment(sentence) for sentence in sentences) / len(sentences)
    
    word_tokens = word_tokenize(text.lower())
    word_counts = Counter(word_tokens)
    submerged_word_count = sum(word_counts[word] for word in submerged_words if word in word_counts)

    density = lexical_density(text)

    score = (0.5 * -sentiment_score) + (0.3 * submerged_word_count) + (0.2 * (1 - density))
    return max(score, 0) 

def process_directory(directory):
    scores = []
    for file_name in tqdm(os.listdir(directory), desc=f"Processing {directory}"):
        file_path = os.path.join(directory, file_name)
        if not file_name.endswith(".txt"):
            continue
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()
            title_match = re.search(r"^(.*?)(\n|$)", text)  
            title = title_match.group(1).strip() if title_match else "Unknown Title"
            score = submerged_score(text)
            scores.append((title, score))
    return scores

def save_scores(scores, output_file):
    with open(output_file, "w", encoding="utf-8") as file:
        for title, score in scores:
            file.write(f"{title}: {score:.2f}\n")

def main():
    print("Starting analysis...")
    generated_scores = process_directory(generated_dir)
    human_scores = process_directory(human_dir)

    save_scores(generated_scores, generated_output_file)
    save_scores(human_scores, human_output_file)
    print(f"Analysis complete. Results saved to {output_dir}")

if __name__ == "__main__":
    main()
