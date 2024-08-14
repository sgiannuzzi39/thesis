document.addEventListener('DOMContentLoaded', () => {
    const numCharactersInput = document.getElementById('num-characters');
    const charactersContainer = document.getElementById('characters-container');
    const storyForm = document.getElementById('story-form');

    // Function to create character input fields
    function createCharacterInputs(numCharacters) {
        charactersContainer.innerHTML = ''; // Clear the container first

        // Loop through and create character input fields
        for (let i = 1; i <= numCharacters; i++) {
            const characterDiv = document.createElement('div');
            characterDiv.className = 'character-input mt-4';

            const nameLabel = document.createElement('label');
            nameLabel.htmlFor = `character${i}-name`;
            nameLabel.textContent = `Character ${i} Name:`;
            nameLabel.className = 'block';

            const nameInput = document.createElement('input');
            nameInput.id = `character${i}-name`;
            nameInput.type = 'text';
            nameInput.className = 'block w-full bg-gray-800 text-white mt-1 p-2';

            const sexLabel = document.createElement('label');
            sexLabel.htmlFor = `character${i}-sex`;
            sexLabel.textContent = `Character ${i} Sex:`;
            sexLabel.className = 'block mt-2';

            const sexSelect = document.createElement('select');
            sexSelect.id = `character${i}-sex`;
            sexSelect.className = 'block w-full bg-gray-800 text-white mt-1 p-2';

            const maleOption = document.createElement('option');
            maleOption.value = 'male';
            maleOption.textContent = 'Male';

            const femaleOption = document.createElement('option');
            femaleOption.value = 'female';
            femaleOption.textContent = 'Female';

            const otherOption = document.createElement('option');
            otherOption.value = 'other';
            otherOption.textContent = 'Other';

            sexSelect.append(maleOption, femaleOption, otherOption);

            characterDiv.append(nameLabel, nameInput, sexLabel, sexSelect);
            charactersContainer.appendChild(characterDiv);
        }
    }

    // Create the initial character input fields
    createCharacterInputs(numCharactersInput.value);

    // Add an event listener for the numCharactersInput to recreate the character input fields
    numCharactersInput.addEventListener('input', () => {
        createCharacterInputs(numCharactersInput.value);
    });

    // Add an event listener for the story form submission
    storyForm.addEventListener('submit', async(e) => {
        e.preventDefault();

        // Get the user's input from the form
        const genre = document.getElementById('genre').value;
        const numCharacters = parseInt(document.getElementById('num-characters').value, 10);
        const readerAge = parseInt(document.getElementById('reader-age').value, 10);

        // Build the characters array with names and sexes
        const characters = [];
        for (let i = 1; i <= numCharacters; i++) {
            const name = document.getElementById(`character${i}-name`).value;
            const sex = document.getElementById(`character${i}-sex`).value;
            characters.push({ name, sex });
        }

        // Build the prompt based on the user's input
        let prompt = `Create a short story in the ${genre} genre for a reader aged ${readerAge}. `;
        prompt += `The story should have ${numCharacters} main character(s): `;
        characters.forEach((char, index) => {
            prompt += `${char.name} (${char.sex})${index === characters.length - 1 ? '.' : ', '}`;
        });
        prompt += '\n\nStory: ';

        // Call the generateStory function and update the generated-story div
        const storyText = await generateStory(prompt);
        document.getElementById('generated-story').innerText = storyText;
    });

});

// Function to call the OpenAI API
// Function to call the OpenAI API
async function generateStory(prompt) {
    const response = await fetch('https://api.openai.com/v1/chat/completions', { // Updated endpoint
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer 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'
        },
        body: JSON.stringify({
            model: 'gpt-3.5-turbo', // Updated model name
            messages: [
                { role: "system", content: "You are a helpful assistant." },
                { role: "user", content: prompt }
            ],
            max_tokens: 1200,
            n: 1,
            stop: null,
            temperature: 1.0,
        }),
    });

    const data = await response.json();
    if (data.choices && data.choices.length > 0) {
        return data.choices[0].message.content;
    } else {
        // Return a default message or an error message to the user
        return 'An error occurred while generating the story. Please try again.';
    }
}