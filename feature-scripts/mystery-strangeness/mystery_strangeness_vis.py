"""
Code co-authored with ChatGPT
"""

import matplotlib.pyplot as plt
import os

generated_results_path = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/mystery-strangeness/results/generated_analysis_results.txt"
human_results_path = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/mystery-strangeness/results/human_analysis_results.txt"
output_folder = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/mystery-strangeness/results"

def parse_results(file_path):
    scores = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line in lines:
                if line.startswith("Normalized Mystery and Strangeness Score:"):
                    score = float(line.split(":")[1].strip())
                    scores.append(score)
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
    return scores

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
    generated_scores = parse_results(generated_results_path)
    human_scores = parse_results(human_results_path)

    if not generated_scores and not human_scores:
        print("No scores available to plot.")
        return

    data = [generated_scores, human_scores]
    labels = ["Generated Stories", "Human Stories"]

    create_boxplot(
        data, 
        labels, 
        "Mystery and Strangeness: Generated vs. Human Stories", 
        "Normalized Absolute Negative Sentiment Score", 
        "mystery_and_strangeness_boxplot.png"
    )

    print("Plot generated and saved!")

if __name__ == "__main__":
    main()
