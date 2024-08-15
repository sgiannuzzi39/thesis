from transformers import GPT2Tokenizer, GPT2LMHeadModel  # Import necessary components

def generate_story(prompt, max_length=300):
    tokenizer = GPT2Tokenizer.from_pretrained("./fine_tuned_gpt2")
    model = GPT2LMHeadModel.from_pretrained("./fine_tuned_gpt2")

    inputs = tokenizer.encode(prompt, return_tensors="pt")
    attention_mask = tokenizer(prompt, return_tensors="pt").attention_mask

    outputs = model.generate(
        inputs,
        attention_mask=attention_mask,
        max_length=max_length,
        num_return_sequences=1,
        no_repeat_ngram_size=2,
        do_sample=True,
        top_k=50,
        top_p=0.95,
        temperature=0.7,
        num_beams=5,  # Using beam search with 5 beams
        early_stopping=True
    )

    return tokenizer.decode(outputs[0], skip_special_tokens=True)
