"""
SETUP: conda activate py39
Code co-authored with ChatGPT
"""

import os
from textblob import TextBlob

def analyze_sentiment(file_path):
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

    for sentence in sentences:
        sentiment = sentence.sentiment.polarity
        if sentiment > 0.5:
            high_positive_sentiment += 1
        elif sentiment < -0.5:
            high_negative_sentiment += 1

    return {
        "high_positive_sentiment": high_positive_sentiment,
        "high_negative_sentiment": high_negative_sentiment,
    }

def process_sentiment_directory(directory_path, output_file_path):
    results = []

    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)

        if os.path.isfile(file_path):
            scores = analyze_sentiment(file_path)
            if scores is not None:
                results.append((filename, scores))

    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write("### Sentiment Analysis Results for Each File ###\n\n")
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

    process_sentiment_directory(generated_stories_dir, output_generated)
    process_sentiment_directory(human_stories_dir, output_human)

if __name__ == "__main__":
    main()
