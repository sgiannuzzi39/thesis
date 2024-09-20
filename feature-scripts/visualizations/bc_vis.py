import os
import pandas as pd
import matplotlib.pyplot as plt

# Function to load data from the results file
def load_data(file_path):
    """
    Load the analysis results from the given file and return as a DataFrame.
    
    Args:
        file_path (str): Path to the results file.
    
    Returns:
        pd.DataFrame: DataFrame with parsed metrics.
    """
    data = {
        'Title': [],
        'Unnecessary words': [],
        'Adjectives': [],
        'Adverbs': [],
        'Word count': [],
        'Character count': [],
        'Sentence count': []
    }
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            # Skip the overall averages
            if "Average" in line:
                continue
            
            # If the line starts with "Title", we parse the title and subsequent metrics
            if line.startswith("Title:"):
                title = line.replace("Title:", "").strip()
                data['Title'].append(title)
            elif "Unnecessary words" in line:
                data['Unnecessary words'].append(int(line.split(":")[1].strip()))
            elif "Adjectives" in line:
                data['Adjectives'].append(int(line.split(":")[1].strip()))
            elif "Adverbs" in line:
                data['Adverbs'].append(int(line.split(":")[1].strip()))
            elif "Word count" in line:
                data['Word count'].append(int(line.split(":")[1].strip()))
            elif "Character count" in line:
                data['Character count'].append(int(line.split(":")[1].strip()))
            elif "Sentence count" in line:
                data['Sentence count'].append(int(line.split(":")[1].strip()))
    
    return pd.DataFrame(data)

# Load the generated and human-written results
generated_file = '/Users/sgiannuzzi/Desktop/thesis/feature-scripts/results/brevity_conciseness/bc_generated_results.txt'
human_file = '/Users/sgiannuzzi/Desktop/thesis/feature-scripts/results/brevity_conciseness/bc_human_results.txt'

generated_data = load_data(generated_file)
human_data = load_data(human_file)

# Add a new column to distinguish between generated and human stories
generated_data['Type'] = 'Generated'
human_data['Type'] = 'Human'

# Combine both datasets
combined_data = pd.concat([generated_data, human_data])

# Set the story titles as the index for the plot
combined_data.set_index('Title', inplace=True)

# Plot the stacked bar chart for unnecessary words, adjectives, and adverbs
metrics = ['Unnecessary words', 'Adjectives', 'Adverbs']

# Separate generated and human stories
generated_stories = combined_data[combined_data['Type'] == 'Generated']
human_stories = combined_data[combined_data['Type'] == 'Human']

# Plotting
fig, axes = plt.subplots(1, 2, figsize=(14, 8), sharey=True)

# Generated Stories Stacked Bar Plot
generated_stories[metrics].plot(kind='bar', stacked=True, ax=axes[0], color=['#1f77b4', '#ff7f0e', '#2ca02c'])
axes[0].set_title('Generated Stories')
axes[0].set_xlabel('Story Title')
axes[0].set_ylabel('Count')
axes[0].tick_params(axis='x', rotation=90)

# Human Stories Stacked Bar Plot
human_stories[metrics].plot(kind='bar', stacked=True, ax=axes[1], color=['#1f77b4', '#ff7f0e', '#2ca02c'])
axes[1].set_title('Human-Written Stories')
axes[1].set_xlabel('Story Title')
axes[1].tick_params(axis='x', rotation=90)

# Add a legend
plt.legend(['Unnecessary words', 'Adjectives', 'Adverbs'], loc='upper center', bbox_to_anchor=(-0.1, 1.15),
           fancybox=True, shadow=True, ncol=3)

# Adjust layout for better spacing
plt.tight_layout()
plt.show()
