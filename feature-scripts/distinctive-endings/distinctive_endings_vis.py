import matplotlib.pyplot as plt
import os

generated_results_path = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/distinctive-endings/results/generated_quarters_results.txt"
human_results_path = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/distinctive-endings/results/human_quarters_results.txt"
output_folder = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/distinctive-endings/results"

def parse_results(file_path):
    story_scores = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            current_story_scores = []

            for line in lines:
                if line.startswith("Quarter") and "WMD" in line:
                    try:
                        score = float(line.split("=")[1].strip())
                        current_story_scores.append(score)
                    except ValueError:
                        print(f"Unable to parse WMD score from line: {line}")
                elif line.startswith("Title:") and current_story_scores:
                    story_scores.append(current_story_scores)
                    current_story_scores = []

            if current_story_scores:
                story_scores.append(current_story_scores)
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")

    return story_scores

def create_line_graph(story_scores, title, ylabel, output_filename):
    plt.figure(figsize=(10, 6))

    for i, scores in enumerate(story_scores):
        plt.plot(range(1, len(scores) + 1), scores, label=f"Story {i + 1}")

    plt.title(title)
    plt.xlabel("Quarter Pair")
    plt.ylabel(ylabel)
    plt.legend(loc="upper right", fontsize="small")
    plt.tight_layout()
    plt.savefig(os.path.join(output_folder, output_filename))
    plt.close()

def main():
    # Parse results
    generated_scores = parse_results(generated_results_path)
    human_scores = parse_results(human_results_path)

    if not generated_scores and not human_scores:
        print("No scores available to plot.")
        return

    # Create line graphs
    create_line_graph(
        generated_scores,
        "WMD Scores for Generated Stories (Quarterly)",
        "WMD Score",
        "generated_stories_quarters_line_graph.png"
    )

    create_line_graph(
        human_scores,
        "WMD Scores for Human Stories (Quarterly)",
        "WMD Score",
        "human_stories_quarters_line_graph.png"
    )

    print("Line graphs generated and saved!")

if __name__ == "__main__":
    main()
