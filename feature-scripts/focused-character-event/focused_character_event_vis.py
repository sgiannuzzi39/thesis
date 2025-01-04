import matplotlib.pyplot as plt
import os

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

def create_boxplot(generated_scores, human_scores, output_path, title, ylabel):
    """Create a box-and-whisker plot comparing scores."""
    data = [generated_scores, human_scores]
    labels = ['Generated Stories', 'Human Stories']

    plt.figure(figsize=(8, 6))
    plt.boxplot(data, labels=labels, patch_artist=True, showmeans=True)
    plt.title(title)
    plt.ylabel(ylabel)
    plt.grid(axis='y')
    plt.savefig(output_path)
    plt.show()

def main():
    # File paths
    generated_event_file = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/focused-character-event/results/generated_event_results.txt"
    human_event_file = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/focused-character-event/results/human_event_results.txt"
    output_path = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/focused-character-event/results/focused_event_boxplot.png"

    # Parse scores
    generated_scores = parse_results(generated_event_file, "Focused Event")
    human_scores = parse_results(human_event_file, "Focused Event")

    if not generated_scores and not human_scores:
        print("No scores available to plot.")
        return

    # Debugging: Print parsed scores
    print("Generated Scores:", generated_scores)
    print("Human Scores:", human_scores)

    # Create and save the plot
    create_boxplot(
        generated_scores,
        human_scores,
        output_path,
        "Focused Event Scores: Generated vs. Human Stories",
        "Focused Event Score"
    )

if __name__ == "__main__":
    main()
