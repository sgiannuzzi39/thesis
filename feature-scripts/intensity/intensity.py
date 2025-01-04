"""
SETUP: conda activate py39
Code co-authored with ChatGPT
"""

import os
from textblob import TextBlob
import spacy
from collections import Counter

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Define dynamic and emotive keywords
dynamic_keywords = {"roaring", "exploded", "burst", "shattered", "intense", "screamed", "whispered"}
emotive_phrases = {"oh my god", "unbelievable", "incredible", "heartbreaking", "overjoyed"}

def analyze_intensity(file_path):
    """Analyze a file for general intensity metrics."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
    except UnicodeDecodeError:
        print(f"Skipping file due to encoding error: {file_path}")
        return None

    blob = TextBlob(text)
    sentences = blob.sentences

    high_positive_sentiment = 0
    high_negative_sentiment = 0
    dynamic_language_count = 0
    emotive_expression_count = 0
    lexical_variety_score = 0

    all_words = []

    for sentence in sentences:
        # Sentiment analysis
        sentiment = sentence.sentiment.polarity
        if sentiment > 0.5:
            high_positive_sentiment += 1
        elif sentiment < -0.5:
            high_negative_sentiment += 1

        # Dynamic language and emotive expressions
        doc = nlp(str(sentence))
        sentence_lower = str(sentence).lower()

        dynamic_language_count += sum(1 for token in doc if token.lemma_.lower() in dynamic_keywords)
        emotive_expression_count += sum(1 for phrase in emotive_phrases if phrase in sentence_lower)

        # Collect words for lexical variety
        all_words.extend([token.text.lower() for token in doc if token.is_alpha])

    # Lexical variety: unique words relative to total words
    lexical_variety_score = len(set(all_words)) / len(all_words) if all_words else 0

    total_intensity_score = (
        high_positive_sentiment
        + high_negative_sentiment
        + dynamic_language_count
        + emotive_expression_count
        + (lexical_variety_score * 10)  # Scale lexical variety for contribution
    )

    return {
        "high_positive_sentiment": high_positive_sentiment,
        "high_negative_sentiment": high_negative_sentiment,
        "dynamic_language_count": dynamic_language_count,
        "emotive_expression_count": emotive_expression_count,
        "lexical_variety_score": round(lexical_variety_score, 2),
        "total_intensity_score": round(total_intensity_score, 2),
    }

def process_intensity_directory(directory_path, output_file_path):
    """Process all files in a directory and compute intensity metrics."""
    results = []

    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)

        if os.path.isfile(file_path):
            scores = analyze_intensity(file_path)
            if scores is not None:
                results.append((filename, scores))

    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write("### Intensity Analysis Results for Each File ###\n\n")
        for title, scores in results:
            output_file.write(f"Title: {title}\n")
            for metric, value in scores.items():
                output_file.write(f"{metric.replace('_', ' ').capitalize()}: {value}\n")
            output_file.write("\n")

def main():
    generated_stories_dir = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/generated-stories"
    human_stories_dir = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/human-stories"
    results_dir = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/intensity/results"

    os.makedirs(results_dir, exist_ok=True)

    output_generated = os.path.join(results_dir, "generated_intensity_results.txt")
    output_human = os.path.join(results_dir, "human_intensity_results.txt")

    process_intensity_directory(generated_stories_dir, output_generated)
    process_intensity_directory(human_stories_dir, output_human)

if __name__ == "__main__":
    main()
