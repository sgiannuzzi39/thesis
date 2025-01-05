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
                if line.startswith("Psychological Intensity:"):
                    score = int(line.split(":")[1].strip())
                    scores.append(score)
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
    return scores

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
        "Psychological Intensity: Generated vs. Human Stories", 
        "Psychological Intensity", 
        "psychological_intensity_boxplot.png"
    )

    print("Plot generated and saved!")

if __name__ == "__main__":
    main()
