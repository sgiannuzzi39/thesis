# train_model.py

from transformers import GPT2Tokenizer, GPT2LMHeadModel, TrainingArguments, Trainer
from datasets import Dataset
from transformers import GPT2Config

class CustomTrainer(Trainer):
    def compute_loss(self, model, inputs, return_outputs=False):
        labels = inputs.get("input_ids").clone()
        outputs = model(**inputs, labels=labels)
        loss = outputs.loss
        return (loss, outputs) if return_outputs else loss

def fine_tune_model(corpus):
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    tokenizer.pad_token = tokenizer.eos_token

    config = GPT2Config.from_pretrained("gpt2")
    config.attn_pdrop = 0.2  # Moderate dropout
    config.resid_pdrop = 0.2  # Moderate dropout
    config.embd_pdrop = 0.2  # Moderate dropout

    model = GPT2LMHeadModel.from_pretrained("gpt2", config=config)

    # **Freeze the first 6 layers of the transformer model**
    for param in model.transformer.h[:6].parameters():
        param.requires_grad = False

    def tokenize_function(examples):
        return tokenizer(examples['text'], padding="max_length", truncation=True, max_length=512)

    dataset = Dataset.from_dict({"text": [corpus]})
    tokenized_dataset = dataset.map(tokenize_function, batched=True)

    training_args = TrainingArguments(
        output_dir="./results",
        per_device_train_batch_size=1,  # Adjust based on your GPU memory
        num_train_epochs=5,  # Increased epochs
        learning_rate=3e-5,  # Lowered learning rate
        weight_decay=0.01,  # Regularization
        logging_dir='./logs',
        logging_steps=10,
        report_to="none"
    )

    trainer = CustomTrainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset,
    )

    print("Starting model fine-tuning...")
    trainer.train()
    print("Model fine-tuning complete.")

    model.save_pretrained("./fine_tuned_gpt2")
    tokenizer.save_pretrained("./fine_tuned_gpt2")
