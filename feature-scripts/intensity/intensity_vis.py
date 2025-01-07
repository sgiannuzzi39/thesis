import matplotlib.pyplot as plt
import os

generated_results_path = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/intensity/results/generated_intensity_results.txt"
human_results_path = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/intensity/results/human_intensity_results.txt"
output_folder = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/intensity/results"

def parse_sentiment_results(file_path):
    high_positive_scores = []
    high_negative_scores = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            high_positive = 0
            high_negative = 0

            for line in lines:
                if line.startswith("High positive sentiment:"):
                    try:
                        high_positive = int(line.split(":")[1].strip())
                    except ValueError:
                        print(f"Unable to parse positive sentiment from line: {line}")
                elif line.startswith("High negative sentiment:"):
                    try:
                        high_negative = int(line.split(":")[1].strip())
                    except ValueError:
                        print(f"Unable to parse negative sentiment from line: {line}")
                elif line.strip() == "":  
                    high_positive_scores.append(high_positive)
                    high_negative_scores.append(high_negative)
                    high_positive = 0
                    high_negative = 0
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
    return high_positive_scores, high_negative_scores

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
    generated_positive, generated_negative = parse_sentiment_results(generated_results_path)
    human_positive, human_negative = parse_sentiment_results(human_results_path)

    if not generated_positive and not human_positive:
        print("No sentiment scores available to plot.")
        return

    create_boxplot(
        [generated_positive, human_positive],
        ["Generated Stories", "Human Stories"],
        "High Positive Sentiment: Generated vs. Human Stories",
        "High Positive Sentiment Count",
        "high_positive_sentiment_boxplot.png"
    )

    create_boxplot(
        [generated_negative, human_negative],
        ["Generated Stories", "Human Stories"],
        "High Negative Sentiment: Generated vs. Human Stories",
        "High Negative Sentiment Count",
        "high_negative_sentiment_boxplot.png"
    )

    print("Plots generated and saved!")

if __name__ == "__main__":
    main()
