# ============================================================
# 🎯 YouTube Transcript Proxy API (Flask)
# Fetches transcripts using youtube-transcript-api
# ============================================================

from flask import Flask, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # allow all origins (for Streamlit access)

@app.route('/<video_id>', methods=['GET'])
def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        text = " ".join([t["text"] for t in transcript])
        return jsonify({"status": "success", "transcript": text})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/')
def home():
    return jsonify({"message": "YouTube Transcript Proxy is running!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
