import matplotlib.pyplot as plt
import os

generated_results_path = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/intensity/results/generated_intensity_results.txt"
human_results_path = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/intensity/results/human_intensity_results.txt"
output_folder = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/intensity/results"

def parse_sentiment_results(file_path):
    absolute_sentiment_scores = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

            for line in lines:
                if line.startswith("Total absolute sentiment:"):
                    try:
                        score = float(line.split(":")[1].strip())
                        absolute_sentiment_scores.append(score)
                    except ValueError:
                        print(f"Unable to parse absolute sentiment from line: {line}")
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
    return absolute_sentiment_scores

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
    generated_absolute = parse_sentiment_results(generated_results_path)
    human_absolute = parse_sentiment_results(human_results_path)

    if not generated_absolute and not human_absolute:
        print("No sentiment scores available to plot.")
        return

    create_boxplot(
        [generated_absolute, human_absolute],
        ["Generated Stories", "Human Stories"],
        "Total Intensity: Generated vs. Human Stories",
        "Total Intensity",
        "total_absolute_sentiment_boxplot.png"
    )

    print("Plot generated and saved!")

if __name__ == "__main__":
    main()