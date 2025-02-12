import os
import random
import numpy as np
import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as sch
from sklearn.feature_extraction.text import TfidfVectorizer
from matplotlib.patches import Patch

ai_folder = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/generated-stories"
human_folder = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/human-stories"

def load_random_stories(folder, label, num_samples=50):
    files = [f for f in os.listdir(folder) if f.endswith(".txt")]
    selected_files = random.sample(files, min(num_samples, len(files)))
    stories = []
    labels = []
    
    for file in selected_files:
        file_path = os.path.join(folder, file)
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
            formatted_name = file.replace(".txt", "").replace("_", " ")
            formatted_name = formatted_name.split(",")[0]  
            formatted_name = formatted_name.title() 
            stories.append(text)
            labels.append((formatted_name, label))  
    
    return stories, labels

ai_stories, ai_labels = load_random_stories(ai_folder, "AI")
human_stories, human_labels = load_random_stories(human_folder, "Human")

all_stories = ai_stories + human_stories
all_labels = ai_labels + human_labels

vectorizer = TfidfVectorizer(max_features=1000, stop_words="english")
X = vectorizer.fit_transform(all_stories).toarray()

linkage_matrix = sch.linkage(X, method="ward")

plt.figure(figsize=(14, 7))
dendrogram = sch.dendrogram(linkage_matrix, labels=[label[0] for label in all_labels], leaf_rotation=90, leaf_font_size=8)

ax = plt.gca()
x_labels = ax.get_xticklabels()
for lbl in x_labels:
    text = lbl.get_text()
    for name, label in all_labels:
        if text == name:
            lbl.set_color("blue" if label == "AI" else "green")
            break 

legend_elements = [Patch(facecolor="blue", edgecolor="blue", label="AI-Generated Stories"),
                   Patch(facecolor="green", edgecolor="green", label="Human-Written Stories")]
plt.legend(handles=legend_elements, loc="upper right", fontsize=10, frameon=False)

plt.title("Dendrogram of AI-written vs Human-written Short Stories", fontsize=14)
plt.xlabel("Short Story", fontsize=12)
plt.ylabel("Distance", fontsize=12)
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()
