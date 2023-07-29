const wordList = document.getElementById('word-list');
const containerHeight = wordList.clientHeight;
let words = [];

function fetchWords() {
    fetch('sorted_names.json')
        .then(response => response.json())
        .then(data => {
            words = data;
            updateView();
        })
        .catch(error => console.error('Error fetching words:', error));
}

function updateView() {
    const centerIndex = Math.floor(words.length / 2);
    wordList.innerHTML = '';

    for (let i = 0; i < words.length; i++) {
        const element = document.createElement('li');
        element.textContent = words[i];
        const offset = i - centerIndex;
        const scale = 1 - Math.abs(offset) / 5; // Display about 10 items, center item with max scale
        element.style.opacity = scale.toFixed(2);
        element.style.fontSize = `${scale.toFixed(2)}em`;
        wordList.appendChild(element);
    }
}

window.addEventListener('scroll', updateView);
window.addEventListener('resize', updateView);

fetchWords(); // Fetch words from JSON file and initialize the view
