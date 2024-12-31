''' 
    SETUP: conda activate spacy_env
    Code co-authored with ChatGPT

'''
import os
import spacy
from collections import Counter

# Load the spaCy English model globally
nlp = spacy.load("en_core_web_sm")

def load_text_from_file(file_path):
    """
    Loads the text from an external .txt file.

    Args:
        file_path (str): Path to the .txt file.

    Returns:
        str: Content of the file as a string.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def extract_title(text):
    """
    Extracts the title from the first line of the text file.

    Args:
        text (str): The content of the text file.

    Returns:
        str: The title of the story (extracted from the first line).
    """
    first_line = text.splitlines()[0]
    if first_line.startswith("Title: "):
        return first_line.replace("Title: ", "").strip()
    else:
        return "Unknown Title"

def analyze_text(text, unnecessary_words):
    """
    Analyzes the text to count unnecessary words, parts of speech, total words, total characters, and sentences.

    Args:
        text (str): The input text.
        unnecessary_words (list): List of unnecessary words.

    Returns:
        dict: A dictionary containing counts of various metrics.
    """
    doc = nlp(text)

    unnecessary_word_count = 0
    pos_counts = Counter()
    sentence_count = len(list(doc.sents))
    total_words = 0
    total_characters = len(text)

    for token in doc:
        if token.text.lower() in unnecessary_words:
            unnecessary_word_count += 1
        pos_counts[token.pos_] += 1
        if token.is_alpha:
            total_words += 1

    avg_words_per_sentence = total_words / sentence_count if sentence_count > 0 else 0
    avg_characters_per_sentence = total_characters / sentence_count if sentence_count > 0 else 0

    return {
        "unnecessary_word_count": unnecessary_word_count,
        "pos_counts": dict(pos_counts),
        "total_words": total_words,
        "total_characters": total_characters,
        "sentence_count": sentence_count,
        "avg_words_per_sentence": avg_words_per_sentence,
        "avg_characters_per_sentence": avg_characters_per_sentence
    }

def analyze_folder(folder_path, unnecessary_words, output_file):
    """
    Analyzes all .txt files in the specified folder and writes results to an output text file.

    Args:
        folder_path (str): Path to the folder containing the .txt files.
        unnecessary_words (list): List of unnecessary words to count.
        output_file (str): Path to the output file where results will be saved.
    """
    total_files = 0
    aggregated_metrics = Counter()
    results = []

    for file_name in os.listdir(folder_path):
        if file_name.endswith(".txt"):
            file_path = os.path.join(folder_path, file_name)
            text = load_text_from_file(file_path)
            title = extract_title(text)

            # Analyze the text
            analysis_result = analyze_text(text, unnecessary_words)

            # Aggregate totals for averaging later
            aggregated_metrics.update(analysis_result["pos_counts"])
            aggregated_metrics["unnecessary_word_count"] += analysis_result["unnecessary_word_count"]
            aggregated_metrics["total_words"] += analysis_result["total_words"]
            aggregated_metrics["total_characters"] += analysis_result["total_characters"]
            aggregated_metrics["sentence_count"] += analysis_result["sentence_count"]
            aggregated_metrics["avg_words_per_sentence"] += analysis_result["avg_words_per_sentence"]
            aggregated_metrics["avg_characters_per_sentence"] += analysis_result["avg_characters_per_sentence"]
            total_files += 1

            # Add individual file's results to the list
            results.append(f"Title: {title}\n"
                           f"Unnecessary words: {analysis_result['unnecessary_word_count']}\n"
                           f"Parts of Speech: {analysis_result['pos_counts']}\n"
                           f"Total words: {analysis_result['total_words']}\n"
                           f"Total characters: {analysis_result['total_characters']}\n"
                           f"Sentence count: {analysis_result['sentence_count']}\n"
                           f"Avg words per sentence: {analysis_result['avg_words_per_sentence']:.2f}\n"
                           f"Avg characters per sentence: {analysis_result['avg_characters_per_sentence']:.2f}\n\n")

    # Calculate averages across all files
    if total_files > 0:
        avg_metrics = {key: value / total_files for key, value in aggregated_metrics.items()}
    else:
        avg_metrics = {key: 0 for key in aggregated_metrics.keys()}

    # Write the results to the output file
    with open(output_file, 'w', encoding='utf-8') as output:
        output.write("### Analysis Results for Each File ###\n\n")
        for result in results:
            output.write(result)

        # Write averages at the end
        output.write("### Averages Across All Files ###\n\n")
        output.write(f"Average unnecessary words: {avg_metrics['unnecessary_word_count']:.2f}\n")
        output.write(f"Average parts of speech: {dict(avg_metrics)}\n")
        output.write(f"Average words per sentence: {avg_metrics['avg_words_per_sentence']:.2f}\n")
        output.write(f"Average characters per sentence: {avg_metrics['avg_characters_per_sentence']:.2f}\n")

if __name__ == "__main__":
    # Specify folders and output files for human-written and generated stories
    human_folder_path = "human-stories/"
    generated_folder_path = "generated-stories/"
    unnecessary_words = [
        # Intensifiers and qualifiers
        "very", "really", "just", "quite", "somewhat", "rather", "basically", "actually", "literally",
        "totally", "completely", "absolutely", "definitely", "extremely", "incredibly", "seriously",
        "truly", "simply", "frankly", "honestly", "obviously", "surely", "undoubtedly", "essentially",
        "utterly", "slightly", "relatively", "remarkably", "particularly", "especially", "exceptionally",
        "highly", "awfully", "probably", "certainly", "virtually",

        # Redundant phrases
        "end result", "added bonus", "free gift", "past history", "future plans", "unexpected surprise",
        "advance warning", "basic fundamentals", "final outcome", "completely finished",
        "absolutely essential", "each and every", "first and foremost", "in order to",
        "at this point in time", "due to the fact that", "in the event that", "with the exception of",
        "despite the fact that", "for the purpose of", "in the near future", "on a daily basis",
        "at this moment in time", "until such time as", "whether or not", "as a matter of fact",
        "by means of", "for the most part", "in the process of", "in the vicinity of", "on account of",
        "with regard to", "with respect to", "at all times", "for the duration of", "in the meantime",
        "in the neighborhood of", "in the course of", "in the final analysis", "in the midst of",
        "in the not-too-distant future", "on the grounds that", "under the circumstances",
        "with the result that", "in the majority of instances", "in view of the fact that",
        "on the occasion of",

        # Clichés and overused expressions
        "all of a sudden", "at the end of the day", "back to square one", "beyond a shadow of a doubt",
        "crystal clear", "few and far between", "in a nutshell", "in the nick of time", "last but not least",
        "leaves much to be desired", "needless to say", "nipped in the bud", "only time will tell",
        "read between the lines", "the fact of the matter", "the writing on the wall", "think outside the box",
        "time and time again", "tip of the iceberg", "to make a long story short", "when all is said and done",
        "with all due respect", "without a doubt", "at this juncture", "in light of the fact that",
        "in many cases", "under the circumstances", "with the result that", "in the majority of instances",
        "in view of the fact that", "on the occasion of"
    ]

    analyze_folder(human_folder_path, unnecessary_words, "brevity-conciseness/results/human_results.txt")
    analyze_folder(generated_folder_path, unnecessary_words, "brevity-conciseness/results/generated_results.txt")
