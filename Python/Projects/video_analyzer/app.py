import streamlit as st
from google import genai
import os
import time
import logging
from dotenv import load_dotenv
import tempfile
from contextlib import contextmanager
from dataclasses import dataclass
from functools import wraps

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# Environment-based configuration
@dataclass
class AppConfig:
    """Configuration class for the Video Analyzer application."""

    model_name: str = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
    default_prompt: str = os.getenv(
        "GEMINI_PROMPT", "Describe what is happening in this video in detail."
    )
    max_video_size_mb: int = int(os.getenv("MAX_VIDEO_SIZE_MB", "100"))
    api_timeout: float = float(os.getenv("API_TIMEOUT", "30.0"))
    file_processing_poll_interval: float = float(
        os.getenv("FILE_PROCESSING_POLL_INTERVAL", "2.0")
    )
    max_api_retries: int = int(os.getenv("MAX_API_RETRIES", "3"))


# Custom exception classes for better error handling
class VideoAnalysisError(Exception):
    """Base exception for video analysis errors."""

    pass


class VideoUploadError(VideoAnalysisError):
    """Exception raised for video upload failures."""

    pass


class VideoProcessingError(VideoAnalysisError):
    """Exception raised when video processing fails."""

    pass


class APIGenerationError(VideoAnalysisError):
    """Exception raised when API content generation fails."""

    pass


class ConfigurationError(VideoAnalysisError):
    """Exception raised for configuration errors."""

    pass


# Error handling decorator


def handle_video_errors(func):
    """Decorator to handle video analysis errors with proper logging and user feedback."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except VideoUploadError as e:
            logger.error(f"Video upload failed: {str(e)}")
            st.error(f"Video upload failed: {str(e)}")
            raise
        except VideoProcessingError as e:
            logger.error(f"Video processing failed: {str(e)}")
            st.error(f"Video processing failed: {str(e)}")
            raise
        except APIGenerationError as e:
            logger.error(f"Content generation failed: {str(e)}")
            st.error(f"Content generation failed: {str(e)}")
            raise
        except ConfigurationError as e:
            logger.error(f"Configuration error: {str(e)}")
            st.error(f"Configuration error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in {func.__name__}: {str(e)}")
            st.error(f"An unexpected error occurred: {str(e)}")
            raise VideoAnalysisError(f"Analysis failed: {str(e)}")

    return wrapper


# Resource management
@contextmanager
def temp_video_file(uploaded_file):
    """Context manager for temporary video files with auto-cleanup."""
    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tfile:
            # Validate file size
            uploaded_file.seek(0, 2)  # Seek to end
            file_size_mb = uploaded_file.tell() / (1024 * 1024)
            uploaded_file.seek(0)  # Seek back to start

            if file_size_mb > 100:  # Using config value
                raise VideoUploadError(
                    f"Video file too large: {file_size_mb:.2f}MB (max 100MB)"
                )

            tfile.write(uploaded_file.read())
            temp_path = tfile.name

        yield temp_path

    finally:
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
                logger.debug(f"Cleaned up temporary file: {temp_path}")
            except Exception as e:
                logger.warning(f"Failed to cleanup temp file {temp_path}: {e}")


# API retry logic


def with_retry(max_retries: int, delay: float):
    """Decorator to retry API calls with exponential backoff."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries:
                        logger.warning(
                            f"Attempt {attempt + 1} failed, retrying in "
                            f"{delay * (2 ** attempt)}s..."
                        )
                        time.sleep(delay * (2**attempt))
                    else:
                        logger.error(f"All {max_retries + 1} attempts failed")
            raise last_exception

        return wrapper

    return decorator


# Configuration validation


def validate_config(config: AppConfig) -> None:
    """Validate application configuration."""
    if not config.model_name:
        raise ConfigurationError("Model name cannot be empty")

    if not config.default_prompt:
        raise ConfigurationError("Default prompt cannot be empty")

    if config.max_video_size_mb <= 0:
        raise ConfigurationError("Max video size must be positive")

    if config.api_timeout <= 0:
        raise ConfigurationError("API timeout must be positive")


# Load environment variables and configuration
load_dotenv()

try:
    config = AppConfig()
    validate_config(config)
    logger.info(
        f"Application configuration loaded: model={config.model_name}, "
        f"max_size={config.max_video_size_mb}MB"
    )
except ConfigurationError as e:
    logger.error(f"Configuration error: {str(e)}")
    st.error(f"Configuration error: {str(e)}")
    st.stop()

st.set_page_config(page_title="Video Analyzer", page_icon="📹")

st.title("📹 Video Analyzer with Gemini")

# Display configuration status (development/debugging)
if st.sidebar.checkbox("Show Debug Info", value=False):
    with st.sidebar.expander("Configuration Details"):
        st.write(f"Model: {config.model_name}")
        st.write(f"Max Video Size: {config.max_video_size_mb}MB")
        st.write(f"API Timeout: {config.api_timeout}s")

if not os.getenv("GOOGLE_API_KEY"):
    st.warning("Please set your GOOGLE_API_KEY in the .env file.")
    st.stop()


