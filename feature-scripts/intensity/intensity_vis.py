"""
Code co-authored with ChatGPT
"""

import matplotlib.pyplot as plt
import os

generated_results_path = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/intensity/results/generated_intensity_results.txt"
human_results_path = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/intensity/results/human_intensity_results.txt"
output_folder = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/intensity/results"

def parse_sentiment_results(file_path):
    normalized_sentiment_scores = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line in lines:
                if line.startswith("Normalized absolute sentiment:"):
                    try:
                        score = float(line.split(":")[1].strip())
                        normalized_sentiment_scores.append(score)
                    except ValueError:
                        print(f"Unable to parse normalized sentiment from line: {line}")
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
    return normalized_sentiment_scores

def create_boxplot(data, labels, title, ylabel, output_filename):
    plt.figure(figsize=(10, 7), dpi=300) 
    boxprops = dict(facecolor="lightgray", color="black", linewidth=1.5)
    meanprops = dict(marker='D', markerfacecolor='blue', markersize=8, linestyle='none', color='blue')
    medianprops = dict(color='red', linewidth=2)
    whiskerprops = dict(color="black", linewidth=1.5)
    capprops = dict(color="black", linewidth=1.5)

    plt.boxplot(
        data, labels=labels, patch_artist=True, showmeans=True, 
        meanprops=meanprops, medianprops=medianprops, 
        boxprops=boxprops, whiskerprops=whiskerprops, capprops=capprops
    )

    plt.ylim(0, 0.6)  
    
    plt.title(title, fontsize=14, fontweight='bold')
    plt.ylabel(ylabel, fontsize=12)
    
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    legend_elements = [
        plt.Line2D([0], [0], color='red', lw=2, label='Median (Red Line)'),
        plt.Line2D([0], [0], marker='D', color='blue', label='Mean (Blue Diamond)', linestyle='None', markersize=8)
    ]
    plt.legend(handles=legend_elements, loc='upper right')

    plt.tight_layout()
    plt.savefig(os.path.join(output_folder, output_filename), dpi=300)
    plt.close()

def main():
    generated_normalized = parse_sentiment_results(generated_results_path)
    human_normalized = parse_sentiment_results(human_results_path)

    if not generated_normalized and not human_normalized:
        print("No sentiment scores available to plot.")
        return

    create_boxplot(
        [generated_normalized, human_normalized],
        ["Generated Stories", "Human Stories"],
        "Normalized Sentiment Intensity: Generated vs. Human Stories",
        "Normalized Absolute Value Sentiment Scores",
        "normalized_absolute_sentiment_boxplot.png"
    )

    print("Plot generated and saved!")

if __name__ == "__main__":
    main()
