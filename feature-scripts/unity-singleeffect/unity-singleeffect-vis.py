import matplotlib.pyplot as plt
import os

generated_results_path = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/unity-singleeffect/results/generated_results.txt"
human_results_path = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/unity-singleeffect/results/human_results.txt"
output_folder = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/unity-singleeffect/results"

def parse_results(file_path):
    vvi_values = []

    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith("VVI:"):
                vvi_values.append(float(line.split()[1]))

    return vvi_values

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
    generated_vvi = parse_results(generated_results_path)
    human_vvi = parse_results(human_results_path)

    vvi_data = [generated_vvi, human_vvi]

    labels = ["Generated", "Human"]

    create_boxplot(
        vvi_data, 
        labels, 
        "VVI: Generated vs. Human Stories", 
        "VVI: Weighted Lexical Diversity Score", 
        "vvi_boxplot.png"
    )

    print("VVI plot generated and saved!")

if __name__ == "__main__":
    main()
