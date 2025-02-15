''' 
    SETUP: conda activate spacy_env
    Code co-authored with ChatGPT

'''

import os
import spacy
import statistics
from collections import Counter

nlp = spacy.load("en_core_web_sm")

def load_text_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def extract_title(text):
    first_line = text.splitlines()[0]
    if first_line.startswith("Title: "):
        return first_line.replace("Title: ", "").strip()
    return "Unknown Title"

def analyze_text(text, unnecessary_words):
    doc = nlp(text)

    unnecessary_word_count = 0
    pos_counts = Counter()
    total_words = 0
    total_characters = len(text)
    sentence_lengths = []
    character_lengths = []
    
    sentences = list(doc.sents)
    sentence_count = len(sentences)
    
    for token in doc:
        if token.text.lower() in unnecessary_words:
            unnecessary_word_count += 1
        pos_counts[token.pos_] += 1
        if token.is_alpha:
            total_words += 1
    
    for sent in sentences:
        words_in_sent = sum(1 for token in sent if token.is_alpha)
        chars_in_sent = sum(len(token.text) for token in sent)
        sentence_lengths.append(words_in_sent)
        character_lengths.append(chars_in_sent)
    
    avg_words_per_sentence = total_words / sentence_count if sentence_count > 0 else 0
    avg_characters_per_sentence = total_characters / sentence_count if sentence_count > 0 else 0
    
    median_words_per_sentence = statistics.median(sentence_lengths) if sentence_lengths else 0
    median_characters_per_sentence = statistics.median(character_lengths) if character_lengths else 0

    return {
        "unnecessary_word_count": unnecessary_word_count,
        "pos_counts": dict(pos_counts),
        "total_words": total_words,
        "total_characters": total_characters,
        "sentence_count": sentence_count,
        "avg_words_per_sentence": avg_words_per_sentence,
        "avg_characters_per_sentence": avg_characters_per_sentence,
        "median_words_per_sentence": median_words_per_sentence,
        "median_characters_per_sentence": median_characters_per_sentence
    }

def analyze_folder(folder_path, unnecessary_words, output_file):
    total_files = 0
    aggregated_metrics = Counter()
    results = []
    median_words_list = []
    median_chars_list = []

    for file_name in os.listdir(folder_path):
        if file_name.endswith(".txt"):
            file_path = os.path.join(folder_path, file_name)
            text = load_text_from_file(file_path)
            title = extract_title(text)

            analysis_result = analyze_text(text, unnecessary_words)

            aggregated_metrics.update(analysis_result["pos_counts"])
            aggregated_metrics["unnecessary_word_count"] += analysis_result["unnecessary_word_count"]
            aggregated_metrics["total_words"] += analysis_result["total_words"]
            aggregated_metrics["total_characters"] += analysis_result["total_characters"]
            aggregated_metrics["sentence_count"] += analysis_result["sentence_count"]
            aggregated_metrics["avg_words_per_sentence"] += analysis_result["avg_words_per_sentence"]
            aggregated_metrics["avg_characters_per_sentence"] += analysis_result["avg_characters_per_sentence"]

            median_words_list.append(analysis_result["median_words_per_sentence"])
            median_chars_list.append(analysis_result["median_characters_per_sentence"])
            total_files += 1

            results.append(f"Title: {title}\n"
                           f"Unnecessary words: {analysis_result['unnecessary_word_count']}\n"
                           f"Parts of Speech: {analysis_result['pos_counts']}\n"
                           f"Total words: {analysis_result['total_words']}\n"
                           f"Total characters: {analysis_result['total_characters']}\n"
                           f"Sentence count: {analysis_result['sentence_count']}\n"
                           f"Avg words per sentence: {analysis_result['avg_words_per_sentence']:.2f}\n"
                           f"Avg characters per sentence: {analysis_result['avg_characters_per_sentence']:.2f}\n"
                           f"Median words per sentence: {analysis_result['median_words_per_sentence']:.2f}\n"
                           f"Median characters per sentence: {analysis_result['median_characters_per_sentence']:.2f}\n\n")
    
    if total_files > 0:
        avg_metrics = {key: value / total_files for key, value in aggregated_metrics.items()}
        overall_median_words = statistics.median(median_words_list) if median_words_list else 0
        overall_median_chars = statistics.median(median_chars_list) if median_chars_list else 0
    else:
        avg_metrics = {key: 0 for key in aggregated_metrics.keys()}
        overall_median_words = 0
        overall_median_chars = 0
    
    with open(output_file, 'w', encoding='utf-8') as output:
        output.write("### Analysis Results for Each File ###\n\n")
        for result in results:
            output.write(result)

        output.write("### Averages Across All Files ###\n\n")
        output.write(f"Average unnecessary words: {avg_metrics['unnecessary_word_count']:.2f}\n")
        output.write(f"Average parts of speech: {dict(avg_metrics)}\n")
        output.write(f"Average words per sentence: {avg_metrics['avg_words_per_sentence']:.2f}\n")
        output.write(f"Average characters per sentence: {avg_metrics['avg_characters_per_sentence']:.2f}\n")
        output.write(f"Median words per sentence: {overall_median_words:.2f}\n")
        output.write(f"Median characters per sentence: {overall_median_chars:.2f}\n")

if __name__ == "__main__":
    human_folder_path = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/human-stories"
    generated_folder_path = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/generated-stories"

    results_folder = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/brevity-conciseness/results"
    os.makedirs(results_folder, exist_ok=True)  

    human_results_file = os.path.join(results_folder, "human_results.txt")
    generated_results_file = os.path.join(results_folder, "generated_results.txt")

    unnecessary_words =     unnecessary_words = [
        # intensifiers and qualifiers
        "very", "really", "just", "quite", "somewhat", "rather", "basically", "actually", "literally",
        "totally", "completely", "absolutely", "definitely", "extremely", "incredibly", "seriously",
        "truly", "simply", "frankly", "honestly", "obviously", "surely", "undoubtedly", "essentially",
        "utterly", "slightly", "relatively", "remarkably", "particularly", "especially", "exceptionally",
        "highly", "awfully", "probably", "certainly", "virtually",

        # redundant phrases
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

        # clichés and overused expressions
        "all of a sudden", "at the end of the day", "back to square one", "beyond a shadow of a doubt",
        "crystal clear", "few and far between", "in a nutshell", "in the nick of time", "last but not least",
        "leaves much to be desired", "needless to say", "nipped in the bud", "only time will tell",
        "read between the lines", "the fact of the matter", "the writing on the wall", "think outside the box",
        "time and time again", "tip of the iceberg", "to make a long story short", "when all is said and done",
        "with all due respect", "without a doubt", "at this juncture", "in light of the fact that",
        "in many cases", "under the circumstances", "with the result that", "in the majority of instances",
        "in view of the fact that", "on the occasion of"
    ]

    print("Analyzing human stories...")
    analyze_folder(human_folder_path, unnecessary_words, human_results_file)

    print("Analyzing generated stories...")
    analyze_folder(generated_folder_path, unnecessary_words, generated_results_file)

    print("Analysis complete! Results saved in:", results_folder)

