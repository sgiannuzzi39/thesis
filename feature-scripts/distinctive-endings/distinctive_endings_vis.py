import matplotlib.pyplot as plt
import os

def parse_results(file_path):
    """Parse results from a plain text file and extract minimum change scores."""
    scores = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line in lines:
                if line.startswith("Min Change:"):
                    try:
                        score = float(line.split(":")[1].strip())
                        scores.append(score)
                    except ValueError:
                        print(f"Unable to parse score from line: {line}")
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
    return scores

def create_boxplot(generated_scores, human_scores, output_path):
    """Create a box-and-whisker plot comparing minimum change scores."""
    data = [generated_scores, human_scores]
    labels = ['Generated Stories', 'Human Stories']

    plt.figure(figsize=(8, 6))
    plt.boxplot(data, labels=labels, patch_artist=True, showmeans=True)
    plt.title("Minimum Change Scores: Generated vs. Human Stories")
    plt.ylabel("Minimum Change Score")
    plt.grid(axis='y')
    plt.savefig(output_path)
    plt.show()

def main():
    generated_file = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/distinctive-endings/results/generated_endings_results.txt"
    human_file = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/distinctive-endings/results/human_endings_results.txt"
    output_path = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/distinctive-endings/results/min_change_boxplot.png"

    # Parse scores
    generated_scores = parse_results(generated_file)
    human_scores = parse_results(human_file)

    if not generated_scores and not human_scores:
        print("No scores available to plot.")
        return

    # Debugging: Print parsed scores
    print("Generated Scores:", generated_scores)
    print("Human Scores:", human_scores)

    # Create and save the plot
    create_boxplot(generated_scores, human_scores, output_path)

if __name__ == "__main__":
    main()
