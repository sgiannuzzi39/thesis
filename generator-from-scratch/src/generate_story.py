import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer, GPT2Config

def count_words(text):
    return len(text.split())

def generate_story(prompt="Write a short story.", min_length=1000, max_length=7500, model_dir=None):
    if model_dir is None:
        raise ValueError("model_dir must be specified to load the fine-tuned model.")

    tokenizer = GPT2Tokenizer.from_pretrained(model_dir)
    tokenizer.pad_token = tokenizer.eos_token  

    config = GPT2Config.from_pretrained(model_dir)
    config.n_positions = 1024  

    model = GPT2LMHeadModel.from_pretrained(model_dir, config=config)

    model.transformer.wpe = torch.nn.Embedding(config.n_positions, config.n_embd)
    print("Reinitialized positional embeddings to:", config.n_positions)

    # Validate tokenizer and model alignment
    assert tokenizer.vocab_size == model.config.vocab_size, (
        f"Tokenizer vocab size ({tokenizer.vocab_size}) and model vocab size ({model.config.vocab_size}) do not match!"
    )

    # Tokenize prompt
    inputs = tokenizer.encode(prompt, return_tensors="pt", truncation=True, max_length=config.n_positions)
    print("Input Token IDs:", inputs[0])
    print("Max Token ID:", max(inputs[0]))

    # Validate position IDs
    position_ids = torch.arange(inputs.size(-1), dtype=torch.long, device=inputs.device)
    assert torch.max(position_ids) < config.n_positions, (
        f"Position IDs exceed the maximum allowed ({config.n_positions})!"
    )
    print("Max Position ID:", torch.max(position_ids))

    generated_text = prompt
    word_count = count_words(prompt)

    while word_count < min_length:
        if inputs.size(1) > config.n_positions:
            inputs = inputs[:, -config.n_positions:]

        with torch.no_grad():
            outputs = model.generate(
                inputs,
                attention_mask=(inputs != tokenizer.pad_token_id),
                position_ids=position_ids.unsqueeze(0),  # Explicit position IDs
                max_new_tokens=256,
                temperature=0.7,
                top_p=0.9,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id,
            )

        new_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        generated_text += " " + new_text[len(prompt):]
        word_count = count_words(generated_text)

        inputs = tokenizer.encode(generated_text, return_tensors="pt", truncation=True, max_length=config.n_positions)

        if word_count >= max_length:
            break

    if word_count > max_length:
        words = generated_text.split()
        generated_text = ' '.join(words[:max_length])

    title = "Untitled Story"
    return title, generated_text

if __name__ == "__main__":
    title, story = generate_story(
        prompt="Once upon a time in a small village.",
        model_dir="/Users/sgiannuzzi/Desktop/thesis/generator-from-scratch/fine_tuned_gpt2"
    )
    print(f"Title: {title}\n")
    print(story)
