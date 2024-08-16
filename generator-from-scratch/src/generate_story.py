from transformers import GPT2Tokenizer, GPT2LMHeadModel

def generate_story(prompt):
    tokenizer = GPT2Tokenizer.from_pretrained("./fine_tuned_gpt2")
    model = GPT2LMHeadModel.from_pretrained("./fine_tuned_gpt2")

    inputs = tokenizer.encode(prompt, return_tensors="pt")
    attention_mask = inputs.ne(tokenizer.pad_token_id)

    generated_story = model.generate(
        input_ids=inputs,
        attention_mask=attention_mask,
        max_length=512,
        temperature=0.8,  # Slightly higher temperature for more variability
        top_k=50,         # Top-k sampling
        top_p=0.9,        # Nucleus sampling
        repetition_penalty=1.2,  # Adds a penalty to repeated sequences
        do_sample=True    # Enable sampling
    )

    return tokenizer.decode(generated_story[0], skip_special_tokens=True)
