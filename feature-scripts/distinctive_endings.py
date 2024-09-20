# conda activate spacy_env
# goes through the endings_embeddings files, finds average euclidean distance between beginning and endings
# stores output in endings_human/generated_results.txt, which is each individual story's distance and average across all

import os
import numpy as np

import os
import numpy as np

def load_embeddings_from_file(file_path):
    """
    Load the embeddings for both the first part and last 10 sentences from the file.
    
    Args:
        file_path (str): Path to the file containing the embeddings.
    
    Returns:
        tuple: Two lists of embeddings: first part and last 10 sentences.
    """
    first_part_embeddings = []
    last_part_embeddings = []
    reading_first_part = False
    reading_last_part = False
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue  # Skip empty lines
            
            if "First Part Embeddings:" in line:
                reading_first_part = True
                reading_last_part = False
                continue
            elif "Last 10 Sentences Embeddings:" in line:
                reading_first_part = False
                reading_last_part = True
                continue
            
            try:
                # Convert the line to a numpy array
                embedding = np.array(eval(line))
                
                if reading_first_part:
                    first_part_embeddings.append(embedding)
                elif reading_last_part:
                    last_part_embeddings.append(embedding)
            except (SyntaxError, ValueError) as e:
                print(f"Error parsing line in {file_path}: {line} - {e}")
    
    return first_part_embeddings, last_part_embeddings



def compute_average_euclidean_distance(first_part, last_part):
    """
    Compute the average Euclidean distance between embeddings in the first part and last 10 sentences.
    
    Args:
        first_part (list): List of embeddings for the first part of the text.
        last_part (list): List of embeddings for the last 10 sentences.
    
    Returns:
        float: The average Euclidean distance between the embeddings.
    """
    distances = []
    
    # Ensure the lists have the same number of embeddings to compute pairwise distances.
    min_length = min(len(first_part), len(last_part))
    
    for i in range(min_length):
        dist = np.linalg.norm(first_part[i] - last_part[i])  # Euclidean distance
        distances.append(dist)
    
    if len(distances) == 0:
        return 0  # If there's no valid distance, return 0
    
    return np.mean(distances)


def process_endings_embeddings_folder(folder_path, output_file):
    """
    Process all embedding files in the endings_embeddings folder and save the results.
    
    Args:
        folder_path (str): Path to the endings_embeddings folder.
        output_file (str): Path to the file where the results will be saved.
    """
    results = []
    total_distance = 0
    file_count = 0
    
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".txt"):
            file_path = os.path.join(folder_path, file_name)
            
            # Load embeddings from the file
            first_part_embeddings, last_part_embeddings = load_embeddings_from_file(file_path)
            
            # Compute the average Euclidean distance for this file
            avg_distance = compute_average_euclidean_distance(first_part_embeddings, last_part_embeddings)
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
    folder_path = "embeddings/generated/endings_embeddings"  # Path to your endings_embeddings folder
    output_file = "results/distinctive_endings/endings_generated_results.txt"  # Output file for the results
    
    process_endings_embeddings_folder(folder_path, output_file)
