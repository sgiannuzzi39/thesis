import os
import matplotlib.pyplot as plt
import numpy as np

# Function to extract the averages from the results file
def extract_averages(file_path):
    """
    Extract the average values for unnecessary words, adjectives, adverbs, and word count from the results file.
    
    Args:
        file_path (str): Path to the results file.
    
    Returns:
        dict: Dictionary containing the average values.
    """
    averages = {
        'Unnecessary words': 0,
        'Adjectives': 0,
        'Adverbs': 0,
        'Word count': 0
    }
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if "Average unnecessary words" in line:
                averages['Unnecessary words'] = float(line.split(":")[1].strip())
            elif "Average adjectives" in line:
                averages['Adjectives'] = float(line.split(":")[1].strip())
            elif "Average adverbs" in line:
                averages['Adverbs'] = float(line.split(":")[1].strip())
            elif "Average word count" in line:
                averages['Word count'] = float(line.split(":")[1].strip())
    
    return averages

# File paths for generated and human results
generated_file = '/Users/sgiannuzzi/Desktop/thesis/feature-scripts/results/brevity_conciseness/bc_generated_results.txt'
human_file = '/Users/sgiannuzzi/Desktop/thesis/feature-scripts/results/brevity_conciseness/bc_human_results.txt'

# Extract averages for generated and human stories
generated_averages = extract_averages(generated_file)
human_averages = extract_averages(human_file)

# Calculate proportions relative to average word count for generated and human stories
generated_proportions = {
    'Unnecessary words': generated_averages['Unnecessary words'] / generated_averages['Word count'],
    'Adjectives': generated_averages['Adjectives'] / generated_averages['Word count'],
    'Adverbs': generated_averages['Adverbs'] / generated_averages['Word count']
}

human_proportions = {
    'Unnecessary words': human_averages['Unnecessary words'] / human_averages['Word count'],
    'Adjectives': human_averages['Adjectives'] / human_averages['Word count'],
    'Adverbs': human_averages['Adverbs'] / human_averages['Word count']
}

# Set up categories and values for the bar chart
categories = ['Unnecessary words', 'Adjectives', 'Adverbs']
generated_values = [generated_proportions['Unnecessary words'], generated_proportions['Adjectives'], generated_proportions['Adverbs']]
human_values = [human_proportions['Unnecessary words'], human_proportions['Adjectives'], human_proportions['Adverbs']]

# Set up bar chart positions
x = np.arange(len(categories))
width = 0.35  # Width of the bars

# Create the bar chart
fig, ax = plt.subplots(figsize=(10, 6))

# Plot generated bars
ax.bar(x - width/2, generated_values, width, label='Generated', color='#CBC3E3')  # Light purple for generated stories

# Plot human bars
ax.bar(x + width/2, human_values, width, label='Human', color='#5D3FD3')  # Dark purple for human stories

# Customize the plot
ax.set_title('Proportions of Adjectives, Adverbs, and Unnecessary Words to Word Count', fontsize=16, fontweight='bold')
ax.set_xlabel('Categories', fontsize=14)
ax.set_ylabel('Proportion Relative to Word Count', fontsize=14)
ax.set_xticks(x)
ax.set_xticklabels(categories)

# Add legend
ax.legend()

# Adjust layout to prevent overlap
plt.tight_layout()

# Show the plot
plt.show()
