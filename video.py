import streamlit as st
import os
import new

def dir():
    st.set_page_config(
        page_title="Video Dashboard",
        page_icon="▶️",
        layout="wide",
        initial_sidebar_state="expanded",
    )

def videos():
    # Create a directory to store uploaded videos
    video_folder = "D:\\AWAJ\\video_Directory"
    if not os.path.exists("uploaded_videos"):
        os.makedirs("uploaded_videos")

    # Streamlit app header
    st.sidebar.title("Video Upload and List App")

    # File upload section
    st.sidebar.header("Upload Video")
    uploaded_file = st.sidebar.file_uploader("Choose a video...", type=["mp4", "avi"])

    if uploaded_file is not None:
        with open(os.path.join("uploaded_videos", uploaded_file.name), "wb") as f:
            f.write(uploaded_file.read())
        st.sidebar.success("Video uploaded successfully!")

    # List uploaded videos
    st.header("List of Uploaded Videos")
    video_files = os.listdir("uploaded_videos")
    if not video_files:
        st.info("No videos uploaded yet.")
    else:
        for video_file in video_files:
            video_path = os.path.join("uploaded_videos", video_file)
            st.video(video_path)
            st.caption(video_file)

    # Get a list of video files in the folder
    video_files = [os.path.join(video_folder, file) for file in os.listdir(video_folder) if file.endswith(".mp4")]

    # Display videos in a grid pattern
    if video_files:
        st.subheader("List of Videos")
        num_columns = 5  # Adjust the number of columns

        # Calculate the number of rows
        num_videos = len(video_files)
        num_rows = (num_videos + num_columns - 1) // num_columns

        # Create a grid to display videos
        for i in range(num_rows):
            row_videos = video_files[i * num_columns: (i + 1) * num_columns]
            cols = st.columns(num_columns)
            for j, (col, video_path) in enumerate(zip(cols, row_videos)):
                col.video(video_path, format='video/mp4')
                col.caption(os.path.basename(video_path))
    else:
        st.warning("No video files found in the specified folder.")

def uploadvideos():
        # Streamlit app header
    video_folder = "D:\\AWAJ\\video_Directory"
    if not os.path.exists("uploaded_videos"):
        os.makedirs("uploaded_videos")
    st.title("Video Upload")
    # File upload section
    uploaded_file = st.file_uploader("Choose a video...", type=["mp4", "avi"])

    if uploaded_file is not None:
        with open(os.path.join("uploaded_videos", uploaded_file.name), "wb") as f:
            f.write(uploaded_file.read())
            st.sidebar.success("Video uploaded successfully!")

    new.uid()