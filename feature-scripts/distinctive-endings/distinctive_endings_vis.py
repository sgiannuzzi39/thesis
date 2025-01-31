import matplotlib.pyplot as plt
import os
import numpy as np

# File paths
generated_results_path = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/distinctive-endings/results/generated_quarters_results.txt"
human_results_path = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/distinctive-endings/results/human_quarters_results.txt"
output_folder = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/distinctive-endings/results"

def parse_results(file_path):
    quarter_scores = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            current_story_scores = []
            
            for line in lines:
                if line.startswith("Quarter") and "WMD" in line:
                    try:
                        score = float(line.split("=")[1].strip())
                        current_story_scores.append(score)
                    except ValueError:
                        print(f"Unable to parse WMD score from line: {line}")
                elif line.startswith("Title:") and current_story_scores:
                    if len(quarter_scores) < len(current_story_scores):
                        quarter_scores.extend([[] for _ in range(len(current_story_scores) - len(quarter_scores))])
                    for i, score in enumerate(current_story_scores):
                        quarter_scores[i].append(score)
                    current_story_scores = []
            
            if current_story_scores:
                if len(quarter_scores) < len(current_story_scores):
                    quarter_scores.extend([[] for _ in range(len(current_story_scores) - len(quarter_scores))])
                for i, score in enumerate(current_story_scores):
                    quarter_scores[i].append(score)
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
    
    return [np.mean(q) for q in quarter_scores] if quarter_scores else []

def plot_average_wmd(generated_avg, human_avg, output_filename):
    plt.figure(figsize=(10, 6))
    x_labels = ["WMD between Quarter 1 & 2", "WMD between Quarter 2 & 3", "WMD between Quarter 3 & 4"]
    x_positions = range(1, len(generated_avg) + 1)
    
    plt.plot(x_positions, generated_avg, marker='o', label="Generated Stories")
    plt.plot(x_positions, human_avg, marker='s', label="Human Stories")
    
    plt.xticks(x_positions, x_labels)
    plt.title("Average WMD Scores per Quarter Transition")
    plt.xlabel("Quarter Transitions")
    plt.ylabel("Average WMD Score")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_folder, output_filename))
    plt.close()

def main():
    generated_avg = parse_results(generated_results_path)
    human_avg = parse_results(human_results_path)
    
    if not generated_avg or not human_avg:
        print("No scores available to plot.")
        return
    
    plot_average_wmd(generated_avg, human_avg, "average_wmd_comparison.png")
    print("Average WMD comparison graph generated and saved!")

if __name__ == "__main__":
    main()