# Gemini API client configuration
try:
    # Initialize Google Gen AI client
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

    @st.cache_data
    def get_available_models():
        """Get available Gemini models for video analysis."""
        try:
            models = client.models.list()
            video_models = [
                model.name
                for model in models
                if "video" in model.supported_generation_methods
            ]
            return video_models
        except Exception as e:
            logger.error(f"Failed to get available models: {str(e)}")
            return ["gemini-2.0-flash"]  # fallback

    def upload_file(video_path: str):
        """Upload video file to Gemini."""
        try:
            return client.files.upload_file(path=video_path)
        except Exception as e:
            logger.error(f"Video upload failed: {str(e)}")
            raise VideoUploadError(f"Failed to upload video: {str(e)}")

    def get_file(file_name: str):
        """Get uploaded file status from Gemini."""
        try:
            return client.files.get(name=file_name)
        except Exception as e:
            logger.error(f"Failed to get file status: {str(e)}")
            raise

    def delete_file(file_name: str):
        """Delete file from Gemini to save storage."""
        try:
            client.files.delete(name=file_name)
        except Exception as e:
            logger.warning(f"Failed to delete file from Gemini: {str(e)}")

    def generate_content(prompt_parts, model_name="gemini-2.0-flash"):
        """Generate content using Gemini."""
        try:
            model = genai.GenerativeModel(model_name=model_name)
            response = model.generate_content(prompt_parts)
            return response.text
        except Exception as e:
            logger.error(f"Content generation failed: {str(e)}")
            raise APIGenerationError(f"Failed to generate content: {str(e)}")

except Exception as e:
    logger.error(f"Failed to initialize Gemini client: {str(e)}")
    st.error(f"Application initialization failed: {str(e)}")
    st.stop()


uploaded_file = st.file_uploader(
    "Upload a video file",
    type=["mp4", "mov", "avi", "mkv"],
    help=f"Maximum file size: {config.max_video_size_mb}MB",
)

if uploaded_file is not None:
    # Display the video
    st.video(uploaded_file)

    # Display file info
    uploaded_file.seek(0, 2)
    file_size = uploaded_file.tell()
    uploaded_file.seek(0)

    st.write(f"📁 File size: {file_size / (1024 * 1024):.2f} MB")

    # Model selection (expandable)
    with st.expander("Advanced Options"):
        available_models = get_available_models()
        selected_model = st.selectbox(
            "Gemini Model",
            available_models,
            index=(
                available_models.index(config.model_name)
                if config.model_name in available_models
                else 0
            ),
        )

        custom_prompt = st.text_area(
            "Custom Prompt",
            value=config.default_prompt,
            help="Customize the prompt for video analysis",
        )

        # Display processing options
        poll_interval = st.slider(
            "Polling Interval (seconds)",
            min_value=1.0,
            max_value=10.0,
            value=config.file_processing_poll_interval,
            help="Interval for checking video processing status",
        )

    if st.button("Analyze Video"):
        with st.spinner("Processing video..."):
            try:
                # Use selected model and prompt
                model_name = selected_model
                prompt = custom_prompt

                with temp_video_file(uploaded_file) as video_path:
                    st.info("Uploading video to Gemini...")

                    @with_retry(
                        config.max_api_retries, config.file_processing_poll_interval
                    )
                    def upload_and_analyze():
                        video_file = upload_file(video_path)

                        # Wait for the file to be processed
                        while video_file.state.name == "PROCESSING":
                            time.sleep(config.file_processing_poll_interval)
                            video_file = get_file(video_file.name)

                        if video_file.state.name == "FAILED":
                            raise VideoProcessingError(
                                "Video processing failed on Gemini's side"
                            )

                        st.info(
                            "Video uploaded successfully. Generating description..."
                        )

                        # Create the prompt
                        full_prompt = (
                            f"{prompt}\n\nPlease provide a detailed analysis "
                            "of the video content."
                        )

                        # Choose a model that supports video
                        model = genai.GenerativeModel(model_name=selected_model)

                        # Generate content with timeout
                        response = model.generate_content(
                            [video_file, full_prompt],
                            generation_config={"timeout": config.api_timeout},
                        )

                        return response.text

                    # Generate analysis
                    analysis_result = upload_and_analyze()

                    st.subheader("Analysis Result:")
                    st.markdown(analysis_result)

                    # Add download option
                    st.download_button(
                        label="Download Analysis",
                        data=analysis_result,
                        file_name=f"video_analysis_{uploaded_file.name.split('.')[0]}.txt",
                        mime="text/plain",
                    )

                    # Clean up: delete the file from Gemini to save storage/quota
                    # Note: Uncomment if you want to delete the file
                    # genai.delete_file(video_file.name) # Optional: delete after use

            except VideoAnalysisError:
                # Already handled by decorator
                pass
            except Exception as e:
                logger.error(f"Unexpected error during analysis: {str(e)}")
                st.error(f"An unexpected error occurred during analysis: {str(e)}")
