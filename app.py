import streamlit as st
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key = os.getenv('GOOGLE_API_KEY'))

prompt = """ You are a youtube video summarizer. You will be taking the transcript text asnd summarize the entire
video and providing the important summary in points withing 200-250 words.
Please procide the summary of the text given here:- """

## getting the transcript data from YT videos
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split('=')[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)

        transcript = ""
        for text in transcript_text:
            transcript += " " + text["text"] 

        return transcript

    except Exception as e:
        raise e
    

## getting the summary based on  prompt using Gemini Pro
def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt+transcript_text)
    return response.text

## Setting up the frontend using streamlit
st.title("YouTube Video Summarizer")
youtube_link = st.text_input("Enter your youyube link here:- ",)

if youtube_link:
    video_id = youtube_link.split("=")[1].split("&")[0]
    print("video_id:- ",video_id)
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Get Summary"):
    transcript_text = extract_transcript_details(youtube_link)

    if transcript_text:
        summary = generate_gemini_content(transcript_text,prompt)
        st.markdown("## Detailed Summary:")
        st.write(summary)