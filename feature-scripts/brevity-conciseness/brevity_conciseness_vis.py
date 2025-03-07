''' 
    SETUP: conda activate spacy_env
    Code co-authored with ChatGPT

'''

import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import numpy as np
import statistics

human_results_path = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/brevity-conciseness/results/human_results.txt"
generated_results_path = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/brevity-conciseness/results/generated_results.txt"
output_folder = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/brevity-conciseness/results"

def calculate_median(values):
    return statistics.median(values) if values else 0

def parse_results(file_path):
    data = {
        "Total words": [],
        "Total characters": [],
        "Avg words per sentence": [],
        "Avg characters per sentence": [],
        "Median words per sentence": [],
        "Median characters per sentence": [],
        "Unnecessary words": []
    }

    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return data  

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

        for line in lines:
            if line.startswith("Total words:"):
                data["Total words"].append(int(line.split(":")[1].strip()))
            elif line.startswith("Total characters:"):
                data["Total characters"].append(int(line.split(":")[1].strip()))
            elif line.startswith("Avg words per sentence:"):
                data["Avg words per sentence"].append(float(line.split(":")[1].strip()))
            elif line.startswith("Avg characters per sentence:"):
                data["Avg characters per sentence"].append(float(line.split(":")[1].strip()))
            elif line.startswith("Median words per sentence:"):
                data["Median words per sentence"].append(float(line.split(":")[1].strip()))
            elif line.startswith("Median characters per sentence:"):
                data["Median characters per sentence"].append(float(line.split(":")[1].strip()))
            elif line.startswith("Unnecessary words:"):
                data["Unnecessary words"].append(int(line.split(":")[1].strip()))

    return data

def create_bar_whisker_plot(data_human, data_generated, label, output_filename):
    data = [data_human, data_generated]
    boxprops = dict(facecolor="white", color="black")
    meanprops = dict(marker='D', markerfacecolor='green', markersize=7, linestyle='none', color='green')
    medianprops = dict(color='orange', linewidth=2)

    plt.figure(figsize=(8, 6))
    plt.boxplot(data, labels=["Human", "Generated"], showmeans=True, meanprops=meanprops, medianprops=medianprops, patch_artist=True, boxprops=boxprops)
    plt.title(f"Distribution of {label} (Per Story)")
    plt.ylabel("Value")

    legend_elements = [
        mpatches.Patch(facecolor='white', edgecolor='black', label='Box (Interquartile Range)'),
        plt.Line2D([0], [0], color='orange', lw=2, label='Median (Orange Line)'),
        plt.Line2D([0], [0], marker='D', color='green', label='Mean (Green Diamond)', linestyle='None', markersize=8)
    ]
    plt.legend(handles=legend_elements, loc='upper right')

    plt.tight_layout()
    plt.savefig(os.path.join(output_folder, output_filename))
    plt.close()

def create_data_table(human_data, generated_data):
    metrics = list(human_data.keys())

    human_averages = [np.mean(human_data[metric]) if human_data[metric] else 0 for metric in metrics]
    human_medians = [calculate_median(human_data[metric]) if human_data[metric] else 0 for metric in metrics]
    generated_averages = [np.mean(generated_data[metric]) if generated_data[metric] else 0 for metric in metrics]
    generated_medians = [calculate_median(generated_data[metric]) if generated_data[metric] else 0 for metric in metrics]

    data_table = pd.DataFrame({
        "Metric": metrics,
        "Human Average": human_averages,
        "Human Median": human_medians,
        "Generated Average": generated_averages,
        "Generated Median": generated_medians,
    })

    print("Generated Data Table:")
    print(data_table.to_string(index=False))

    data_table.to_csv(os.path.join(output_folder, "relative_averages.csv"), index=False)

if __name__ == "__main__":
    print("Starting visualization script...")

    human_data = parse_results(human_results_path)
    generated_data = parse_results(generated_results_path)

    if not human_data["Total words"] or not generated_data["Total words"]:
        print("⚠️ No valid data found in one or both results files. Exiting.")
        exit()

    print("Data successfully parsed!")

    create_data_table(human_data, generated_data)

    print("Data table created!")

    print("Generating plots...")
    create_bar_whisker_plot(human_data["Total words"], generated_data["Total words"], "Word Count", "word_count_distribution.png")
    create_bar_whisker_plot(human_data["Total characters"], generated_data["Total characters"], "Character Count", "character_count_distribution.png")
    create_bar_whisker_plot(human_data["Avg words per sentence"], generated_data["Avg words per sentence"], "Words per Sentence", "words_per_sentence_distribution.png")
    create_bar_whisker_plot(human_data["Unnecessary words"], generated_data["Unnecessary words"], "Unnecessary Words", "unnecessary_words_distribution.png")

    print("Visualizations saved in", output_folder)
