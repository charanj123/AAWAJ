import streamlit as st
import subprocess
import base64
import os

# Function to upload video
def upload_video():
    uploaded_file = st.file_uploader("Upload Video", type=["mp4", "avi", "mov"])
    if uploaded_file is not None:
        return uploaded_file
    return None

# Function to resize video
def resize_video(filename):
    output_filename = f"resized_{filename}"
    cmd = f"ffmpeg -i {filename} -vf scale=-1:720 {output_filename}"
    subprocess.run(cmd, shell=True)
    return output_filename

# Function to dub the video
def dub_video(video_file, language):
    # Placeholder code to simulate dubbing
    # Here, we can simply return the input video path
    return video_file

# Function to run inference and generate video
def generate_video(video_file, language):
    if video_file:
        # Placeholder for dubbed video path (replace with actual logic)
        dubbed_video_path = "path_to_dubbed_video.mp4"
        
        # Resize the video if necessary
        if resize_to_720p:
            dubbed_video_path = resize_video(dubbed_video_path)
        
        # Debugging: Print the value of dubbed_video_path
        print("Dubbed Video Path:", dubbed_video_path)

        # Display the dubbed video
        st.success("Video uploaded successfully!")
        st.video(dubbed_video_path, format="video/mp4")



# Main function to run the Streamlit app
def main():
    st.title("AI Dubbing System")

    # Checkbox to resize video
    global resize_to_720p
    resize_to_720p = st.checkbox("Resize to 720p (better results)")

    # Upload video
    uploaded_file = upload_video()

    # Language selection
    language = st.selectbox("Select Dubbing Language", ["English", "Spanish", "French"])

    # Button to run inference and generate video
    if st.button("Generate Dubbed Video"):
        generate_video(uploaded_file, language)

if __name__ == "__main__":
    main()
