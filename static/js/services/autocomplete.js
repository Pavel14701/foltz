document.addEventListener('DOMContentLoaded', function() {
    setupAutocomplete('title');
    setupAutocomplete('category');
    setupAutocomplete('tag');
});

function setupAutocomplete(fieldType) {
    const input = document.getElementById(fieldType);
    const suggestionsBox = document.getElementById(fieldType + '-suggestions');

    input.addEventListener('input', function() {
        const query = this.value;

        if (query.length > 2) {
            fetch(`/services/autocomplete/?type=${fieldType}&term=${query}`)
                .then(response => response.json())
                .then(data => {
                    suggestionsBox.innerHTML = '';
                    data.forEach(item => {
                        const div = document.createElement('div');
                        div.textContent = item.value;
                        div.classList.add('suggestion-item');
                        suggestionsBox.appendChild(div);

                        div.addEventListener('click', function() {
                            input.value = this.textContent;
                            suggestionsBox.innerHTML = '';
                        });
                    });
                })
                .catch(error => console.error('Error:', error));
        } else {
            suggestionsBox.innerHTML = '';
        }
    });

    document.addEventListener('click', function(e) {
        if (!input.contains(e.target)) {
            suggestionsBox.innerHTML = '';
        }
    });
}