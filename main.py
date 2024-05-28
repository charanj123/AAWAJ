import streamlit as st
from ai_dubbing_module import dub_video

# Function to dub the video
def dub_video_with_language(video_file, language):
    # Call your AI dubbing function passing the video file and language
    # Replace this with your actual AI dubbing code
    dub_video(video_file, language)

# Main function to run the Streamlit app
def main():
    st.title("AI Dubbing System")

    # Upload video file
    uploaded_file = st.file_uploader("Upload Video File", type=["mp4", "avi", "mov"])

    if uploaded_file is not None:
        st.video(uploaded_file)

        # Language selection
        language = st.selectbox("Select Dubbing Language", ["English", "Spanish", "French"])

        # Dub video button
        if st.button("Dub Video"):
            # Dub the video with the selected language
            dub_video_with_language(uploaded_file, language)
            st.success("Video dubbed successfully!")

            # Download dubbed video button
            st.markdown(get_binary_file_downloader_html("dubbed_video.mp4", "Download Dubbed Video"), unsafe_allow_html=True)

# Helper function to download the dubbed video
def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="{bin_file}">{file_label}</a>'
    return href

if __name__ == "__main__":
    main()
