import streamlit as st
import google.generativeai as genai
import os
import time
from dotenv import load_dotenv
import tempfile

# Load environment variables
load_dotenv()

# Configure Gemini API
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

st.set_page_config(page_title="Video Analyzer", page_icon="📹")

st.title("📹 Video Analyzer with Gemini")

if not api_key:
    st.warning("Please set your GOOGLE_API_KEY in the .env file.")
    st.stop()

uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "mov", "avi", "mkv"])

if uploaded_file is not None:
    # Display the video
    st.video(uploaded_file)

    if st.button("Analyze Video"):
        with st.spinner("Processing video..."):
            try:
                # Save uploaded file to a temporary file
                tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') 
                tfile.write(uploaded_file.read())
                video_path = tfile.name
                tfile.close()

                st.info("Uploading video to Gemini...")
                video_file = genai.upload_file(path=video_path)
                
                # Wait for the file to be processed
                while video_file.state.name == "PROCESSING":
                    time.sleep(2)
                    video_file = genai.get_file(video_file.name)

                if video_file.state.name == "FAILED":
                    st.error("Video processing failed.")
                else:
                    st.info("Video uploaded successfully. Generating description...")
                    
                    # Create the prompt
                    prompt = "Describe what is happening in this video in detail."
                    
                    # Choose a model that supports video
                    model = genai.GenerativeModel(model_name="gemini-2.0-flash")
                    
                    # Generate content
                    response = model.generate_content([video_file, prompt])
                    
                    st.subheader("Analysis Result:")
                    st.markdown(response.text)
                    
                    # Clean up: delete the file from Gemini to save storage/quota
                    # genai.delete_file(video_file.name) # Optional: delete after use

            except Exception as e:
                st.error(f"An error occurred: {e}")
            finally:
                # Clean up local temp file
                if os.path.exists(video_path):
                    os.remove(video_path)
