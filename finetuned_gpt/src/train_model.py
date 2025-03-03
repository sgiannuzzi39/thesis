import os
from transformers import GPT2Tokenizer, GPT2LMHeadModel, TrainingArguments, Trainer
from datasets import Dataset

class CustomTrainer(Trainer):
    def compute_loss(self, model, inputs, return_outputs=False):
        labels = inputs["input_ids"].clone()
        outputs = model(**inputs, labels=labels)
        loss = outputs.loss
        return (loss, outputs) if return_outputs else loss

def load_corpus_from_folder(folder_path):
    stories = []
    for filename in sorted(os.listdir(folder_path)):
        if filename.endswith(".txt"):
            with open(os.path.join(folder_path, filename), "r", encoding="utf-8") as f:
                stories.append(f.read().strip())
    return " ".join(stories)

def fine_tune_model(corpus_path, output_dir):
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    tokenizer.pad_token = tokenizer.eos_token

    model = GPT2LMHeadModel.from_pretrained("gpt2")

    # Load and preprocess the dataset
    print(f"Loading corpus from: {corpus_path}")
    corpus = load_corpus_from_folder(corpus_path)
    chunk_size = 512
    corpus_chunks = [corpus[i:i+chunk_size] for i in range(0, len(corpus), chunk_size)]
    dataset = Dataset.from_dict({"text": corpus_chunks})

    def tokenize_function(examples):
        return tokenizer(
            examples['text'], 
            padding="max_length", 
            truncation=True, 
            max_length=512
        )

    print("Tokenizing dataset...")
    tokenized_dataset = dataset.map(tokenize_function, batched=True)

    training_args = TrainingArguments(
        output_dir=output_dir,
        per_device_train_batch_size=1,
        num_train_epochs=3,
        learning_rate=5e-5,
        logging_dir=f"{output_dir}/logs",
        logging_steps=10,
        gradient_accumulation_steps=4,
        save_steps=500,
        save_total_limit=2,
        fp16=False,
        dataloader_num_workers=0,
        report_to="none"
    )

    trainer = CustomTrainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset,
    )

    print("Starting training...")
    trainer.train()

    print(f"Saving fine-tuned model to: {output_dir}")
    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)
