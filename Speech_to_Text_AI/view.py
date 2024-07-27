from flask import Flask, render_template, request
from gtts import gTTS
import os
import requests
import time

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    input_text = request.form['text']
    
    if input_text:
        translation_direction = request.form.get('translation_direction')  # Get the translation direction from the form
        record_language = request.form.get('recordLanguage')  # Get the language for text recognition
        
        if translation_direction == 'en':  # English to Indonesian translation
            payload = {
                'from': record_language,
                'to': 'en',
                'text': input_text
            }
            lang = 'en'  # Indonesian voice for translation to Indonesian
        elif translation_direction == 'id':  # Indonesian to English translation
            payload = {
                'from': record_language,
                'to': 'id',
                'text': input_text
            }
            lang = 'id'  # English voice for translation to English
        elif translation_direction == 'ja': 
            payload = {
                'from': record_language,
                'to': 'ja',
                'text': input_text
            }
            lang = 'ja'
        elif translation_direction == 'fr': 
            payload = {
                'from': record_language,
                'to': 'fr',
                'text': input_text
            }
            lang = 'fr'
            
        else:
            return render_template('result.html', error_message="Error: Invalid translation direction.")

        url = "https://google-translate113.p.rapidapi.com/api/v1/translator/text"
        headers = {
            'content-type': "application/x-www-form-urlencoded",
            'X-RapidAPI-Key': "3536e48a1emsh500706c020aa762p18d7ccjsn36bf1ef48508",
            'X-RapidAPI-Host': "google-translate113.p.rapidapi.com"
        }

        response = requests.post(url, data=payload, headers=headers)

        if response.status_code == 200:
            translated_text = response.json().get('trans')  # Extract translated text from JSON response
            
            # Generate unique audio file name using timestamp
            timestamp = int(time.time())
            audio_path = f"static/translated_output_{timestamp}.mp3"

            # Generate audio file using gTTS with language-specific voice
            tts = gTTS(text=translated_text, lang=lang)
            tts.save(audio_path)

            # Send the path to the generated speech file to the template
            return render_template('result.html', translation=translated_text, audio_path=audio_path)
        else:
            error_message = f"Error: {response.reason}"
            return render_template('result.html', error_message=error_message)
    else:
        return render_template('result.html', error_message="Error: No input text provided.")

if __name__ == "__main__":
    app.run(debug=True)
