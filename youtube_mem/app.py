# ============================================================
# 🎓  YouTube Learning Assistant (MEM Style)
# Stable Final Version – works on Hugging Face Spaces
# ============================================================

import streamlit as st
import re
from transformers import pipeline
import requests

# --- Safe import of transcript library ---
try:
    from youtube_transcript_api import YouTubeTranscriptApi
except ImportError:
    st.error("youtube-transcript-api not found. Make sure it’s in requirements.txt")

# ============================================================
# 🧠 Helper Functions
# ============================================================

def extract_video_id(url: str):
    """Extract the 11-character YouTube video ID from any valid URL."""
    pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(pattern, url)
    return match.group(1) if match else None


def get_transcript(video_id):
    """Fetch transcript from the proxy API hosted on Render."""
    proxy_url = f"https://yt-transcript-proxy.onrender.com/{video_id}"
    response = requests.get(proxy_url)
    data = response.json()
    if data["status"] == "success":
        return data["transcript"]
    else:
        raise Exception(f"Proxy Error: {data['message']}")


def summarize_MEM_style(text: str) -> str:
    """Summarize transcript using MEM (Model Explanation Method)."""
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    max_chunk = 1000  # keep inside model token limit
    chunks = [text[i:i + max_chunk] for i in range(0, len(text), max_chunk)]
    summary = ""

    for chunk in chunks:
        prompt = f"""
        Summarize and explain this content using the MEM (Model Explanation Method):
        - Use simple, story-like language.
        - Explain step-by-step, as if teaching a beginner.
        - Focus on understanding, not technical detail.
        - Keep tone calm, structured, and easy to remember.

        Text:
        {chunk}
        """
        out = summarizer(prompt, max_length=200, min_length=80, do_sample=False)[0]['summary_text']
        summary += out + " "

    return summary.strip()

# ============================================================
# 🎨 Streamlit Interface
# ============================================================

st.set_page_config(page_title="🎥 YouTube Learning Assistant (MEM Style)", layout="centered")
st.title("🎓 YouTube Learning Assistant (MEM Style)")
st.markdown("Paste a **YouTube video link** below to generate its transcript and a MEM-style explanation.")

url = st.text_input("Enter YouTube URL:")

if st.button("Generate MEM Summary"):
    if not url:
        st.warning("Please paste a YouTube link first.")
    else:
        video_id = extract_video_id(url)
        if not video_id:
            st.error("Invalid YouTube URL. Please check and try again.")
        else:
            with st.spinner("Fetching transcript… please wait ⏳"):
                try:
                    text = get_transcript(video_id)
                    st.success("Transcript fetched successfully ✅")
                    st.subheader("📝 Transcript Preview")
                    st.write(text[:600] + "…")

                    with st.spinner("Creating your MEM-style summary… ⏳"):
                        summary = summarize_MEM_style(text)
                    st.subheader("📘 MEM-Style Explanation")
                    st.write(summary)

                except Exception as e:
                    st.error(f"Error: {str(e)}")
