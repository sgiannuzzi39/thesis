import matplotlib.pyplot as plt
import os

# File paths
generated_event_file = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/focused-character-event/results/generated_event_results.txt"
human_event_file = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/focused-character-event/results/human_event_results.txt"
generated_character_file = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/focused-character-event/results/generated_character_results.txt"
human_character_file = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/focused-character-event/results/human_character_results.txt"
output_folder = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/focused-character-event/results"

def parse_results(file_path, score_type):
    """Parse results from a plain text file and extract scores for the specified type."""
    scores = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line in lines:
                if line.startswith(f"{score_type} Score:"):
                    try:
                        score = float(line.split(":")[1].strip())
                        scores.append(score)
                    except ValueError:
                        print(f"Unable to parse score from line: {line}")
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
    return scores

def create_boxplot(data, labels, title, ylabel, output_filename):
    """Create a box-and-whisker plot."""
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
    # Parse scores for events
    generated_event_scores = parse_results(generated_event_file, "Focused Event")
    human_event_scores = parse_results(human_event_file, "Focused Event")

    # Parse scores for characters
    generated_character_scores = parse_results(generated_character_file, "Focused Character")
    human_character_scores = parse_results(human_character_file, "Focused Character")

    if not generated_event_scores and not human_event_scores:
        print("No event scores available to plot.")
    else:
        # Create Focused Event plot
        create_boxplot(
            [generated_event_scores, human_event_scores], 
            ["Generated Stories", "Human Stories"], 
            "Focused Event Scores: Generated vs. Human Stories", 
            "Focused Event Score", 
            "focused_event_boxplot.png"
        )

    if not generated_character_scores and not human_character_scores:
        print("No character scores available to plot.")
    else:
        # Create Focused Character plot
        create_boxplot(
            [generated_character_scores, human_character_scores], 
            ["Generated Stories", "Human Stories"], 
            "Focused Character Scores: Generated vs. Human Stories", 
            "Focused Character Score", 
            "focused_character_boxplot.png"
        )

    print("Plots generated and saved!")

if __name__ == "__main__":
    main()