"""
SETUP: conda activate py39
Code co-authored with ChatGPT
"""

import os
import glob
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.cluster.hierarchy import dendrogram, linkage
import matplotlib.pyplot as plt
import numpy as np

def load_texts_from_directory(directory):
    texts = []
    titles = []
    for filepath in glob.glob(os.path.join(directory, "*.txt")):
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
            texts.append(content)
            first_line = content.splitlines()[0]
            if first_line.startswith("Title: "):
                title = first_line.replace("Title: ", "").strip()
            else:
                title = os.path.basename(filepath)  
            titles.append(title)
    return texts, titles

ai_dir = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/generated-stories"
human_dir = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/human-stories"

ai_texts, ai_titles = load_texts_from_directory(ai_dir)
human_texts, human_titles = load_texts_from_directory(human_dir)

all_texts = ai_texts + human_texts
all_labels = ["Generated: " + title for title in ai_titles] + ["Human: " + title for title in human_titles]

vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
tfidf_matrix = vectorizer.fit_transform(all_texts)

linkage_matrix = linkage(tfidf_matrix.toarray(), method='ward')

def label_colors(label):
    if label.startswith("Generated: "):
        return 'blue'
    elif label.startswith("Human: "):
        return 'green'
    return 'black'

plt.figure(figsize=(12, 8))
dendrogram(
    linkage_matrix,
    labels=all_labels,
    leaf_rotation=90,
    leaf_font_size=10,
    leaf_label_func=lambda x: f"{all_labels[int(x)]}",
    color_threshold=0
)
ax = plt.gca()
xlbls = ax.get_xmajorticklabels()
for lbl in xlbls:
    text = lbl.get_text()
    lbl.set_color(label_colors(text))

plt.title("Hierarchical Clustering Dendrogram")
plt.xlabel("Story")
plt.ylabel("Distance")
plt.tight_layout()

output_path = "/Users/sgiannuzzi/Desktop/thesis/feature-scripts/clustering/results/dendrogram.png"
os.makedirs(os.path.dirname(output_path), exist_ok=True)
plt.savefig(output_path)
plt.show()
