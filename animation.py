import streamlit as st
import base64

def set_background(video_file_path):
    """Set the background video using HTML and CSS."""
    with open(video_file_path, "rb") as video_file:
        video_base64 = base64.b64encode(video_file.read()).decode()  # Convert video to base64
    page_bg_video = f'''
    <style>
    .st-emotion-cache-13k62yr {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
        overflow: hidden;
    }}
    .st-emotion-cache-13k62yr video {{
        width: 100%;
        height: 100%;
        object-fit: cover; /* Ensures the video covers the entire background */
    }}
    </style>
    <div class="st-emotion-cache-13k62yr">
        <video autoplay loop muted>
            <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
        </video>
    </div>
    '''
    st.markdown(page_bg_video, unsafe_allow_html=True)

# Specify the path to your video file
video_file_path = '48569-454825064.mp4'  # Replace with the actual path to your video file

# Set the background video directly from the file
set_background(video_file_path)

# Display some content on top of the video
st.title("Welcome to My App")
st.write("This video is set as the background.")
