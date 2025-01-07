import nltk
from nltk.tokenize import sent_tokenize
import os
from textblob import TextBlob

nltk.download('punkt')

def analyze_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
    except UnicodeDecodeError:
        print(f"Skipping file due to encoding error: {file_path}")
        return None

    blob = TextBlob(text)
    sentences = blob.sentences

    if not sentences:
        print(f"Skipping file due to no valid sentences: {file_path}")
        return None

    total_polarity = sum(sentence.sentiment.polarity for sentence in sentences)
    average_polarity = total_polarity / len(sentences)

    psychological_intensity = -average_polarity * 10 

    return {
        "psychological_intensity": psychological_intensity
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
            output_file.write(f"Psychological Intensity: {scores['psychological_intensity']:.4f}\n\n")

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
