# conda activate spacy_env
# code co-authored with ChatGPT
import os
import spacy

# Load the spaCy English model globally
nlp = spacy.load("en_core_web_sm")

def load_text_from_file(file_path):
    """
    Loads the text from an external .txt file.
    
    Args:
        file_path (str): Path to the .txt file.
        
    Returns:
        str: Content of the file as a string.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def extract_title(text):
    """
    Extracts the title from the first line of the text file.
    
    Args:
        text (str): The content of the text file.
        
    Returns:
        str: The title of the story (extracted from the first line).
    """
    first_line = text.splitlines()[0]
    if first_line.startswith("Title: "):
        return first_line.replace("Title: ", "").strip()
    else:
        return "Unknown Title"

def analyze_text(text, unnecessary_words):
    """
    Analyzes the text to count unnecessary words, adjectives, adverbs, 
    total words, total characters, and sentences.
    
    Args:
        text (str): The input text.
        unnecessary_words (list): List of unnecessary words.
        
    Returns:
        dict: A dictionary containing counts of unnecessary words, adjectives, adverbs, 
              total words, total characters, and sentences.
    """
    doc = nlp(text)
    
    unnecessary_word_count = 0
    adjective_count = 0
    adverb_count = 0
    sentence_count = len(list(doc.sents))
    total_characters = len(text)
    
    # Iterate through each token in the text
    for token in doc:
        # Check if the token is an unnecessary word
        if token.text.lower() in unnecessary_words:
            unnecessary_word_count += 1
        
        # Check if the token is an adjective
        if token.pos_ == "ADJ":
            adjective_count += 1
        
        # Check if the token is an adverb
        if token.pos_ == "ADV":
            adverb_count += 1
    
    # Count the total number of words
    total_words = len([token.text for token in doc if token.is_alpha])
    
    return {
        "unnecessary_word_count": unnecessary_word_count,
        "adjective_count": adjective_count,
        "adverb_count": adverb_count,
        "total_words": total_words,
        "total_characters": total_characters,
        "sentence_count": sentence_count
    }

def analyze_folder(folder_path, unnecessary_words, output_file):
    """
    Analyzes all .txt files in the specified folder, calculates the average for each data point,
    and writes the results to an output text file.
    
    Args:
        folder_path (str): Path to the folder containing the .txt files.
        unnecessary_words (list): List of unnecessary words to count.
        output_file (str): Path to the output file where results will be saved.
    """
    total_files = 0
    total_unnecessary_words = 0
    total_adjectives = 0
    total_adverbs = 0
    total_word_count = 0
    total_character_count = 0
    total_sentence_count = 0
    
    results = []

    for file_name in os.listdir(folder_path):
        if file_name.endswith(".txt"):
            file_path = os.path.join(folder_path, file_name)
            text = load_text_from_file(file_path)
            title = extract_title(text)
            
            # Analyze the text
            analysis_result = analyze_text(text, unnecessary_words)
            
            # Aggregate totals for averaging later
            total_unnecessary_words += analysis_result['unnecessary_word_count']
            total_adjectives += analysis_result['adjective_count']
            total_adverbs += analysis_result['adverb_count']
            total_word_count += analysis_result['total_words']
            total_character_count += analysis_result['total_characters']
            total_sentence_count += analysis_result['sentence_count']
            total_files += 1
            
            # Add individual file's results to the list
            results.append(f"Title: {title}\n"
                           f"Unnecessary words: {analysis_result['unnecessary_word_count']}\n"
                           f"Adjectives: {analysis_result['adjective_count']}\n"
                           f"Adverbs: {analysis_result['adverb_count']}\n"
                           f"Word count: {analysis_result['total_words']}\n"
                           f"Character count: {analysis_result['total_characters']}\n"
                           f"Sentence count: {analysis_result['sentence_count']}\n\n")
    
    # Calculate averages across all files
    if total_files > 0:
        avg_unnecessary_words = total_unnecessary_words / total_files
        avg_adjectives = total_adjectives / total_files
        avg_adverbs = total_adverbs / total_files
        avg_word_count = total_word_count / total_files
        avg_character_count = total_character_count / total_files
        avg_sentence_count = total_sentence_count / total_files
    else:
        avg_unnecessary_words = avg_adjectives = avg_adverbs = avg_word_count = avg_character_count = avg_sentence_count = 0
    
    # Write the results to the output file
    with open(output_file, 'w', encoding='utf-8') as output:
        output.write("### Analysis Results for Each File ###\n\n")
        for result in results:
            output.write(result)
        
        # Write averages at the end
        output.write("### Averages Across All Files ###\n\n")
        output.write(f"Average unnecessary words: {avg_unnecessary_words:.2f}\n")
        output.write(f"Average adjectives: {avg_adjectives:.2f}\n")
        output.write(f"Average adverbs: {avg_adverbs:.2f}\n")
        output.write(f"Average word count: {avg_word_count:.2f}\n")
        output.write(f"Average character count: {avg_character_count:.2f}\n")
        output.write(f"Average sentence count: {avg_sentence_count:.2f}\n")

# Example usage
if __name__ == "__main__":
    folder_path = "generated-stories/"  # Replace with the path to the folder with .txt files
    unnecessary_words = [ "totally", "completely", "absolutely", "literally", "definitely", "certainly", "probably",
    "actually", "basically", "virtually", "very", "really", "just", "quite", "incredibly",
    "seriously", "truly", "simply", "frankly", "honestly", "obviously", "surely", "undoubtedly", 
    "essentially", "utterly", "slightly", "relatively", "remarkably", "particularly", "extremely",
    "especially", "exceptionally", "highly", "awfully"]
    output_file = "analysis_results.txt"
    analyze_folder(folder_path, unnecessary_words, output_file)
