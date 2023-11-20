from flask import Flask, render_template, request
from pathlib import Path
from openai import OpenAI
import uuid

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ''
    audio_file = None
    text_input = ''
    selected_voice = 'echo'  # Valor padrão para a voz
    selected_quality = 'tts-1'  # Valor padrão para a qualidade do áudio


    if request.method == 'POST':
        text_input = request.form['text_input']
        selected_voice = request.form.get('voice_select', 'echo')  # Captura a voz selecionada
        selected_quality = request.form.get('quality_select', 'tts-1')  # Captura a qualidade selecionada
        
        client = OpenAI(api_key='COLOCAR_API_KEY')
        audio_filename = f"speech_{uuid.uuid4().hex}.mp3"
        speech_file_path = Path(__file__).parent / "static" / audio_filename
        response = client.audio.speech.create(
            model=selected_quality,
            voice=selected_voice,  # Usa a voz selecionada
            input=text_input
        )
        response.stream_to_file(speech_file_path)
        
        message = 'Arquivo de áudio criado com sucesso.'
        audio_file = audio_filename

    return render_template('index.html', message=message, audio_file=audio_file, text_input=text_input, selected_voice=selected_voice)

if __name__ == '__main__':
    app.run(debug=True)
