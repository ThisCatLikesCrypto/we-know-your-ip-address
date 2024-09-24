from pytube import YouTube
from main import producesyntaxed
import os

#Audio downloader (from youtube)
def download_audio(yt_link):
    producesyntaxed(f"Downloading new background song with link {yt_link}...")
    try:
        yt = YouTube(yt_link)
        audio_stream = yt.streams.filter(only_audio=True).first()
        audio_file = audio_stream.download(os.getcwd(), "song.mp4")
        producesyntaxed("Success")
        return audio_file
    except Exception as e:
        producesyntaxed("Error downloading audio:" + str(e))
        return None
    