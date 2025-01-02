import matplotlib.pyplot as plt
import os

def parse_results(file_path):
    """Parse results from a plain text file and extract psychological_intensity scores."""
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

def create_boxplot(generated_scores, human_scores, output_path):
    """Create a box-and-whisker plot comparing psychological_intensity scores."""
    data = [generated_scores, human_scores]
    labels = ['Generated Stories', 'Human Stories']
    
    plt.figure(figsize=(8, 6))
    plt.boxplot(data, labels=labels, patch_artist=True, showmeans=True)
    plt.title("Psychological Intensity Scores: Generated vs. Human Stories")
    plt.ylabel("Psychological Intensity")
    plt.grid(axis='y')
    plt.savefig(output_path)
    plt.show()

def main():
    generated_file = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/mystery-strangeness/results/generated_analysis_results.txt"
    human_file = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/mystery-strangeness/results/human_analysis_results.txt"
    output_path = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/mystery-strangeness/results/psychological_intensity_boxplot.png"
    
    # Parse scores
    generated_scores = parse_results(generated_file)
    human_scores = parse_results(human_file)
    
    if not generated_scores and not human_scores:
        print("No scores available to plot.")
        return
    
    # Create and save the plot
    create_boxplot(generated_scores, human_scores, output_path)

if __name__ == "__main__":
    main()
