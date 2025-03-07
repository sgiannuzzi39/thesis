"""
Code co-authored with ChatGPT
"""
import matplotlib.pyplot as plt
import os

generated_results_path = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/unity-singleeffect/results/generated_results.txt"
human_results_path = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/unity-singleeffect/results/human_results.txt"
output_folder = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/unity-singleeffect/results"

def parse_results(file_path):
    ttr_values = []
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith("Moving TTR:"):
                tokens = line.split()
                ttr_values.append(float(tokens[2]))
    return ttr_values

def create_boxplot(data, labels, title, ylabel, output_filename):
    plt.figure(figsize=(10, 7), dpi=300) 
    
    boxprops = dict(facecolor="lightgray", color="black", linewidth=1.5)
    medianprops = dict(color='red', linewidth=2)
    meanprops = dict(marker='D', markerfacecolor='blue', markersize=8, linestyle='none', color='blue')
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
    generated_ttr = parse_results(generated_results_path)
    human_ttr = parse_results(human_results_path)

    ttr_data = [generated_ttr, human_ttr]
    labels = ["Generated", "Human"]

    create_boxplot(
        ttr_data, 
        labels, 
        "Moving-Average TTR: Generated vs. Human Stories", 
        "Moving-Average Type-Token Ratio", 
        "ttr_boxplot.png"
    )

    print("TTR plot generated and saved!")

if __name__ == "__main__":
    main()
