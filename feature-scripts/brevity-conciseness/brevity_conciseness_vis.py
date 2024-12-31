import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import numpy as np

# Define file paths for results
human_results_path = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/brevity-conciseness/results/human_results.txt"
generated_results_path = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/brevity-conciseness/results/generated_results.txt"

def parse_results(file_path):
    """
    Parses results from a text file into a structured list of dictionaries.

    Args:
        file_path (str): Path to the results file.

    Returns:
        list: A list of dictionaries, each representing a story's data.
    """
    data = []

    with open(file_path, 'r') as file:
        lines = file.readlines()

        # Initialize variables
        total_words = None
        unnecessary_words = None
        total_characters = None
        sentence_count = None
        pos_counts = {}

        for line in lines:
            if line.startswith("Parts of Speech: "):
                pos_counts = eval(line.replace("Parts of Speech: ", "").strip())
            elif line.startswith("Total words: "):
                total_words = int(line.replace("Total words: ", "").strip())
            elif line.startswith("Unnecessary words: "):
                unnecessary_words = int(line.replace("Unnecessary words: ", "").strip())
            elif line.startswith("Total characters: "):
                total_characters = int(line.replace("Total characters: ", "").strip())
            elif line.startswith("Sentence count: "):
                sentence_count = int(line.replace("Sentence count: ", "").strip())
                # Append data after all metrics are processed
                if all(v is not None for v in [total_words, total_characters, sentence_count]):
                    data.append({
                        "POS Counts": pos_counts,
                        "Total Words": total_words,
                        "Unnecessary Words": unnecessary_words,
                        "Total Characters": total_characters,
                        "Sentence Count": sentence_count
                    })

    return data

def calculate_per_story_averages(data):
    """
    Calculate relative averages per story for selected parts of speech and unnecessary words.

    Args:
        data (list): List of dictionaries containing text analysis data.

    Returns:
        tuple: POS data, word counts, character counts, words per sentence, and unnecessary words.
    """
    pos_data = {"VERB": [], "NOUN": [], "ADJ": [], "ADV": [], "PUNCT": [], "DET": [], "PROPN": [], "ADP": [], "SPACE": [], "SCONJ": [], "PRON": [], "CCONJ": [], "AUX": [], "NUM": [], "PART": []}
    word_counts = []
    character_counts = []
    words_per_sentence = []
    unnecessary_words = []

    for entry in data:
        total_words = entry["Total Words"]
        total_characters = entry["Total Characters"]
        sentence_count = entry["Sentence Count"]
        unnecessary_count = entry["Unnecessary Words"]

        word_counts.append(total_words)
        character_counts.append(total_characters)
        words_per_sentence.append(total_words / sentence_count if sentence_count > 0 else 0)
        unnecessary_words.append((unnecessary_count / total_words) * 100 if total_words > 0 else 0)

        for pos in pos_data.keys():
            pos_data[pos].append((entry["POS Counts"].get(pos, 0) / total_words) * 100 if total_words > 0 else 0)

    return pos_data, word_counts, character_counts, words_per_sentence, unnecessary_words

def create_bar_whisker_plot(data_human, data_generated, label):
    """
    Creates a bar and whisker plot for a specific metric.

    Args:
        data_human (list): List of percentages for human-written works.
        data_generated (list): List of percentages for generated works.
        label (str): The label for the metric to visualize.

    Returns:
        None.
    """
    data = [data_human, data_generated]
    boxprops = dict(facecolor="lightblue", color="black")
    meanprops = dict(marker='o', markerfacecolor='red', markersize=5, linestyle='none', color='red')
    medianprops = dict(color='blue', linewidth=2)

    plt.boxplot(data, labels=["Human", "Generated"], showmeans=True, meanprops=meanprops, medianprops=medianprops, patch_artist=True, boxprops=boxprops)
    plt.title(f"Distribution of {label} (Percentage per Story)")
    plt.ylabel("Percentage")

    # Add a legend for the plot elements
    legend_elements = [
        mpatches.Patch(facecolor='lightblue', edgecolor='black', label='Box (Interquartile Range)'),
        plt.Line2D([0], [0], color='blue', lw=2, label='Median (Blue Line)'),
        plt.Line2D([0], [0], marker='o', color='red', label='Mean (Red Dot)', linestyle='None', markersize=8)
    ]
    plt.legend(handles=legend_elements, loc='upper right')

    plt.tight_layout()
    plt.show()

def create_data_table(data_human, data_generated, human_stats, generated_stats, human_unnecessary, generated_unnecessary):
    """
    Creates and displays a data table comparing human and generated averages for selected POS and other metrics.

    Args:
        data_human (dict): Per-story averages for human-written works.
        data_generated (dict): Per-story averages for generated works.
        human_stats (tuple): Human statistics for word count, character count, and words per sentence.
        generated_stats (tuple): Generated statistics for word count, character count, and words per sentence.
        human_unnecessary (list): List of unnecessary words percentages for human-written works.
        generated_unnecessary (list): List of unnecessary words percentages for generated works.

    Returns:
        None.
    """
    pos_tags = list(data_human.keys())

    human_averages = [np.mean(data_human[pos]) for pos in pos_tags]
    generated_averages = [np.mean(data_generated[pos]) for pos in pos_tags]

    word_count_human, char_count_human, wps_human = human_stats
    word_count_generated, char_count_generated, wps_generated = generated_stats

    data_table = pd.DataFrame({
        "Metric": ["Average Word Count", "Average Character Count", "Average Words per Sentence", "Average Unnecessary Words"] + pos_tags,
        "Human Average": [
            np.mean(word_count_human), np.mean(char_count_human), np.mean(wps_human), np.mean(human_unnecessary)
        ] + human_averages,
        "Generated Average": [
            np.mean(word_count_generated), np.mean(char_count_generated), np.mean(wps_generated), np.mean(generated_unnecessary)
        ] + generated_averages
    })

    print(data_table)
    data_table.to_csv("relative_averages.csv", index=False)

if __name__ == "__main__":
    human_data = parse_results(human_results_path)
    generated_data = parse_results(generated_results_path)

    human_pos_data, human_word_counts, human_char_counts, human_wps, human_unnecessary = calculate_per_story_averages(human_data)
    generated_pos_data, generated_word_counts, generated_char_counts, generated_wps, generated_unnecessary = calculate_per_story_averages(generated_data)

    # Define specific POS tags to visualize
    target_pos_tags = ["VERB", "NOUN", "ADJ", "ADV"]

    # Create bar and whisker plots for target parts of speech
    for pos_tag in target_pos_tags:
        create_bar_whisker_plot(human_pos_data[pos_tag], generated_pos_data[pos_tag], pos_tag)

    # Create bar and whisker plot for unnecessary words
    create_bar_whisker_plot(human_unnecessary, generated_unnecessary, "Unnecessary Words")

    # Create data table for relative averages
    create_data_table(human_pos_data, generated_pos_data, 
                      (human_word_counts, human_char_counts, human_wps), 
                      (generated_word_counts, generated_char_counts, generated_wps),
                      human_unnecessary, generated_unnecessary)
