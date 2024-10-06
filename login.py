import streamlit as st
import main
import datetime
import base64

st.set_page_config(
    page_title="K-Means Mall Clustering",
    page_icon="data-analysis.png"
)


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

login_credentials = {
    "Usernames": ["FranklinNthenya1", "ElvisAsiki2", "RooneyWanjohi3", "MelvynNyakoeNyasani4", "AllanVikiru"],
    "Passwords": ["franko@123", "elvo@123", "rooney@123", "melo@123", "viki@123"]
}


def checkCreds(username, password):
    if username in login_credentials["Usernames"]:
        index = login_credentials["Usernames"].index(username)
        if password in login_credentials["Passwords"][index]:
            return True
        else:
            st.error("Invalid passwords")
            return False
    else:
        st.error("Invalid username")
        return False


def login():
    if "tries" not in st.session_state:
        st.session_state.tries = 4
    if "login_success" not in st.session_state:
        st.session_state.login_success = False

    if st.session_state.tries > 1:
        username = st.text_input("Username: ")
        password = st.text_input("Password: ", type="password")
        if st.button("login"):
            if checkCreds(username, password):
                st.session_state.login_success = True
                st.success("Login successful")
                st.session_state.tries = 4

                return True
            else:
                st.session_state.tries -= 1
                if st.session_state.tries > 0:
                    st.warning(f"{st.session_state.tries} attempts remaining")
                else:
                    st.error("Access Denied")
                    st.stop()
    else:
        st.error("Access Denied")


if "login_success" in st.session_state and st.session_state.login_success:
    main.main()

else:
    st.warning("Please Login to access site")
    login()
