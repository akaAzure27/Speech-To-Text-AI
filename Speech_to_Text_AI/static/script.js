const outputDiv = document.getElementById('inputText');
const startButton = document.getElementById('startButton');
let recognition;

function initializeRecognition(lang) {
    recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition || window.mozSpeechRecognition || window.msSpeechRecognition)();
    recognition.lang = lang;
    recognition.interimResults = false;

    recognition.onstart = function() {
        startButton.textContent = 'Listening...';
    };

    recognition.onend = function() {
        startButton.textContent = 'Start Recording';
    };

    recognition.onresult = function(event) {
        const result = event.results[event.results.length - 1];
        const text = result[0].transcript;
        outputDiv.innerHTML = text; // Set innerHTML to the final recognized text
        
        // Send the recognized text to the server for translation
        translateText(text);
    };

    recognition.onerror = function(event) {
        console.error('Speech recognition error: ' + event.error);
    };
}

document.getElementById('startButton').addEventListener('click', function() {
    var selectedLanguage = document.getElementById('recordLanguage').value;
    if (selectedLanguage === 'en') {
        initializeRecognition('en-US');
        recognition.start();
    } else if (selectedLanguage === 'id') {
        initializeRecognition('id-ID');
        recognition.start();
    }else if (selectedLanguage === 'ja') {
        initializeRecognition('ja');
        recognition.start();
    } 
    else if (selectedLanguage === 'fr') {
        initializeRecognition('fr');
        recognition.start();
    }
});

// Function to send recognized text to the server for translation
function translateText(text) {
    var translationLanguage = document.getElementById('translationLanguage').value;
    var formData = new FormData();
    formData.append('text', text);
    formData.append('translationLanguage', translationLanguage);
    
    fetch('/translate', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // Display translated text or handle response accordingly
        console.log(data);
    })
    .catch(error => console.error('Error:', error));
}
