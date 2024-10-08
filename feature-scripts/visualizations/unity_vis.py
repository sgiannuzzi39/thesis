import os
import matplotlib.pyplot as plt

# Function to load distances from the results file
def load_distances(file_path, label):
    """
    Load the Euclidean distances and story names from a results file.
    
    Args:
        file_path (str): Path to the results file.
        label (str): A label to indicate whether the story is generated or human-written.
    
    Returns:
        list of tuples: Each tuple contains a cleaned story name, Euclidean distance, and label.
        float: The overall average Euclidean distance across all files.
    """
    story_data = []
    overall_avg = 0.0
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # Look for the overall average line
            if "Overall Average" in line:
                try:
                    overall_avg = float(line.split(":")[1].strip())
                except (IndexError, ValueError) as e:
                    print(f"Error parsing overall average in file: {file_path}")
                    print(f"Line: {line}, Error: {e}")
                continue
            
            # We expect lines in the format "StoryName_embeddings.txt: distance"
            if ":" in line:
                try:
                    story_name, distance_str = line.split(":")[0], line.split(":")[1].strip()
                    story_name = story_name.replace('_', ' ').replace('embeddings', '').replace('.txt', '').title().strip()
                    story_data.append((story_name, float(distance_str), label))
                except (IndexError, ValueError) as e:
                    print(f"Error parsing story data in file: {file_path}")
                    print(f"Line: {line}, Error: {e}")
    
    return story_data, overall_avg

# Provide the absolute paths to the generated and human results files
generated_results_file = '/Users/sgiannuzzi/Desktop/thesis/feature-scripts/results/unity/unity_generated_results.txt'
human_results_file = '/Users/sgiannuzzi/Desktop/thesis/feature-scripts/results/unity/unity_human_results.txt'

# Check if files exist
if not os.path.exists(generated_results_file):
    print(f"Error: Generated results file not found at {generated_results_file}")
    exit(1)

if not os.path.exists(human_results_file):
    print(f"Error: Human results file not found at {human_results_file}")
    exit(1)

# Load distances from both generated and human short stories and their overall averages
generated_data, generated_avg = load_distances(generated_results_file, 'Generated')
human_data, human_avg = load_distances(human_results_file, 'Human')

# Combine the datasets by separating the distances for the box plot
generated_distances = [distance for _, distance, label in generated_data]
human_distances = [distance for _, distance, label in human_data]

# Create a box-and-whisker plot
plt.figure(figsize=(12, 8))
boxplot = plt.boxplot([generated_distances, human_distances], labels=['Generated', 'Human'], patch_artist=True)

# Customize the plot appearance
plt.title('Euclidean Distances Across Entirety of Short Stories', fontsize=16, fontweight='bold')
plt.ylabel('Euclidean Distance', fontsize=14, fontweight='bold')

# Customize colors for the box plots to shades of purple
colors = ['#CBC3E3', '#5D3FD3']
for patch, color in zip(boxplot['boxes'], colors):
    patch.set_facecolor(color)

# Change the median line color to light gray for better visibility
for median in boxplot['medians']:
    median.set_color('#A9A9A9')  # Light gray color
    median.set_linewidth(2)  # Increase line width for better visibility

# Add a grid for better readability
plt.grid(True, linestyle='--', alpha=0.5)

# Display the plot
plt.tight_layout()
plt.show()
