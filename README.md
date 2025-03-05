# Evaluating AI as Author: An Analysis of AI-Generated Short Stories

This repository includes all relevant code created for *Evaluating AI as Author: An Analysis of AI-Generated Short Stories*, a thesis submitted to the **Harvard English Department** by **Sofia Giannuzzi** in partial fulfillment of the requirements for the **Bachelor’s Degree with Honors**.

*Writing this code was supported in part by AI tools, specifically OpenAI's ChatGPT.*

---

## Repository Structure

This repository contains **five folders**:

### 1. `crawlers`
This folder contains the Python scripts that were utilized to scrape short stories from online platforms, including:
- **The New Yorker website** (additional stories were collected by clicking “Next Page”):  
  [https://www.newyorker.com/magazine/fiction](https://www.newyorker.com/magazine/fiction)  
- **100 Great Short Stories**:  
  [https://americanliterature.com/100-great-short-stories/](https://americanliterature.com/100-great-short-stories/)  
- **Classic Short Stories site**:  
  [https://classicshorts.com/](https://classicshorts.com/)

Stories were also collected from the Tin House Fiction archive, though they were collected manually: 
- **Tin House Fiction archive**:  
  [https://tinhouse.com/category/fiction/](https://tinhouse.com/category/fiction/)

---

### 2. `feature-scripts`
Includes the Python scripts that were made to measure the existence of short story genre conventions within AI-generated and human-written texts (**see Chapter One**). As a result, this directory contains the following folders:
- `brevity-conciseness`
- `distinctive-endings`
- `focused-character-event`
- `intensity`
- `mystery-strangeness`
- `submerged-identity`
- `unity-singleeffect`

Within each of these folders, there is a Python file that holds the algorithm intended to measure for the feature, a folder with the corresponding results of the algorithm, and another file that generates the data visualization to display the findings. The folder `clustering` can also be found in `feature-scripts,` which contains the code that generated the dendrogram (Graph 2.1) in Chapter Two.

---

### 3. `generated-stories`
Contains all of the AI-generated short stories used for data analyses. These stories are stored as `.txt` files.

---

### 4. `gpt-4-turbo-generator`
Includes the Python script used to access OpenAI's GPT-4-turbo API to generate the short stories used in this study.

---

### 5. `human-stories`
Includes all of the human-written stories used for data analyses in this thesis. These stories are stored as `.txt` files.

---
