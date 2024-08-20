document.addEventListener('DOMContentLoaded', () => {
    // Fetch author list and populate checkboxes
    fetch('/get-authors')
        .then(response => response.json())
        .then(data => {
            const authorCheckboxes = document.getElementById('author-checkboxes');
            data.authors.forEach(author => {
                const label = document.createElement('label');
                const checkbox = document.createElement('input');
                checkbox.type = 'checkbox';
                checkbox.name = 'author';
                checkbox.value = author;
                label.classList.add('author-label');
                label.appendChild(checkbox);
                label.appendChild(document.createTextNode(author));
                authorCheckboxes.appendChild(label);
            });
        });

    document.getElementById('generateButton').addEventListener('click', function() {
        const selectedAuthors = Array.from(document.querySelectorAll('input[name="author"]:checked'))
            .map(checkbox => checkbox.value);
        const selectedGenres = Array.from(document.querySelectorAll('input[name="genre"]:checked'))
            .map(checkbox => checkbox.value);

        fetch('/generate-story', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    authors: selectedAuthors,
                    genres: selectedGenres
                }),
            })
            .then(response => response.json())
            .then(data => {
                const storyDiv = document.getElementById('story');
                storyDiv.textContent = data.story;
                storyDiv.style.display = 'block'; // Show the story container
            })
            .catch(error => console.error('Error:', error));
    });
});