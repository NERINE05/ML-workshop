import streamlit as st
import cohere
from gtts import gTTS
import os
import tempfile
from io import BytesIO

# Initialize Cohere API client with your API key
api_key = 'v3MveYurFYCrCrS4UnazRQ7yqkHreNXXuluBk4cm'  # Replace this with your actual Cohere API key
co = cohere.Client(api_key)

# Function to generate text using Cohere
def generate_text(prompt: str) -> str:
    response = co.generate(
        model='command-xlarge-20221108',  # Replace with a valid model
        prompt=prompt,
        max_tokens=100,  # You can adjust the max length of the generated text
        temperature=0.7  # Adjust randomness if needed
    )
    return response.generations[0].text.strip()

# Function to convert text to speech
def text_to_speech(text: str) -> BytesIO:
    # Convert text to speech using gTTS
    tts = gTTS(text, lang='en')
    # Save speech to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
        tts.save(tmp_file.name)
        tmp_file.seek(0)  # Rewind the file to the beginning
        return tmp_file.name

# Streamlit app
def main():
    st.title("Text-to-Speech with Cohere & Streamlit")

    # Text input for generating text (if needed)
    text_input = st.text_area("Enter Text or a Prompt", height=150)

    # Generate button for text-to-speech
    if st.button("Generate Speech"):
        if text_input:
            # If text is entered, use that directly, otherwise generate text
            generated_text = text_input  # Use entered text directly

            # Convert the text to speech and provide download link
            audio_file = text_to_speech(generated_text)
            audio_path = audio_file  # Path to the generated audio file
            
            # Provide a downloadable link to the audio file
            st.audio(audio_path, format="audio/mp3")
        else:
            st.warning("Please enter some text or a prompt.")

if __name__ == "__main__":
    main()
