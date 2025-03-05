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
    plt.figure(figsize=(8, 6))
    boxprops = dict(facecolor="white", color="black")
    meanprops = dict(marker='D', markerfacecolor='green', markersize=7, linestyle='none', color='green')
    medianprops = dict(color='orange', linewidth=2)

    plt.boxplot(data, labels=labels, patch_artist=True, showmeans=True, 
                meanprops=meanprops, medianprops=medianprops, boxprops=boxprops)

    plt.title(title)
    plt.ylabel(ylabel)

    legend_elements = [
        plt.Line2D([0], [0], color='orange', lw=2, label='Median (Orange Line)'),
        plt.Line2D([0], [0], marker='D', color='green', label='Mean (Green Diamond)', linestyle='None', markersize=8)
    ]
    plt.legend(handles=legend_elements, loc='upper right')

    plt.tight_layout()
    plt.savefig(os.path.join(output_folder, output_filename))
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
