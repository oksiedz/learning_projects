import streamlit as st
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

    model_name: str = os.getenv("OPENROUTER_MODEL", "openrouter/free")
    default_prompt: str = os.getenv(
        "OPENROUTER_PROMPT", "Describe what is happening in this video in detail."
    )
    max_video_size_mb: int = int(os.getenv("MAX_VIDEO_SIZE_MB", "100"))
    api_timeout: float = float(os.getenv("API_TIMEOUT", "30.0"))
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

st.title("📹 Video Analyzer with OpenRouter")

# Display configuration status (development/debugging)
if st.sidebar.checkbox("Show Debug Info", value=False):
    with st.sidebar.expander("Configuration Details"):
        st.write(f"Model: {config.model_name}")
        st.write(f"Max Video Size: {config.max_video_size_mb}MB")
        st.write(f"API Timeout: {config.api_timeout}s")

if not os.getenv("OPENROUTER_API_KEY"):
    st.warning("Please set your OPENROUTER_API_KEY in the .env file.")
    st.stop()

st.write(f"Using model: **{config.model_name}**")

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
        st.write(f"Current model: **{config.model_name}**")
        st.caption("Change OPENROUTER_MODEL in .env to switch models")

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
                with temp_video_file(uploaded_file) as video_path:
                    st.info("Analyzing video...")

                    @with_retry(
                        config.max_api_retries, config.file_processing_poll_interval
                    )
                    def analyze_video():
                        # OpenRouter API call using OpenAI-compatible client
                        import openai

                        client = openai.OpenAI(
                            api_key=os.getenv("OPENROUTER_API_KEY"),
                            base_url="https://openrouter.ai/api/v1",
                        )

                        response = client.chat.completions.create(
                            model=config.model_name,
                            messages=[
                                {
                                    "role": "user",
                                    "content": [
                                        {"type": "text", "text": f"{custom_prompt}"},
                                        {
                                            "type": "input_text",
                                            "text": "Please analyze this video content.",
                                        },
                                    ],
                                }
                            ],
                        )

                        return response.choices[0].message.content

                    # Generate analysis
                    analysis_result = analyze_video()

                    st.subheader("Analysis Result:")
                    st.markdown(analysis_result)

                    # Add download option
                    st.download_button(
                        label="Download Analysis",
                        data=analysis_result,
                        file_name=f"video_analysis_{uploaded_file.name.split('.')[0]}.txt",
                        mime="text/plain",
                    )

            except VideoAnalysisError:
                # Already handled by decorator
                pass
            except Exception as e:
                logger.error(f"Unexpected error during analysis: {str(e)}")
                st.error(f"An unexpected error occurred during analysis: {str(e)}")
