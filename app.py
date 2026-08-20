import streamlit as st
import os
import time
import glob
from gtts import gTTS
from PIL import Image
import base64
from googletrans import Translator # <--- Usando tu librería googletrans

st.title("Traducción de cuentos")
image = Image.open('Gatoyraton.JPG')
st.image(image, width=350)
with st.sidebar:
    st.subheader("Escriba y/o selecciona texto para ser escuchado.")

try:
    os.mkdir("temp")
except:
    pass

st.subheader("Una pequeña Fábula.")
st.write('¡Ay! -dijo el ratón-. El mundo se hace cada día más pequeño. Al principio era tan grande que le tenía miedo. '  
         ' Corría y corría y por cierto que me alegraba ver esos muros, a diestra y siniestra, en la distancia. ' 
         ' Pero esas paredes se estrechan tan rápido que me encuentro en el último cuarto y ahí en el rincón está '  
         ' la trampa sobre la cual debo pasar. Todo lo que debes hacer es cambiar de rumbo dijo el gato...y se lo comió. ' 
         '  '
         ' Franz Kafka.'
        )
            
st.markdown(f"Quieres escucharlo en inglés?, copia el texto")
text = st.text_area("Ingrese El texto a escuchar.")

# Inicializamos el traductor de googletrans
translator = Translator()

def text_to_speech(text):
    # Traduce el texto del español al inglés
    translation = translator.translate(text, src='es', dest='en')
    translated_text = translation.text
    
    # Genera el audio usando el texto traducido y con idioma inglés ('en')
    tts = gTTS(translated_text, lang='en')
    
    try:
        my_file_name = text[0:20].replace(" ", "_")
    except:
        my_file_name = "audio"
        
    tts.save(f"temp/{my_file_name}.mp3")
    return my_file_name, translated_text

if st.button("convertir a Audio"):
    if text.strip():
        result, output_text = text_to_speech(text)
        audio_file = open(f"temp/{result}.mp3", "rb")
        audio_bytes = audio_file.read()
        
        st.markdown(f"## Texto traducido al inglés:")
        st.write(output_text)
        
        st.markdown(f"## Tú audio:")
        st.audio(audio_bytes, format="audio/mp3", start_time=0)

        with open(f"temp/{result}.mp3", "rb") as f:
            data = f.read()

        def get_binary_file_downloader_html(bin_file, file_label='File'):
            bin_str = base64.b64encode(data).decode()
            href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download {file_label}</a>'
            return href
        st.markdown(get_binary_file_downloader_html("audio.mp3", file_label="Audio File"), unsafe_allow_html=True)
    else:
        st.warning("Por favor ingresa un texto antes de convertir.")

def remove_files(n):
    mp3_files = glob.glob("temp/*mp3")
    if len(mp3_files) != 0:
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)
                print("Deleted ", f)

remove_files(7)
