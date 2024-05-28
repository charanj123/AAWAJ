import streamlit as st
import subprocess
import os
import whisper
from googletrans import Translator
from TTS.api import TTS
import torch

# Function to resize video
def resize_video(input_path, output_path):
    try:
        cmd = f'ffmpeg -i "{input_path}" -vf scale=-1:720 "{output_path}"'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            st.error(f"Failed to resize video: {result.stderr}")
        return output_path
    except Exception as e:
        st.error(f"Exception during resizing video: {str(e)}")
        return None

# Function to extract audio from video
def extract_audio(video_path, audio_output_path):
    try:
        cmd = f'ffmpeg -i "{video_path}" -acodec pcm_s24le -ar 48000 -q:a 0 -map a -y "{audio_output_path}"'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            st.error(f"Failed to extract audio: {result.stderr}")
            return None
        return audio_output_path
    except Exception as e:
        st.error(f"Exception during extracting audio: {str(e)}")
        return None

# Function to transcribe audio using Whisper
def transcribe_audio(audio_path):
    try:
        model = whisper.load_model("base")
        result = model.transcribe(audio_path)
        return result["text"], result["language"]
    except Exception as e:
        st.error(f"Exception during transcribing audio: {str(e)}")
        return None, None

# Function to translate text using Google Translate
def translate_text(text, src_language, target_language):
    try:
        translator = Translator()
        translated = translator.translate(text, src=src_language, dest=target_language)
        return translated.text
    except Exception as e:
        st.error(f"Exception during translating text: {str(e)}")
        return None

# Function to generate audio from text using TTS
def generate_audio(translated_text, target_language_code, selected_speaker):
    try:
        tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=True)
        tts.to("cuda" if torch.cuda.is_available() else "cpu")  # Use GPU if available
        data = tts.tts(translated_text, speaker=selected_speaker, language=target_language_code)
        output_path = "output_synth.wav"
        tts.save_wav(data, output_path)
        return output_path
    except Exception as e:
        st.error(f"Exception during generating audio: {str(e)}")
        return None

# Main function for the Streamlit app
def uid():
    st.title("Wav2Lip Inference Command Runner with Translation")

    if 'uploaded_file_path' not in st.session_state:
        st.session_state.uploaded_file_path = None

    if 'extracted_audio_path' not in st.session_state:
        st.session_state.extracted_audio_path = None

    if 'whisper_text' not in st.session_state:
        st.session_state.whisper_text = None

    if 'translated_text' not in st.session_state:
        st.session_state.translated_text = None

    st.header("Video Upload")
    uploaded_file = st.file_uploader("Upload Video", type=["mp4", "mov", "avi"])

    resize_to_720p = st.checkbox("Resize to 720p (better results)", value=False)

    if uploaded_file is not None:
        video_path = os.path.join("temp", uploaded_file.name)
        os.makedirs("temp", exist_ok=True)
        with open(video_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"Uploaded {uploaded_file.name}")
        st.session_state.uploaded_file_path = video_path

        if resize_to_720p:
            resized_video_path = os.path.join("temp", f"resized_{uploaded_file.name}")
            resized_video_path = resize_video(video_path, resized_video_path)
            if resized_video_path:
                st.success(f"Resized video saved as {resized_video_path}")
                st.session_state.uploaded_file_path = resized_video_path

    if st.session_state.uploaded_file_path:
        st.header("Audio Extraction and Transcription")
        if st.button("Extract Audio and Transcribe"):
            audio_output_path = os.path.join("temp", "output_audio.wav")
            extracted_audio_path = extract_audio(st.session_state.uploaded_file_path, audio_output_path)

            if extracted_audio_path and os.path.exists(extracted_audio_path):
                st.success(f"Extracted audio saved as {extracted_audio_path}")
                st.session_state.extracted_audio_path = extracted_audio_path

                # Provide download link for the extracted audio
                with open(extracted_audio_path, "rb") as file:
                    st.download_button(
                        label="Download Extracted Audio",
                        data=file,
                        file_name="extracted_audio.wav",
                        mime="audio/wav"
                    )

    if st.session_state.extracted_audio_path:
        st.header("Transcription and Translation")
        language_options = [
            "English", "Spanish", "French", "German", "Italian", "Portuguese", "Polish", 
            "Turkish", "Russian", "Dutch", "Czech", "Arabic", "Chinese (Simplified)"
        ]
        target_language = st.selectbox("Select target language for translation", language_options)
        language_mapping = {
            'English': 'en', 'Spanish': 'es', 'French': 'fr', 'German': 'de', 
            'Italian': 'it', 'Portuguese': 'pt', 'Polish': 'pl', 'Turkish': 'tr', 
            'Russian': 'ru', 'Dutch': 'nl', 'Czech': 'cs', 'Arabic': 'ar', 
            'Chinese (Simplified)': 'zh-cn'
        }
        target_language_code = language_mapping[target_language]

        if st.button("Transcribe and Translate"):
            whisper_text, whisper_language = transcribe_audio(st.session_state.extracted_audio_path)
            if whisper_text and whisper_language:
                st.write("Audio text:", whisper_text)
                st.write("Detected language:", whisper_language)
                st.session_state.whisper_text = whisper_text

                translated_text = translate_text(whisper_text, whisper_language, target_language_code)
                if translated_text:
                    st.write("Translated text:", translated_text)
                    st.session_state.translated_text = translated_text
            else:
                st.error("Transcription failed. Please check the logs for more details.")

    if st.session_state.translated_text:
        st.header("Text-to-Speech (TTS)")
        try:
            tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=True)
            tts.to("cuda" if torch.cuda.is_available() else "cpu")  # Use GPU if available
            speakers = getattr(tts, 'speakers', None)
            if speakers:
                selected_speaker = st.selectbox("Select Speaker", speakers)
            else:
                selected_speaker = None
            if st.button("Generate Audio"):
                audio_path = generate_audio(st.session_state.translated_text, target_language_code, selected_speaker)
                if audio_path and os.path.exists(audio_path):
                    st.audio(audio_path)
                    st.success(f"Generated audio saved as {audio_path}")
        except Exception as e:
            st.error(f"Exception during generating audio: {str(e)}")

    if st.session_state.uploaded_file_path:
        # Provide download link for the uploaded video
        with open(st.session_state.uploaded_file_path, "rb") as file:
            st.download_button(
                label="Download Uploaded Video",
                data=file,
                file_name=os.path.basename(st.session_state.uploaded_file_path),
                mime="video/mp4"
            )

