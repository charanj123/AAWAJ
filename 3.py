import streamlit as st
import os
from googletrans import Translator
from TTS.api import TTS
import subprocess
from google.colab import files

# Define the Streamlit app title and icon
app_title = "Video Translation & Voice Synthesis"
app_icon = "▶️"

# Set page configuration
st.set_page_config(
    page_title=app_title,
    page_icon=app_icon,
    layout="wide",
    initial_sidebar_state="expanded",
)

# Function to upload video
def upload_video():
    uploaded_file = st.file_uploader("Upload a video", type=["mp4", "avi"])
    if uploaded_file is not None:
        with open(os.path.join("uploaded_videos", uploaded_file.name), "wb") as f:
            f.write(uploaded_file.read())
        st.success("Video uploaded successfully!")
        return os.path.join("uploaded_videos", uploaded_file.name)
    return None

# Function to extract audio text from video
def extract_audio_text(video_path):
    # Extract audio from video
    audio_path = "output_audio.wav"
    ffmpeg_command = f"ffmpeg -i '{video_path}' -acodec pcm_s24le -ar 48000 -q:a 0 -map a -y '{audio_path}'"
    subprocess.run(ffmpeg_command, shell=True)

    # Perform text extraction (you can replace this with Whisper or any other method)
    # For demonstration purposes, let's assume we have extracted text from the audio
    audio_text = "This is a sample text extracted from the audio of the video."
    return audio_text

# Function for translation
def translate_text(text, target_language):
    translator = Translator()
    translated_text = translator.translate(text, dest=target_language).text
    return translated_text

# Function for voice synthesis
def synthesize_voice(text, language):
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=True).to("cuda")
    tts.tts_to_file(text, speaker_wav='output_audio.wav', file_path="output_synth.wav", language=language)

# Sidebar: Language selection
st.sidebar.subheader("Language Selection")
target_language = st.sidebar.selectbox(
    "Select Target Language:",
    ('English', 'Spanish', 'French', 'German', 'Italian', 'Portuguese', 'Polish', 'Turkish', 'Russian', 'Dutch', 'Czech', 'Arabic', 'Chinese (Simplified)')
)

# Main content
st.title(app_title)

# Step 1: Upload video
st.header("Step 1: Upload Video")
video_path = upload_video()
if video_path:
    st.video(video_path)

    # Step 2: Extract audio text
    st.header("Step 2: Extract Audio Text")
    audio_text = extract_audio_text(video_path)
    st.write("Extracted Audio Text:", audio_text)

    # Step 3: Translate text
    st.header("Step 3: Translate Text")
    translated_text = translate_text(audio_text, target_language)
    st.write("Translated Text:", translated_text)

    # Step 4: Synthesize voice
    st.header("Step 4: Synthesize Voice")
    synthesize_voice(translated_text, target_language)

    # Download synthesized audio
    st.subheader("Download Synthesized Audio")
    st.audio("output_synth.wav", format="audio/wav")

st.sidebar.markdown("---")
st.sidebar.write("Note: Lip-syncing functionality is not available in this demo.")
