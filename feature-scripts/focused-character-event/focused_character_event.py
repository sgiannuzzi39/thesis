import os
import spacy
from collections import Counter

def is_likely_character(entity, doc):
    if entity.label_ != "PERSON":
        return False
    
    context_words = [token.text.lower() for token in entity.sent]
    character_context_indicators = {"said", "replied", "asked", "'"}
    if any(word in context_words for word in character_context_indicators):
        return True
    
    return False

def calculate_focused_character_score(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    named_entities = [ent.text for ent in doc.ents if is_likely_character(ent, doc)]

    unique_named_entities = set(named_entities)
    num_unique_named_entities = len(unique_named_entities)

    total_tokens = len([token for token in doc if not token.is_space])
    score = num_unique_named_entities / total_tokens if total_tokens > 0 else 0

    return score, unique_named_entities

def is_temporal_marker(token):
    temporal_markers = {"then", "later", "suddenly", "the next day", "afterward", "meanwhile", "soon", "next", "immediately", "before long"}
    return token.text.lower() in temporal_markers

def calculate_focused_events_score(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    transition_count = 0
    for sentence in doc.sents:
        if any(is_temporal_marker(token) for token in sentence):
            transition_count += 1

    total_sentences = len(list(doc.sents))
    score = transition_count / total_sentences if total_sentences > 0 else 0

    return score, transition_count

def analyze_stories(input_folder, output_file, calculation_function, result_type):
    results = []
    
    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):
            filepath = os.path.join(input_folder, filename)
            with open(filepath, "r", encoding="utf-8") as file:
                text = file.read()
                score, details = calculation_function(text)

                result = (
                    f"Title: {filename}\n"
                    f"{result_type} Score: {score:.4f}\n"
                    f"Details: {details}\n"
                )
                results.append(result)

    with open(output_file, "w", encoding="utf-8") as file:
        file.write(f"### {result_type} Analysis Results for Each File ###\n\n")
        file.write("\n\n".join(results))

def main():
    human_stories_folder = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/human-stories"
    generated_stories_folder = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/generated-stories"

    human_character_results_file = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/focused-character-event/results/human_character_results.txt"
    generated_character_results_file = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/focused-character-event/results/generated_character_results.txt"

    human_event_results_file = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/focused-character-event/results/human_event_results.txt"
    generated_event_results_file = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/focused-character-event/results/generated_event_results.txt"

    print("Analyzing human-written stories for Focused Character Score...")
    analyze_stories(human_stories_folder, human_character_results_file, calculate_focused_character_score, "Focused Character")
    print("Analyzing generated stories for Focused Character Score...")
    analyze_stories(generated_stories_folder, generated_character_results_file, calculate_focused_character_score, "Focused Character")

    print("Analyzing human-written stories for Focused Event Score...")
    analyze_stories(human_stories_folder, human_event_results_file, calculate_focused_events_score, "Focused Event")
    print("Analyzing generated stories for Focused Event Score...")
    analyze_stories(generated_stories_folder, generated_event_results_file, calculate_focused_events_score, "Focused Event")

if __name__ == "__main__":
    main()