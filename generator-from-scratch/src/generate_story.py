from openai import OpenAI

def generate_story(prompt="Write a short story.", min_length=1000, max_length=7500):
    # Instantiate the OpenAI client
    client = OpenAI(api_key="_____")

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a creative writer."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=max_length,
        temperature=0.7,
        top_p=0.9,
        frequency_penalty=0,
        presence_penalty=0.6,
    )

    # Extract the generated text
    generated_text = response.choices[0].message.content

    # No title extraction needed since we are not providing one
    title = "Untitled"

    return title, generated_text
