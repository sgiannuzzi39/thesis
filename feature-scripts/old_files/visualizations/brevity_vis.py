import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Function to load data from the results file
def load_data(file_path, label_suffix):
    """
    Load the analysis results from the given file and return as a DataFrame.
    
    Args:
        file_path (str): Path to the results file.
        label_suffix (str): Suffix to add to the story title for uniqueness.
    
    Returns:
        pd.DataFrame: DataFrame with parsed metrics.
    """
    data = {
        'Title': [],
        'Word count': []
    }
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            # Skip the overall averages
            if "Average" in line:
                continue
            
            # If the line starts with "Title", we parse the title and subsequent metrics
            if line.startswith("Title:"):
                title = line.replace("Title:", "").strip() + label_suffix
                data['Title'].append(title)
            elif "Word count" in line:
                data['Word count'].append(int(line.split(":")[1].strip()))
    
    return pd.DataFrame(data)

# Load the generated and human-written results
generated_file = '/Users/sgiannuzzi/Desktop/thesis/feature-scripts/results/brevity_conciseness/bc_generated_results.txt'
human_file = '/Users/sgiannuzzi/Desktop/thesis/feature-scripts/results/brevity_conciseness/bc_human_results.txt'

generated_data = load_data(generated_file, '_Generated')
human_data = load_data(human_file, '_Human')

# Merge the dataframes on Title to ensure both generated and human stories are aligned
combined_data = pd.merge(generated_data, human_data, on='Title', how='outer', suffixes=('_Generated', '_Human'))

# Sort the data by the total word count (Generated + Human) to order bars from shortest to longest
combined_data['Total_Word_Count'] = combined_data['Word count_Generated'].fillna(0) + combined_data['Word count_Human'].fillna(0)
combined_data.sort_values(by='Total_Word_Count', inplace=True)

# Set up x-axis positions
x = np.arange(len(combined_data))

# Width of each bar
width = 0.35

# Define colors using the specified purple shades
colors = {
    'Generated': '#CBC3E3',  # Light Purple
    'Human': '#5D3FD3'       # Dark Purple
}

# Create the figure and axis for plotting
fig, ax = plt.subplots(figsize=(14, 6))

# Plot the bar chart for generated stories (shifted slightly left)
ax.bar(x - width/2, combined_data['Word count_Generated'], width, label='Generated Stories', color=colors['Generated'])

# Plot the bar chart for human-written stories (shifted slightly right)
ax.bar(x + width/2, combined_data['Word count_Human'], width, label='Human-Written Stories', color=colors['Human'])

# Customize the plot
ax.set_title('Stories by Word Count', fontsize=16, fontweight='bold')
ax.set_ylabel('Word Count', fontsize=14)

# Remove x-axis labels (titles)
ax.set_xticks(x)
ax.set_xticklabels([])  # No labels on x-axis

# Set the y-axis limit to go beyond 10,000 words
ax.set_ylim(0, 10500)

# Plot the average lines for generated and human-written stories
avg_generated = 1022.16  # Average word count for generated stories
avg_human = 6652.64      # Average word count for human-written stories

# Add horizontal lines for the averages
ax.axhline(y=avg_generated, color=colors['Generated'], linestyle='--', linewidth=2, label=f'Generated Avg: {avg_generated}')
ax.axhline(y=avg_human, color=colors['Human'], linestyle='--', linewidth=2, label=f'Human Avg: {avg_human}')

# Add legend
ax.legend()

# Adjust layout to prevent overlap
plt.tight_layout()

# Show the plot
plt.show()
