# conda activate spacy_env
# finds the average euc distance between all words in a text 
# saves output in unity_human/generated_results.txt

import os
import numpy as np

def load_embeddings_from_file(file_path):
    """
    Load all embeddings from the file.
    
    Args:
        file_path (str): Path to the file containing the embeddings.
    
    Returns:
        list: List of embeddings from the file.
    """
    embeddings = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue  # Skip empty lines
            try:
                # Convert the line to a numpy array
                embedding = np.array(eval(line))
                embeddings.append(embedding)
            except (SyntaxError, ValueError) as e:
                print(f"Error parsing line in {file_path}: {line} - {e}")
    
    return embeddings


def compute_average_euclidean_distance(embeddings):
    """
    Compute the average Euclidean distance between all pairs of embeddings in the file.
    
    Args:
        embeddings (list): List of embeddings.
    
    Returns:
        float: The average Euclidean distance between all pairs of embeddings.
    """
    distances = []
    
    # Compute pairwise Euclidean distances between all word embeddings
    for i in range(len(embeddings)):
        for j in range(i+1, len(embeddings)):
            dist = np.linalg.norm(embeddings[i] - embeddings[j])  # Euclidean distance
            distances.append(dist)
    
    if len(distances) == 0:
        return 0  # If there are no valid distances, return 0
    
    return np.mean(distances)


def process_total_embeddings_folder(folder_path, output_file):
    """
    Process all embedding files in the total_embeddings folder and save the results.
    
    Args:
        folder_path (str): Path to the total_embeddings folder.
        output_file (str): Path to the file where the results will be saved.
    """
    results = []
    total_distance = 0
    file_count = 0
    
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".txt"):
            file_path = os.path.join(folder_path, file_name)
            
            # Load embeddings from the file
            embeddings = load_embeddings_from_file(file_path)
            
            # Compute the average Euclidean distance for this file
            avg_distance = compute_average_euclidean_distance(embeddings)
            results.append(f"{file_name}: {avg_distance:.4f}")
            
            total_distance += avg_distance
            file_count += 1
    
    # Calculate the overall average
    if file_count > 0:
        overall_avg_distance = total_distance / file_count
    else:
        overall_avg_distance = 0
    
    # Save results to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("### Average Euclidean Distances for Each File ###\n")
        f.write("\n".join(results))
        f.write(f"\n\n### Overall Average Euclidean Distance Across All Files ###\n")
        f.write(f"Overall Average: {overall_avg_distance:.4f}\n")


# Example usage
if __name__ == "__main__":
    folder_path = "embeddings/generated/total_embeddings"  # Path to your total_embeddings folder
    output_file = "results/unity/unity_generated_results.txt"  # Output file for the results
    
    process_total_embeddings_folder(folder_path, output_file)
