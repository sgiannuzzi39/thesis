import os
import matplotlib.pyplot as plt

generated_scores_file = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/submerged-identity/results/generated_si_scores.txt"
human_scores_file = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/submerged-identity/results/human_si_scores.txt"
output_folder = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/submerged-identity/results"

def read_scores(file_path):
    scores = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            try:
                _, score = line.rsplit(":", 1)
                scores.append(float(score.strip()))
            except ValueError:
                continue 
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
    generated_scores = read_scores(generated_scores_file)
    human_scores = read_scores(human_scores_file)

    if not generated_scores and not human_scores:
        print("No scores available to plot.")
        return

    data = [generated_scores, human_scores]
    labels = ["Generated Stories", "Human Stories"]

    create_boxplot(
        data, 
        labels, 
        "Submerged Identity Scores: Generated vs. Human Stories", 
        "Submerged Identity Score", 
        "submerged_identity_boxplot.png"
    )

    print("Plot generated and saved!")

if __name__ == "__main__":
    main()
