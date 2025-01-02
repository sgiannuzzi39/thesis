import matplotlib.pyplot as plt
import os

# Paths to results files
generated_results_path = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/unity-singleeffect/results/generated_results.txt"
human_results_path = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/unity-singleeffect/results/human_results.txt"

def parse_results(file_path):
    """
    Parse the results file to extract TTR, VVI, and Average Paragraph Distance values.
    """
    ttr_values = []
    vvi_values = []
    distance_values = []

    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith("TTR:"):
                ttr_values.append(float(line.split()[1]))
            elif line.startswith("VVI:"):
                vvi_values.append(float(line.split()[1]))
            elif line.startswith("Average Paragraph Distance:"):
                distance_values.append(float(line.split()[3]))

    return ttr_values, vvi_values, distance_values

def create_boxplot(data, labels, title, ylabel, output_path):
    """
    Create a box-and-whisker plot.
    """
    plt.figure(figsize=(8, 6))
    box = plt.boxplot(data, labels=labels, patch_artist=True, showmeans=True, 
                      meanprops=dict(linestyle='-', color='orange', linewidth=2), 
                      flierprops=dict(marker='^', color='green', alpha=0.5))

    # Customize box colors
    colors = ['lightblue', 'lightgreen']
    for patch, color in zip(box['boxes'], colors):
        patch.set_facecolor(color)

    plt.title(title)
    plt.ylabel(ylabel)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Add a legend
    plt.legend([
        plt.Line2D([0], [0], color='lightblue', lw=4),
        plt.Line2D([0], [0], color='lightgreen', lw=4),
        plt.Line2D([0], [0], color='orange', linestyle='-', lw=2),
        plt.Line2D([0], [0], color='green', marker='^', linestyle='', markersize=8, alpha=0.5),
        plt.Line2D([0], [0], color='grey', marker='^', linestyle='', markersize=8, alpha=0.5)
    ], 
               ["Generated", "Human", "Mean (Orange Line)", "Outlier (Green Triangle)", "Default Outlier (Grey Triangle)"], loc='upper right')

    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def main():
    # Parse results
    generated_ttr, generated_vvi, generated_distances = parse_results(generated_results_path)
    human_ttr, human_vvi, human_distances = parse_results(human_results_path)

    # Data for plots
    ttr_data = [generated_ttr, human_ttr]
    vvi_data = [generated_vvi, human_vvi]
    distance_data = [generated_distances, human_distances]

    # Labels for the plots
    labels = ["Generated", "Human"]

    # Create TTR plot
    create_boxplot(
        ttr_data, 
        labels, 
        "TTR: Generated vs. Human Stories", 
        "Type-Token Ratio (TTR)", 
        "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/unity-singleeffect/results/ttr_boxplot.png"
    )

    # Create VVI plot
    create_boxplot(
        vvi_data, 
        labels, 
        "VVI: Generated vs. Human Stories", 
        "Verbal Variety Index (VVI)", 
        "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/unity-singleeffect/results/vvi_boxplot.png"
    )

    # Create Average Paragraph Distance plot
    create_boxplot(
        distance_data, 
        labels, 
        "Average Paragraph Distance: Generated vs. Human Stories", 
        "Average Euclidean Distance", 
        "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/unity-singleeffect/results/distance_boxplot.png"
    )

    print("Plots generated and saved!")

if __name__ == "__main__":
    main()
