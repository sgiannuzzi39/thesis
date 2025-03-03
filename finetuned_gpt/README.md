# My AI Generator from Scratch

The goal of this project is to create an AI-based system that can generate creative short stories by fine-tuning a pre-trained language model (GPT-2). The project involves loading and preprocessing a dataset of text files, fine-tuning the model on this data, and then generating new stories based on user-provided prompts.

## Project Structure and Explanation

### 1. Main Script: `main.py`
**Purpose**:  
Entry point for project. It orchestrates the entire process by calling functions from the other scripts to load data, preprocess it, fine-tune the model, and generate a story.

**Steps**:
- **Load Data**: Loads the text files containing stories.
- **Preprocess Stories**: Preprocesses these stories to prepare them for model training.
- **Create Corpus**: Combines the stories into a single corpus (a large body of text) for model fine-tuning.
- **Fine-tune the Model**: Fine-tunes the GPT-2 model on specific dataset.
- **Generate Story**: Uses the fine-tuned model to generate a new story based on a given prompt.

**Overall Role**:  
`main.py` serves as the controller that manages the sequence of tasks, ensuring the entire process flows smoothly from data loading to story generation.

### 2. Data Loading Script: `load_data.py`
**Purpose**:  
This script is responsible for loading the text files from a specified directory and returning their content as a list of strings.

**Functionality**:
- **`load_txt_files(directory)`**: This function takes the path to a directory containing `.txt` files, reads each file, and stores its content in a list. Each item in the list corresponds to the content of one file (i.e., one story).

**Role in the Project**:  
It provides the raw data (stories) needed for further processing and model fine-tuning.

### 3. Preprocessing Script: `preprocess.py`
**Purpose**:  
This script cleans and organizes the raw text data, making it suitable for training the model.

**Functionality**:
- **`preprocess_story(text)`**: This function takes a single story and extracts the title, author, and content. It also performs basic text cleaning, such as removing extra spaces and normalizing line breaks.
- **`preprocess_stories(stories)`**: This function applies `preprocess_story` to each story in the dataset, returning a list of dictionaries where each dictionary contains the title, author, and content of a story.

**Role in the Project**:  
It prepares the raw text data by cleaning it and structuring it in a consistent format, which is essential for effective model training.

### 4. Model Fine-Tuning Script: `train_model.py`
**Purpose**:  
This script fine-tunes the pre-trained GPT-2 model on specific dataset of stories.

**Key Components**:
- **`GPT2Tokenizer` and `GPT2LMHeadModel`**: These are components from the `transformers` library used to tokenize text and build the language model, respectively.
- **`CustomTrainer` Class**: A subclass of `Trainer` that includes a custom `compute_loss` method, ensuring the model correctly computes the loss during training.
- **`fine_tune_model(corpus)`**: This function fine-tunes GPT-2 on the provided text corpus, using the `CustomTrainer` class to manage the training process.

**Role in the Project**:  
It customizes the GPT-2 model, adapting it to specific data (stories) so that it can generate text that aligns with the style and content of dataset.

### 5. Story Generation Script: `generate_story.py`
**Purpose**:  
This script generates new stories using the fine-tuned GPT-2 model.

**Key Components**:
- **`generate_story(prompt)`**: This function takes a prompt (a starting text, like a title and author) and generates a continuation using the fine-tuned GPT-2 model. It includes parameters to control the diversity and coherence of the generated text.

**Role in the Project**:  
It produces the final output of the project—a new, AI-generated story based on the user's input.

## How It All Fits Together

### Initialization (`main.py`):
- The process begins with loading the text files containing stories using the `load_data.py` script.
- These stories are then preprocessed using `preprocess.py` to ensure they are in the correct format for training.

### Fine-tuning (`train_model.py`):
- The preprocessed stories are combined into a corpus and used to fine-tune the GPT-2 model. Fine-tuning adjusts the model's weights so that it better understands the structure, style, and content of dataset.

### Story Generation (`generate_story.py`):
- After fine-tuning, the model is ready to generate new stories. You provide a prompt (e.g., a title and author), and the script generates a story continuation.

## To Train and Run

To train the model and generate a story, run the following command:

```bash
rm -rf fine_tuned_gpt2
python main.py
