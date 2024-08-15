from transformers import GPT2Tokenizer, GPT2LMHeadModel, TrainingArguments, Trainer
from datasets import Dataset
from transformers import GPT2Config  # If using GPT2Config for dropout

class CustomTrainer(Trainer):
    def compute_loss(self, model, inputs, return_outputs=False):
        labels = inputs.get("input_ids").clone()
        outputs = model(**inputs, labels=labels)
        loss = outputs.loss
        return (loss, outputs) if return_outputs else loss

def fine_tune_model(corpus):
    # Ensure the tokenizer and model are imported and defined properly
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

    # Add padding token
    tokenizer.pad_token = tokenizer.eos_token

    # Create a GPT2 model configuration with dropout (if using dropout)
    config = GPT2Config.from_pretrained("gpt2")
    config.attn_pdrop = 0.1  # Dropout for attention probabilities
    config.resid_pdrop = 0.1  # Dropout for residual connections
    config.embd_pdrop = 0.1  # Dropout for embeddings

    model = GPT2LMHeadModel.from_pretrained("gpt2", config=config)

    def tokenize_function(examples):
        return tokenizer(examples['text'], padding="max_length", truncation=True, max_length=512)

    dataset = Dataset.from_dict({"text": [corpus]})
    tokenized_dataset = dataset.map(tokenize_function, batched=True)

    training_args = TrainingArguments(
        output_dir="./results",
        per_device_train_batch_size=1,
        num_train_epochs=5,
        learning_rate=5e-5,
        logging_dir='./logs',
        logging_steps=10,
        report_to="none"
    )

    trainer = CustomTrainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset,
    )

    trainer.train()
    model.save_pretrained("./fine_tuned_gpt2")
    tokenizer.save_pretrained("./fine_tuned_gpt2")
