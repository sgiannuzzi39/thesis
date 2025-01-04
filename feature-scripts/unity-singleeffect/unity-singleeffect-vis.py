import matplotlib.pyplot as plt
import os

# Paths to results files
generated_results_path = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/unity-singleeffect/results/generated_results.txt"
human_results_path = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/unity-singleeffect/results/human_results.txt"
output_folder = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/unity-singleeffect/results"

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

def create_boxplot(data, labels, title, ylabel, output_filename):
    """
    Create a box-and-whisker plot.
    """
    plt.figure(figsize=(8, 6))
    boxprops = dict(facecolor="white", color="black")
    meanprops = dict(marker='D', markerfacecolor='green', markersize=7, linestyle='none', color='green')
    medianprops = dict(color='orange', linewidth=2)

    plt.boxplot(data, labels=labels, patch_artist=True, showmeans=True, 
                meanprops=meanprops, medianprops=medianprops, boxprops=boxprops)

    plt.title(title)
    plt.ylabel(ylabel)

    # Add a legend
    legend_elements = [
        plt.Line2D([0], [0], color='orange', lw=2, label='Median (Orange Line)'),
        plt.Line2D([0], [0], marker='D', color='green', label='Mean (Green Diamond)', linestyle='None', markersize=8)
    ]
    plt.legend(handles=legend_elements, loc='upper right')

    plt.tight_layout()
    plt.savefig(os.path.join(output_folder, output_filename))
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
        "ttr_boxplot.png"
    )

    # Create VVI plot
    create_boxplot(
        vvi_data, 
        labels, 
        "VVI: Generated vs. Human Stories", 
        "Verbal Variety Index (VVI)", 
        "vvi_boxplot.png"
    )

    # Create Average Paragraph Distance plot
    create_boxplot(
        distance_data, 
        labels, 
        "Average Paragraph Distance: Generated vs. Human Stories", 
        "Average Euclidean Distance", 
        "distance_boxplot.png"
    )

    print("Plots generated and saved!")

if __name__ == "__main__":
    main()
