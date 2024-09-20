import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Function to load distances from the results file
def load_distances(file_path, label):
    """
    Load the Euclidean distances and story names from a results file.
    
    Args:
        file_path (str): Path to the results file.
        label (str): A label to indicate whether the story is generated or human-written.
    
    Returns:
        list of tuples: Each tuple contains a cleaned story name, Euclidean distance, and label.
    """
    story_data = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            # Skip the overall average line
            if "Overall Average" in line:
                continue
            
            # We expect lines in the format "StoryName_split_embeddings.txt: distance"
            if ":" in line:
                # Extract and clean the story name
                story_name, distance_str = line.split(":")[0], line.split(":")[1].strip()
                story_name = story_name.replace('_', ' ').replace('split', '').replace('embeddings', '').replace('.txt', '').title().strip()
                story_data.append((story_name, float(distance_str), label))
    
    return story_data

# Provide the absolute paths to the generated and human results files
generated_results_file = '/Users/sgiannuzzi/Desktop/thesis/feature-scripts/results/distinctive_endings/endings_generated_results.txt'
human_results_file = '/Users/sgiannuzzi/Desktop/thesis/feature-scripts/results/distinctive_endings/endings_human_results.txt'

# Check if files exist
if not os.path.exists(generated_results_file):
    print(f"Error: Generated results file not found at {generated_results_file}")
    exit(1)

if not os.path.exists(human_results_file):
    print(f"Error: Human results file not found at {human_results_file}")
    exit(1)

# Load distances from both generated and human short stories
generated_data = load_distances(generated_results_file, 'Generated')
human_data = load_distances(human_results_file, 'Human')

# Combine both datasets
combined_data = generated_data + human_data

# Sort the combined data by Euclidean distance
sorted_data = sorted(combined_data, key=lambda x: x[1])

# Unpack the sorted data into separate lists
sorted_story_names, sorted_distances, sorted_labels = zip(*sorted_data)

# Set style and figure size
plt.style.use('seaborn-whitegrid')  # Using seaborn whitegrid for cleaner look
plt.figure(figsize=(12, 8))

# Use different colors for the labels and increase point size
colors = ['#1f77b4' if label == 'Generated' else '#ff7f0e' for label in sorted_labels]  # Blue for generated, orange for human
plt.scatter(sorted_distances, sorted_story_names, c=colors, s=100, edgecolor='black', alpha=0.7)

# Add labels and title with improved font sizes
plt.xlabel('Euclidean Distance', fontsize=14, fontweight='bold')
plt.ylabel('Story Title', fontsize=14, fontweight='bold')
plt.title('Euclidean Distances Between Beginning and Endings of Short Stories', fontsize=16, fontweight='bold')

# Improve tick parameters
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

# Create custom legend with both blue and orange dots
blue_patch = mpatches.Patch(color='#1f77b4', label='Generated Short Stories')
orange_patch = mpatches.Patch(color='#ff7f0e', label='Human-Written Short Stories')
plt.legend(handles=[blue_patch, orange_patch], fontsize=12)

# Add a grid for better readability
plt.grid(True, linestyle='--', alpha=0.5)

# Show the plot with tight layout for better spacing
plt.tight_layout()
plt.show()
