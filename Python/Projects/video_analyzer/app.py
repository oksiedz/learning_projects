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

    provider: str = os.getenv(
        "AI_PROVIDER",
        "gemini" if os.getenv("GEMINI_API_KEY") else "openrouter",
    )
    model_name: str = os.getenv(
        "OPENROUTER_MODEL", "openrouter/free"
    )
    default_prompt: str = os.getenv(
        "OPENROUTER_PROMPT", "Describe what is happening in this video in detail."
    )
    max_video_size_mb: int = int(os.getenv("MAX_VIDEO_SIZE_MB", "100"))
    api_timeout: float = float(os.getenv("API_TIMEOUT", "30.0"))
    max_api_retries: int = int(os.getenv("MAX_API_RETRIES", "3"))
    file_processing_poll_interval: float = float(
        os.getenv("FILE_PROCESSING_POLL_INTERVAL", "1.0")
    )


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

            if file_size_mb > config.max_video_size_mb:
                raise VideoUploadError(
                    f"Video file too large: {file_size_mb:.2f}MB "
                    f"(max {config.max_video_size_mb}MB)"
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
    if config.provider not in ("openrouter", "gemini"):
        raise ConfigurationError(
            f"Provider must be 'openrouter' or 'gemini', got: {config.provider}"
        )
    if config.provider == "openrouter" and not config.model_name:
        raise ConfigurationError("Model name cannot be empty")
    if not config.default_prompt:
        raise ConfigurationError("Default prompt cannot be empty")
    if config.max_video_size_mb <= 0:
        raise ConfigurationError("Max video size must be positive")
    if config.api_timeout <= 0:
        raise ConfigurationError("API timeout must be positive")


def _analyze_with_openrouter(uploaded_file, custom_prompt, config):
    """Analyze video using OpenRouter API."""
    import base64
    import openai

    client = openai.OpenAI(
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1",
    )

    # Read the uploaded video and encode it as base64
    uploaded_file.seek(0)
    video_bytes = uploaded_file.read()
    video_b64 = base64.b64encode(video_bytes).decode("utf-8")
    mime_type = uploaded_file.type or "video/mp4"

    response = client.chat.completions.create(
        model=config.model_name,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": f"{custom_prompt}"},
                    {
                        "type": "video_url",
                        "video_url": {
                            "url": f"data:{mime_type};base64,{video_b64}"
                        },
                    },
                ],
            }
        ],
    )

    return response.choices[0].message.content


def _analyze_with_gemini(uploaded_file, custom_prompt, config):
    """Analyze video using Google Gemini API."""
    import base64
    import mimetypes
    import time

    from google.genai import types as genai_types
    from google import genai

    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    model_name = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

    # Read the uploaded video
    uploaded_file.seek(0)
    video_bytes = uploaded_file.read()
    mime_type = (
        uploaded_file.type
        or mimetypes.guess_type(uploaded_file.name)[0]
        or "video/mp4"
    )

    # Upload the video file to Gemini
    video_part = genai_types.Part.from_bytes(
        data=video_bytes,
        mime_type=mime_type,
    )

    response = client.models.generate_content(
        model=model_name,
        contents=[custom_prompt, video_part],
    )

    return response.text


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

st.title("📹 Video Analyzer")

# Display configuration status (development/debugging)
if st.sidebar.checkbox("Show Debug Info", value=False):
    with st.sidebar.expander("Configuration Details"):
        st.write(f"Provider: {config.provider}")
        if config.provider == "gemini":
            st.write(f"Model: {os.getenv('GEMINI_MODEL', 'gemini-3.8-flash')}")
        else:
            st.write(f"Model: {config.model_name}")
        st.write(f"Max Video Size: {config.max_video_size_mb}MB")
        st.write(f"API Timeout: {config.api_timeout}s")

# Check required API key based on provider
if config.provider == "gemini":
    if not os.getenv("GEMINI_API_KEY"):
        st.warning("Please set your GEMINI_API_KEY in the .env file.")
        st.stop()
else:
    if not os.getenv("OPENROUTER_API_KEY"):
        st.warning("Please set your OPENROUTER_API_KEY in the .env file.")
        st.stop()

st.write(f"Using provider: **{config.provider}**")
if config.provider == "gemini":
    gemini_model = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
    st.write(f"Using model: **{gemini_model}**")
else:
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
        st.write(f"Provider: **{config.provider}**")
        if config.provider == "gemini":
            st.write(f"Model: **{os.getenv('GEMINI_MODEL', 'gemini-3.8-flash')}**")
        else:
            st.write(f"Model: **{config.model_name}**")
        st.caption(
            "Change AI_PROVIDER, OPENROUTER_MODEL, or GEMINI_MODEL in .env to switch"
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
        try:
            progress_bar = st.progress(0)
            status_text = st.empty()

            with temp_video_file(uploaded_file) as video_path:
                # Stage 1: preparing the video
                status_text.text("Preparing video for analysis...")
                progress_bar.progress(15)

                st.info("Analyzing video...")

                @with_retry(
                    config.max_api_retries, config.file_processing_poll_interval
                )
                def analyze_video():
                    if config.provider == "gemini":
                        return _analyze_with_gemini(
                            uploaded_file, custom_prompt, config
                        )
                    return _analyze_with_openrouter(
                        uploaded_file, custom_prompt, config
                    )

                # Stage 2: analysis in progress (single blocking API call)
                status_text.text("Sending video to AI provider...")
                progress_bar.progress(50)

                # Generate analysis
                analysis_result = analyze_video()

                # Stage 3: complete
                status_text.text("Analysis complete!")
                progress_bar.progress(100)

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
            progress_bar.empty()
            status_text.empty()
            pass
        except Exception as e:
            logger.error(f"Unexpected error during analysis: {str(e)}")
            st.error(f"An unexpected error occurred during analysis: {str(e)}")
            progress_bar.empty()
            status_text.empty()