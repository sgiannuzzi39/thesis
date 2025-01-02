"""
SETUP: conda activate py39
Code co-authored with ChatGPT
"""

import nltk
from nltk.tokenize import sent_tokenize
import os
import spacy
from textblob import TextBlob

# Download necessary NLTK data
nltk.download('punkt')

# Load spaCy model for NER and dependency parsing
nlp = spacy.load("en_core_web_sm")

# Keywords for analysis
mystery_keywords = {"mystery", "secret", "hidden", "unknown", "unseen"}
supernatural_keywords = {"ghost", "spirit", "monster", "witch", "vampire", "zombie"}
deviant_verbs = {"kill", "stab", "laugh", "scream", "attack", "burn", "torture"}

# Main analysis logic with lower psychological intensity threshold

def analyze_file(file_path):
    """Analyze a file for mystery and strangeness metrics."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
    except UnicodeDecodeError:
        print(f"Skipping file due to encoding error: {file_path}")
        return None

    blob = TextBlob(text)
    sentences = blob.sentences

    psychological_intensity = 0
    mystery_score = 0
    supernatural_elements = 0
    deviant_behavior_count = 0

    for sentence in sentences:
        # Sentiment analysis
        sentiment = sentence.sentiment.polarity
        if sentiment < -0.2:  # Reduced threshold
            psychological_intensity += 1

        # Supernatural elements
        doc = nlp(str(sentence))
        for entity in doc.ents:
            if entity.label_ in {"PERSON", "NORP", "ORG", "LOC"} and entity.text.lower() in supernatural_keywords:
                supernatural_elements += 1

        # Deviant behavior
        for token in doc:
            if token.pos_ == "VERB" and token.lemma_.lower() in deviant_verbs:
                deviant_behavior_count += 1

    total_score = psychological_intensity + mystery_score + supernatural_elements + deviant_behavior_count

    return {
        "psychological_intensity": psychological_intensity,
        "mystery_score": mystery_score,
        "supernatural_elements": supernatural_elements,
        "deviant_behavior_count": deviant_behavior_count,
        "total_score": total_score,
    }

def process_directory(directory_path, output_file_path):
    results = []

    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)

        if os.path.isfile(file_path):
            scores = analyze_file(file_path)
            if scores is not None:
                results.append((filename, scores))

    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write("### Analysis Results for Each File ###\n\n")
        for title, scores in results:
            output_file.write(f"Title: {title}\n")
            output_file.write(f"Psychological Intensity: {scores['psychological_intensity']}\n")
            output_file.write(f"Mystery Score: {scores['mystery_score']}\n")
            output_file.write(f"Supernatural Elements: {scores['supernatural_elements']}\n")
            output_file.write(f"Deviant Behavior Count: {scores['deviant_behavior_count']}\n")
            output_file.write(f"Total Score: {scores['total_score']}\n\n")

def main():
    generated_stories_dir = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/generated-stories"
    human_stories_dir = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/human-stories"
    results_dir = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/mystery-strangeness/results"

    os.makedirs(results_dir, exist_ok=True)

    output_generated = os.path.join(results_dir, "generated_analysis_results.txt")
    output_human = os.path.join(results_dir, "human_analysis_results.txt")

    process_directory(generated_stories_dir, output_generated)
    process_directory(human_stories_dir, output_human)

if __name__ == "__main__":
    main()
