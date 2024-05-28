import streamlit as st
import base64
import subprocess
from TTS.api import TTS
from IPython.display import Audio, display

# Function to upload video
def upload_video():
    uploaded = st.file_uploader("Upload Video", type=["mp4", "avi", "mov"])
    if uploaded is not None:
        with open("uploaded_video.mp4", "wb") as f:
            f.write(uploaded.read())
        return "uploaded_video.mp4"
    return None

# Function to resize video
def resize_video(filename):
    output_filename = f"resized_{filename}"
    cmd = f"ffmpeg -i {filename} -vf scale=-1:720 {output_filename}"
    subprocess.run(cmd, shell=True)
    return output_filename

# Function to transcribe audio
def transcribe_audio(audio_file):
    ffmpeg_command = f"ffmpeg -i '{audio_file}' -acodec pcm_s24le -ar 48000 -q:a 0 -map a -y 'output_audio.wav'"
    subprocess.run(ffmpeg_command, shell=True)
    model = whisper.load_model("base")
    result = model.transcribe("output_audio.wav")
    return result["text"], result["language"]

# Function to translate text
def translate_text(text, target_language):
    target_language_code = language_mapping[target_language]
    translator = Translator()
    translated_text = translator.translate(text, dest=target_language_code).text
    return translated_text

# Function to synthesize translated text
def synthesize_text(text, target_language):
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=True).to("cuda")
    tts.tts_to_file(text, speaker_wav='output_audio.wav', file_path="output_synth.wav", language=target_language)
    audio_widget = Audio(filename="output_synth.wav", autoplay=False)
    return audio_widget

# Streamlit app
def main():
    st.title("AI Dubbing System")

    # Upload video
    st.write("Step 1: Upload Video")
    video_file = upload_video()
    if video_file is None:
        st.warning("Please upload a video.")
        return

    # Resize video
    st.write("Step 2: Resize Video (Optional)")
    resize_checkbox = st.checkbox("Resize to 720p (better results)")
    if resize_checkbox:
        video_file = resize_video(video_file)

    # Transcribe audio
    st.write("Step 3: Transcribe Audio")
    text, language = transcribe_audio(video_file)
    st.write("Audio Text:", text)

    # Translate text
    st.write("Step 4: Translate Text")
    target_language = st.selectbox("Select Target Language", ["English", "Spanish", "French", "German", "Italian"])
    translated_text = translate_text(text, target_language)
    st.write("Translated Text:", translated_text)

    # Synthesize translated text
    st.write("Step 5: Synthesize Translated Text")
    audio_widget = synthesize_text(translated_text, target_language)
    st.write("Audio Synthesized:", audio_widget)

    # Download synthesized video
    st.write("Step 6: Download Dubbed Video")
    download_button = st.button("Download Dubbed Video")
    if download_button:
        st.markdown(get_binary_file_downloader_html("output_synth.wav", "Download Dubbed Video"), unsafe_allow_html=True)

# Helper function to download dubbed video
def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="{bin_file}">{file_label}</a>'
    return href

if __name__ == "__main__":
    main()
