import os
import spacy

def is_likely_character(entity):
    return entity.label_ == "PERSON"

def count_characters(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    named_entities = [ent.text for ent in doc.ents if is_likely_character(ent)]
    unique_named_entities = list(set(named_entities))
    num_unique_named_entities = len(unique_named_entities)

    return num_unique_named_entities, unique_named_entities

def analyze_stories(input_folder, output_file):
    results = []
    
    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):
            filepath = os.path.join(input_folder, filename)
            with open(filepath, "r", encoding="utf-8") as file:
                text = file.read()
                num_characters, characters = count_characters(text)

                result = (
                    f"Title: {filename}\n"
                    f"Number of Characters: {num_characters}\n"
                    f"Characters: {characters}\n"
                )
                results.append(result)

    with open(output_file, "w", encoding="utf-8") as file:
        file.write("### Character Analysis Results for Each File ###\n\n")
        file.write("\n\n".join(results))

def main():
    human_stories_folder = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/human-stories"
    generated_stories_folder = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/generated-stories"

    human_character_results_file = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/focused-character-event/results/human_character_results.txt"
    generated_character_results_file = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/focused-character-event/results/generated_character_results.txt"

    print("Analyzing human-written stories for Character Count...")
    analyze_stories(human_stories_folder, human_character_results_file)
    print("Analyzing generated stories for Character Count...")
    analyze_stories(generated_stories_folder, generated_character_results_file)

if __name__ == "__main__":
    main()
