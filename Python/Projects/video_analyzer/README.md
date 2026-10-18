# Video Analyzer with Gemini

This is a Python application that uses [Streamlit](https://streamlit.io/) for the user interface and Google's [Gemini API](https://ai.google.dev/) to analyze video files.

## Features

-   **Upload Video**: Supports uploading video files (mp4, mov, avi, mkv).
-   **Video Playback**: Plays the uploaded video within the app.
-   **AI Analysis**: Uses the Gemini 2.0 Flash model to generate a detailed description of the video's content.

## Prerequisites

-   Python 3.8 or higher
-   A Google Cloud Project with the Gemini API enabled
-   A Google API Key

## Setup

1.  **Clone the repository** (if applicable) or navigate to the project directory.

2.  **Create a virtual environment** (recommended):
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables**:
    -   Create a `.env` file in the root directory.
    -   Add your Google API key:
        ```
        GOOGLE_API_KEY=your_api_key_here
        ```

## How to Run

Run the Streamlit application:

```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`.
