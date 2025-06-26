############################################################################################################################################

 #     -------   |            |         /\       --------       ----------           ----------      -------------
 #     |            |           |        /  \           |            |           |           |            |              |
 #     |            |--------|       / -- \          |            |-----------        |            |              |
 #     |            |           |      /      \         |            |              |        |            |              |
 #     -------   |            |    /        \         |            ------------        ----------              |                                 
 #                                                                                                                                  ~ ~ ~ ~ ~ ~   Your personal AI  

#######################################################################################################################################  Header files
import datetime
import itertools
import customtkinter as ctk
import tkinter as tk
from tkinter import scrolledtext
import pygame
import uuid
import speech_recognition as sr
import pyttsx3
import os
import aiml
import nltk
import pyjokes
from nltk.corpus import wordnet
from PIL import Image, ImageSequence
from googletrans import Translator
import threading
from gtts import gTTS
import cv2
import atexit
from nltk.sentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
import re
from collections import Counter
import random
import time
import warnings
import webbrowser
from googleapiclient.discovery import build
from CTkMessagebox import CTkMessagebox
import subprocess

# Ignore all warnings
warnings.filterwarnings("ignore")

nltk.download('vader_lexicon', quiet=True)

################################################################################ Constants

LIGHT_BG, LIGHT_TEXT = 'white', 'black'
DARK_BG, DARK_TEXT = 'black', 'white'
AUDIO_DIR = "C:/Users/rishi/OneDrive/Desktop/college/fall_sem_24-25/ai/j_comp/audio_files"
NLTK_DATA_PATH = os.path.join(os.path.expanduser("~"), "nltk_data")

############################################################################### Global variables
current_mode = 'dark'
is_video_playing = False
listen_running = False
listen_tamil_running = False
is_on = True
mood=1
############################################################################### Setup
os.environ['NLTK_DATA'] = NLTK_DATA_PATH
nltk.download('wordnet', download_dir=NLTK_DATA_PATH, quiet=True)

k = aiml.Kernel()
for aiml_file in [
    "C:/Users/rishi/OneDrive/Desktop/college/fall_sem_24-25/ai/j_comp/hi.aiml",
    "C:/Users/rishi/OneDrive/Desktop/college/fall_sem_24-25/ai/j_comp/hi_tamil.aiml"
]:
    k.learn(aiml_file)

translator = Translator()
cap = cv2.VideoCapture("C:/Users/rishi/OneDrive/Desktop/college/fall_sem_24-25/ai/j_comp/2-vmake.mp4")
video_path = r"C:\Users\rishi\OneDrive\Desktop\college\fall_sem_24-25\ai\j_comp\A (1).mp4"
logo_audio_path = r"C:\Users\rishi\OneDrive\Desktop\college\fall_sem_24-25\ai\j_comp\A (1).mp3"


#############################################################################################################################          Audio file creation and deletion

def create_audio_dir():
    if not os.path.exists(AUDIO_DIR):
        os.makedirs(AUDIO_DIR)

def delete_audio_files():
    for filename in os.listdir(AUDIO_DIR):
        try:
            os.remove(os.path.join(AUDIO_DIR, filename))
        except Exception as e:
            print(f"Error deleting file {filename}: {e}")

############################################################################################################################   Emotional analysis for english language

def emotional_analysis(input_file):
    

    emotional_lexicon = {
        # Joy/Happiness
        "happy": "joy", "joyful": "joy", "elated": "joy", "glad": "joy", "delighted": "joy",
        "cheerful": "joy", "ecstatic": "joy", "pleased": "joy", "content": "joy", "blissful": "joy",
        "good": "joy", "fine": "joy",
        
        # Sadness
        "sad": "sadness", "unhappy": "sadness", "depressed": "sadness", "gloomy": "sadness",
        "melancholy": "sadness", "heartbroken": "sadness", "downcast": "sadness",
        "sorrowful": "sadness", "miserable": "sadness", "grief": "sadness",
        
        # Anger
        "angry": "anger", "furious": "anger", "enraged": "anger", "irate": "anger",
        "outraged": "anger", "irritated": "anger", "annoyed": "anger", "frustrated": "anger",
        "exasperated": "anger", "hostile": "anger",
        
        # Fear
        "afraid": "fear", "scared": "fear", "frightened": "fear", "terrified": "fear",
        "anxious": "fear", "panicked": "fear", "nervous": "fear", "apprehensive": "fear",
        "worried": "fear", "dreadful": "fear",
        
        # Surprise
        "surprised": "surprise", "amazed": "surprise", "astonished": "surprise", "shocked": "surprise",
        "startled": "surprise", "stunned": "surprise", "bewildered": "surprise",
        "awestruck": "surprise", "dumbfounded": "surprise", "flabbergasted": "surprise",
        
        # Disgust
        "disgusted": "disgust", "repulsed": "disgust", "revolted": "disgust", "nauseated": "disgust",
        "appalled": "disgust", "sickened": "disgust", "grossed": "disgust", "repelled": "disgust",
        "loathing": "disgust", "aversion": "disgust",
        
        # Love
        "love": "love", "adore": "love", "cherish": "love", "affectionate": "love",
        "passionate": "love", "fond": "love", "devoted": "love", "enamored": "love",
        "smitten": "love", "infatuated": "love",
        
        # Excitement
        "excited": "excitement", "thrilled": "excitement", "enthusiastic": "excitement",
        "eager": "excitement", "animated": "excitement", "exhilarated": "excitement",
        "energetic": "excitement", "lively": "excitement", "zestful": "excitement",
        "pumped": "excitement",
        
        # Calmness
        "calm": "calmness", "peaceful": "calmness", "serene": "calmness", "tranquil": "calmness",
        "relaxed": "calmness", "composed": "calmness", "placid": "calmness", "at_ease": "calmness",
        "mellow": "calmness", "zen": "calmness",
        
        # Confusion
        "confused": "confusion", "perplexed": "confusion", "puzzled": "confusion",
        "baffled": "confusion", "mystified": "confusion", "disoriented": "confusion",
        "befuddled": "confusion", "muddled": "confusion", "uncertain": "confusion",
        "ambivalent": "confusion"
    }

    def vader_analysis(text):
        sid = SentimentIntensityAnalyzer()
        return sid.polarity_scores(text)

    def textblob_analysis(text):
        blob = TextBlob(text)
        return blob.sentiment

    def analyze_emotions(text):
        words = text.lower().split()
        emotions = [emotional_lexicon.get(word, "neutral") for word in words if word in emotional_lexicon]
        
        if not emotions:
               return "சந்தோஷமாக" if is_on else "neutral", {}
            
        emotion_counts = {}
        for emotion in emotions:
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        dominant_emotion = max(emotion_counts, key=emotion_counts.get)
        
        return dominant_emotion, emotion_counts

    def analyze_text(text):
        print(f"Analyzing text: '{text.strip()}'\n")
        
        vader_scores = vader_analysis(text)
        print("VADER Sentiment:", vader_scores)
        
        textblob_sentiment = textblob_analysis(text)
        print("TextBlob Sentiment:", textblob_sentiment)
        
        dominant_emotion, emotion_counts = analyze_emotions(text)
        print(f"Dominant emotion: {dominant_emotion}")
        print("Emotion breakdown:", emotion_counts)

    with open(input_file, "r", errors='ignore') as sample_texts:
        lines = sample_texts.readlines()
        last_three_lines = lines[-3:]  # Get the last 3 lines
        for text in last_three_lines:
            analyze_text(text)
            print("\n" + "="*50 + "\n")

            
##############################################################################################################################  Emotional analysis for tamil language

def emotional_analysis_tamil(input_file):
    tamil_emotional_lexicon = {
        
        "மகிழ்ச்சி": "சந்தோஷம்",
        "சந்தோஷம்": "சந்தோஷம்",
        "சந்தோஷமாக": "சந்தோஷம்",
        "நல்ல": "சந்தோஷம்",# conjugated verb: very happy
        "துக்கம்": "சோகமாக",
        "சோகம்": "சோகமாக",
        "துக்கமாக": "சோகமாக",  # conjugated verb: very sad
        "கோபம்": "கோபமாக",
        "சினம்": "கோபமாக",
        "கோபமாக": "கோபமாக",  # conjugated verb: very angry
        "பயம்": "பயம்",
        "அச்சம்": "பயம்",
        "பயமாக": "பயம்",  # conjugated verb: very afraid# conjugated verb: very surprised
        "அருவருப்பு": "சலிப்பு",
        "வெறுப்பு": "சலிப்பு",
        "அருவருப்புமாக": "சலிப்பு"  # conjugated verb: very loving
    }

    def analyze_emotions_tamil(text):
        words = re.findall(r'\S+', text)
        emotions = [tamil_emotional_lexicon.get(word, "neutral") for word in words if word in tamil_emotional_lexicon]
        
        if not emotions:
            return "சந்தோஷமாக" if is_on else "neutral", {}
        
        emotion_counts = Counter(emotions)
        dominant_emotion = emotion_counts.most_common(1)[0][0]
        
        return dominant_emotion, dict(emotion_counts)

    def analyze_text_tamil(text):
        print(f"Analyzing text: '{text.strip()}'\n")
        
        dominant_emotion, emotion_counts = analyze_emotions_tamil(text)
        print(f"Dominant emotion: {dominant_emotion}")
        print("Emotion breakdown:", emotion_counts)

    with open(input_file, "r", encoding="utf-8", errors='ignore') as sample_texts:
        lines = sample_texts.readlines()
        last_three_lines = lines[-3:]  # Get the last 3 lines
        for text in last_three_lines:
            analyze_text_tamil(text)
            print("\n" + "="*50 + "\n")

######################################################################################################################### appending user input to the text file

def append_input_to_file(text, lang):
    file_name = f"user_{lang}_input.txt"
    with open(file_name, "a", encoding="utf-8") as file:
        file.write(text + "\n")
    print(f"Input appended to file: {file_name}")
    
    # Analyze the entire file and write to d_{lang}.txt
    dominant_emotion, emotion_counts = analyze_entire_file(file_name, lang)
    
    # Print the dominant emotion
    print(f"Dominant emotion in d_{lang}.txt: {dominant_emotion}")
    
    if lang == "tamil":
        emotional_analysis_tamil(file_name)
    else:
        emotional_analysis(file_name)

########################################################################################################################  Chat bot respond with audio (speak function)

def speak(text, lang='en'):
    def run_tts():
        start_video()
        
        if lang == 'ta':
            audio_file = os.path.join(AUDIO_DIR, f"response_{uuid.uuid4()}.mp3")
            tts = gTTS(text=text, lang='ta', tld='com.au')
            tts.save(audio_file)
            pygame.mixer.init()
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
        else:
            engine = pyttsx3.init()
            engine.setProperty('rate', 150)
            engine.setProperty('volume', 1)
            voices = engine.getProperty('voices')
            for voice in voices:
                if 'male' in voice.name.lower():
                    engine.setProperty('voice', voice.id)
                    break
            engine.say(text)
            engine.runAndWait()

        stop_video()

    threading.Thread(target=run_tts).start()


##########################################################################################################################    GIF player

def analyze_entire_file(input_file, lang):
    emotional_lexicon = {
        # Joy/Happiness
        "happy": "joy", "joyful": "joy", "elated": "joy", "glad": "joy", "delighted": "joy",
        "cheerful": "joy", "ecstatic": "joy", "pleased": "joy", "content": "joy", "blissful": "joy",
        "good": "joy", "fine": "joy",
        
        # Sadness
        "sad": "sadness", "unhappy": "sadness", "depressed": "sadness", "gloomy": "sadness",
        "melancholy": "sadness", "heartbroken": "sadness", "downcast": "sadness",
        "sorrowful": "sadness", "miserable": "sadness", "grief": "sadness",
        
        # Anger
        "angry": "anger", "furious": "anger", "enraged": "anger", "irate": "anger",
        "outraged": "anger", "irritated": "anger", "annoyed": "anger", "frustrated": "anger",
        "exasperated": "anger", "hostile": "anger",
        
        # Fear
        "afraid": "fear", "scared": "fear", "frightened": "fear", "terrified": "fear",
        "anxious": "fear", "panicked": "fear", "nervous": "fear", "apprehensive": "fear",
        "worried": "fear", "dreadful": "fear",
        
        # Surprise
        "surprised": "surprise", "amazed": "surprise", "astonished": "surprise", "shocked": "surprise",
        "startled": "surprise", "stunned": "surprise", "bewildered": "surprise",
        "awestruck": "surprise", "dumbfounded": "surprise", "flabbergasted": "surprise",
        
        # Disgust
        "disgusted": "disgust", "repulsed": "disgust", "revolted": "disgust", "nauseated": "disgust",
        "appalled": "disgust", "sickened": "disgust", "grossed": "disgust", "repelled": "disgust",
        "loathing": "disgust", "aversion": "disgust",
        
        # Love
        "love": "love", "adore": "love", "cherish": "love", "affectionate": "love",
        "passionate": "love", "fond": "love", "devoted": "love", "enamored": "love",
        "smitten": "love", "infatuated": "love",
        
        # Excitement
        "excited": "excitement", "thrilled": "excitement", "enthusiastic": "excitement",
        "eager": "excitement", "animated": "excitement", "exhilarated": "excitement",
        "energetic": "excitement", "lively": "excitement", "zestful": "excitement",
        "pumped": "excitement",
        
        # Calmness
        "calm": "calmness", "peaceful": "calmness", "serene": "calmness", "tranquil": "calmness",
        "relaxed": "calmness", "composed": "calmness", "placid": "calmness", "at_ease": "calmness",
        "mellow": "calmness", "zen": "calmness",
        
        # Confusion
        "confused": "confusion", "perplexed": "confusion", "puzzled": "confusion",
        "baffled": "confusion", "mystified": "confusion", "disoriented": "confusion",
        "befuddled": "confusion", "muddled": "confusion", "uncertain": "confusion",
        "ambivalent": "confusion",

        
        "மகிழ்ச்சி": "சந்தோஷம்",
        "சந்தோஷம்": "சந்தோஷம்",
        "சந்தோஷமாக": "சந்தோஷம்",
        "நல்ல": "சந்தோஷம்",# conjugated verb: very happy
        "துக்கம்": "சோகமாக",
        "சோகம்": "சோகமாக",
        "துக்கமாக": "சோகமாக",  # conjugated verb: very sad
        "கோபம்": "கோபமாக",
        "சினம்": "கோபமாக",
        "கோபமாக": "கோபமாக",  # conjugated verb: very angry
        "பயம்": "பயம்",
        "அச்சம்": "பயம்",
        "பயமாக": "பயம்",  # conjugated verb: very afraid# conjugated verb: very surprised
        "அருவருப்பு": "சலிப்பு",
        "வெறுப்பு": "சலிப்பு",
        "அருவருப்புமாக": "சலிப்பு",  # conjugated verb: very loving
    }

    def analyze_emotions(text):
        words = text.lower().split()
        emotions = [emotional_lexicon.get(word, "neutral") for word in words if word in emotional_lexicon]
        
        if not emotions:
            return "சந்தோஷமாக" if is_on else "neutral", {}
        
        emotion_counts = Counter(emotions)
        dominant_emotion = emotion_counts.most_common(1)[0][0]
        
        return dominant_emotion, dict(emotion_counts)

    # Read the entire file and analyze emotions
    with open(input_file, 'r', encoding='utf-8', errors='ignore') as sample_texts:
        text = sample_texts.read()
        dominant_emotion, emotion_counts = analyze_emotions(text)
        
        # Append the result to the new file
        output_file = f"d_{lang}.txt"
        with open(output_file, "a", encoding="utf-8") as file:
            file.write(f"{dominant_emotion}\n")
        
        return dominant_emotion, emotion_counts

##########################################################################################################################    Chatbot listens to user query (input voice)        
def listen(lang='en'):
    global gif_label, listen_running, listen_tamil_running
    gif_label.place(x=100, y=100)  # show the label
    animate_gif(0)
    listen_running = lang == 'en'
    listen_tamil_running = lang == 'ta'

    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        if lang == 'en':
            text = recognizer.recognize_google(audio, language='en-US')
        else:
            text = recognizer.recognize_google(audio, language='ta-IN')
        return text
    except sr.UnknownValueError:
        return "None"
    except sr.RequestError as e:
        return f"Could not request results from Google Speech Recognition service; {e}"
    finally:
        listen_running = False
        listen_tamil_running = False
 

#######################################################################################################################    translation of english to tamil and vice-versa

def translate(text, src, dest):
    try:
        translation = translator.translate(text, src=src, dest=dest)
        return translation.text
    except Exception as e:
        print(f"An error occurred during translation: {e}")
        return "Translation error occurred."

#################################################################################################################################   get word from word net

def get_word_meaning(word):
    synsets = wordnet.synsets(word)
    return synsets[0].definition() if synsets else "Sorry, I couldn't find the meaning of that word."

#################################################################################################################################   get bot response from aiml file
def quit1():
        with open('user_tamil_input.txt', 'w') as file:
            pass
        with open('user_english_input.txt', 'w') as file:
            pass
        with open('d_english.txt', 'w') as file:
            pass
        with open('d_tamil.txt', 'w') as file:
            pass
        window.destroy()

##############################################################################################################################################
root = None
youtube = None
playlist_id = None
songs = []
current_song = None
search_entry = None
song_listbox = None

def create_ui():
    global root, search_entry, song_listbox
    
    # Main frame
    main_frame = ctk.CTkFrame(root)
    main_frame.pack(padx=20, pady=20, fill="both", expand=True)
    
    # Search Section
    search_frame = ctk.CTkFrame(main_frame)
    search_frame.pack(pady=10, padx=10, fill="x")
    
    search_entry = ctk.CTkEntry(
        search_frame, 
        placeholder_text="Search songs...", 
        width=500
    )
    search_entry.pack(side="left", padx=(0, 10), expand=True, fill="x")
    
    search_btn = ctk.CTkButton(
        search_frame, 
        text="Search", 
        command=search_songs
    )
    search_btn.pack(side="right")
    
    # Playlist Listbox
    song_listbox = ctk.CTkScrollableFrame(main_frame)
    song_listbox.pack(pady=10, padx=10, fill="both", expand=True)
    
    # Control Buttons Frame
    btn_frame = ctk.CTkFrame(main_frame)
    btn_frame.pack(pady=10, padx=10, fill="x")
    
    # Play Button
    play_btn = ctk.CTkButton(
        btn_frame, 
        text="Play", 
        command=play_song,
        fg_color="green",
        hover_color="dark green"
    )
    play_btn.pack(side="left", padx=5, expand=True, fill="x")
    
    # Stop Button
    stop_btn = ctk.CTkButton(
        btn_frame, 
        text="Stop", 
        command=stop_song,
        fg_color="red",
        hover_color="dark red"
    )
    stop_btn.pack(side="left", padx=5, expand=True, fill="x")
    
    # YouTube Button
    youtube_btn = ctk.CTkButton(
        btn_frame, 
        text="Open in YouTube", 
        command=open_in_youtube,
        fg_color="red",
        text_color="white"
    )
    youtube_btn.pack(side="left", padx=5, expand=True, fill="x")
    
    # Quit Button
    quit_btn = ctk.CTkButton(
        btn_frame, 
        text="Quit", 
        command=quit_app,
        fg_color="gray",
        hover_color="dark gray"
    )
    quit_btn.pack(side="left", padx=5, expand=True, fill="x")

def fetch_playlist(playlist_id):
    global songs
    try:
        request = youtube.playlistItems().list(
            part="snippet",
            playlistId=playlist_id,
            maxResults=50
        )
        response = request.execute()
        
        songs = []
        for item in response['items']:
            song = {
                'title': item['snippet']['title'],
                'video_id': item['snippet']['resourceId']['videoId']
            }
            songs.append(song)
        
        populate_songs(songs)
    except Exception as e:
        show_error(f"Error fetching playlist: {str(e)}")

def populate_songs(songs_list):
    # Clear existing songs
    for widget in song_listbox.winfo_children():
        widget.destroy()
    
    # Create song buttons
    for song in songs_list:
        song_btn = ctk.CTkButton(
            song_listbox, 
            text=song['title'], 
            anchor="w",
            command=lambda s=song: select_song(s)
        )
        song_btn.pack(pady=5, padx=5, fill="x")

def select_song(song):
    global current_song
    current_song = song

def play_song():
    if current_song:
        video_url = f"https://www.youtube.com/watch?v={current_song['video_id']}"
        webbrowser.open(video_url)
        show_notification(f"Playing: {current_song['title']}")
    else:
        show_error("Please select a song first")

def stop_song():
    global current_song
    # Close YouTube tabs
    if os.name == 'nt':  # Windows
        os.system('taskkill /F /IM chrome.exe')
    elif os.name == 'posix':  # macOS and Linux
        os.system('pkill -f "chrome"')
    
    current_song = None
    show_notification("Playback stopped")

def open_in_youtube():
    if current_song:
        video_url = f"https://www.youtube.com/watch?v={current_song['video_id']}"
        webbrowser.open(video_url)
    else:
        show_error("Please select a song first")

def search_songs():
    query = search_entry.get().lower()
    if not query:
        populate_songs(songs)
        return
    matching_songs = [song for song in songs if query in song['title'].lower()]
    populate_songs(matching_songs if matching_songs else [])
    show_notification("No matching songs found" if not matching_songs else "")


def show_notification(message):
    notification = ctk.CTkToplevel(root)
    notification.title("Notification")
    notification.geometry("300x100")
    
    label = ctk.CTkLabel(
        notification, 
        text=message, 
        wraplength=250
    )
    label.pack(expand=True, fill="both", padx=20, pady=20)
    
    # Auto-close after 3 seconds
    notification.after(3000, notification.destroy)

def show_error(message):
    error = ctk.CTkToplevel(root)
    error.title("Error")
    error.geometry("300x100")
    
    label = ctk.CTkLabel(
        error, 
        text=message, 
        text_color="red",
        wraplength=250
    )
    label.pack(expand=True, fill="both", padx=20, pady=20)
    
    # Close button
    close_btn = ctk.CTkButton(
        error, 
        text="Close", 
        command=error.destroy
    )
    close_btn.pack(pady=(0, 20))

def quit_app():
    dialog = CTkMessagebox(
        title="Quit", 
        message="Do you want to exit the application?", 
        icon="question", 
        option_1="Yes", 
        option_2="No"
    )
    
    if dialog.get() == "Yes":
        root.destroy()
        

def initialize_app(mood):
    global root, youtube, playlist_id
    
    # Set up main window
    root = ctk.CTk()
    root.title("Advanced Playlist Player")
    root.geometry("800x600")
    
    # Set appearance mode and color theme
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    # YouTube API Setup
    api_key = "AIzaSyBrD1r60gWFnp44upxTlop4pBHis0s0jwY"
    youtube = build("youtube", "v3", developerKey=api_key)
    
    # Set playlist ID
    
    mood_playlists = {
        1: "RDCLAK5uy_mfdqvCAl8wodlx2P2_Ai2gNkiRDAufkkI",  # Joy- English playlist
        2: "RDCLAK5uy_lp8LtelM9GiSwRFGGQjctKaGoHcrgQVEU", # Sad- English
        3: "RDCLAK5uy_nIDyjgkxsuKb6uQlT3q9eR5tNsW_mKqA8", # Angry/ calm
        4: "RDCLAK5uy_nTbyVypdXPQd00z15bTWjZr7pG-26yyQ4", # Happy- tamil
        5: "RDCLAK5uy_nm-giFQKA4i6JfvowrhofkVXuK7S2dgtA"  # Sad- Tamil
    }
    playlist_id = mood_playlists.get(mood, None)
    if playlist_id:
        fetch_playlist(playlist_id)
    else:
        fetch_playlist("RDCLAK5uy_mfdqvCAl8wodlx2P2_Ai2gNkiRDAufkkI")
        # Create UI
    create_ui()
    
    # Fetch playlist
    fetch_playlist(playlist_id)
    
    # Start the application
    root.mainloop()


#########################################################################################################################################  mood analyzer
# Initialize global variables
def get_most_common_word(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8' if is_on else 'utf-8') as file:
            text = file.read().lower()
            tokens = re.findall(r'\w+', text)
            word_counts = Counter(tokens)
            mood, _ = word_counts.most_common(1)[0]
            return mood
    except Exception as e:
        return "Error reading file: " + str(e)

def analyze_dominant_emotion():
    file_path = r'C:\Users\rishi\OneDrive\Desktop\college\fall_sem_24-25\ai\j_comp\d_tamil.txt' if is_on else r'C:\Users\rishi\OneDrive\Desktop\college\fall_sem_24-25\ai\j_comp\d_english.txt'
    return get_most_common_word(file_path)

def get_bot_response(user_input):
    global current_mode, mood
    lower_input = user_input.lower()
    
    if user_input == "None":
        return "நீ பேசுவதை என்னால் கேட்க முடிய வில்லை. கொஞ்சம் சத்தமாக பேச முடியுமா?" if is_on else "I can't hear you. Can you speak a little louder?"
    
    if "change to dark mode" in lower_input:
        current_mode = 'dark'
        apply_theme(current_mode)
        return "Switching to Dark Mode..."
    
    elif "change to light mode" in lower_input:
        current_mode = 'light'
        apply_theme(current_mode)
        return "Switching to Light Mode..."
    
    elif lower_input.startswith(("meaning of", "what is the meaning of", "what is meaning of")):
        word = lower_input.split()[-1]
        return get_word_meaning(word)
    
    elif lower_input.endswith((" அர்த்தம் என்ன", " என்றால் என்ன")):
        word = lower_input.split()[1]
        english_word = translate(word, 'ta', 'en')
        meaning = get_word_meaning(english_word)
        return translate(meaning, 'en', 'ta')
    
    elif lower_input == "exit":
        quit1()

    elif "open" in lower_input or "திற" in lower_input:  # English and Tamil "open" keywords
        if "app" in lower_input or "ஆப்" in lower_input:  # English and Tamil "app" keywords
            # Extract the application name (using different split methods for English and Tamil)
            app_name = lower_input.split("app")[-1].strip() if "app" in lower_input else lower_input.split("ஆப்")[-1].strip()
            
            # Mapping app names to their paths (including both English and Tamil names)
            app_paths = {
                # English names
                "notepad": "notepad.exe",
                "chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
                "clock": "ms-clock:",
                "calculator": "C:\\Windows\\WinSxS\\wow64_microsoft-windows-calc_31bf3856ad364e35_10.0.26100.1_none_b10653edb7a9547d\\calc.exe",
                
                # Tamil names
                "நோட்": "notepad.exe",
                "குரோம்": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
                "கடிகாரம்": "ms-clock:",
                "கணக்குப்பெறி": "C:\\Windows\\WinSxS\\wow64_microsoft-windows-calc_31bf3856ad364e35_10.0.26100.1_none_b10653edb7a9547d\\calc.exe"
            }
            
            # Check if the app is in the dictionary
            if app_name in app_paths:
                app_path = app_paths[app_name]
                if app_name in ["clock", "கடிகாரம்"]:
                    # Special handling for Windows Clock app
                    subprocess.Popen(["start", app_path], shell=True)
                else:
                    subprocess.Popen([app_path])
                
                # Multilingual response
                return f"Opening {app_name}..." if "app" in lower_input else f"{app_name} திறக்கப்படுகிறது..."
            else:
                # Multilingual error message
                return f"App '{app_name}' not found in the predefined list." if "app" in lower_input else f"ஆப் '{app_name}' பட்டியலில் இல்லை."
        
        elif "website" in lower_input or "வலைத்தளம்" in lower_input:
            # Extract the website name
            website_name = lower_input.split("website")[-1].strip() if "website" in lower_input else lower_input.split("வலைத்தளம்")[-1].strip()
            
            # Mapping website names to URLs (including both English and Tamil names)
            websites = {
                # English names
                "gmail": "https://mail.google.com",
                "youtube": "https://www.youtube.com",
                "news": "https://www.timesnownews.com",
                
                # Tamil names
                "ஜிமெயில்": "https://mail.google.com",
                "யூடியூப்": "https://www.youtube.com",
                "செய்திகள்": "https://www.timesnownews.com"
            }
            
            if website_name in websites:
                webbrowser.open(websites[website_name])
                # Multilingual response
                return f"Opening {website_name}..." if "website" in lower_input else f"{website_name} திறக்கப்படுகிறது..."
            else:
            # Multilingual help message
                return "Please specify the app or website to open. Example: 'open app notepad' or 'open website youtube'" if "open" in lower_input else "தயவுசெய்து திறக்க வேண்டிய ஆப்பை அல்லது வலைத்தளத்தை குறிப்பிடவும்."
        
    elif "news" in lower_input or "செய்தி" in lower_input:
        website_name = "செய்தி" if is_on else "news"
        # Mapping website names to URLs
        websites = {
            "news": "https://www.timesnownews.com",
            "செய்தி": "https://www.timesnownews.com"
        }
        
        # Check if any news-related keyword is in the input
        news_source = next((key for key in websites.keys() if key in lower_input), None)
        
        if news_source:
            webbrowser.open(websites[news_source])
            # Multilingual response
            return f"Opening {news_source}..." if "news" in lower_input else f"{news_source} திறக்கப்படுகிறது..."
        
        else:
            # Multilingual error message
            return "News source not found." if "news" in lower_input else "செய்தி தளம் கிடைக்கவில்லை."        
            
    
    elif "mood" in lower_input or "மனநிலை" in lower_input or "மனநிலைக்கு" in lower_input or "மனநிம்மதி" in lower_input:
        if "song" in lower_input or "பாட்டு" in lower_input or "playlist" in lower_input or "பிளேலிஸ்ட்" in lower_input:
            mood1 = analyze_dominant_emotion()
            print(mood1)
            if is_on:  # English mode
                mood_em = {
                    "neutral":4,
                    "angry": 3,  # Angry/ calm
                    "joy": 4,    # Happy- Tamil
                    "sad": 5  # Angry/ calm
                }
            else:  # Tamil mode
                mood_em = {
                    "neutral":1,
                    "joy": 1,    # Joy- English playlist
                    "sad": 2,    # Sad- English
                    "angry": 3   # Angry/ calm# Sad- Tamil
                }
            mood = mood_em.get(mood1)
            if mood is not None:
                initialize_app(mood)
                if initialize_app(mood):
                    return "உங்களுக்கு பாடல் பிடிக்கும் என்று நம்புகிறேன் ☺" if is_on else "Hope you like the song ☺"
            else:
                return "Could not find a playlist for the current mood."
        else:
            mood = analyze_dominant_emotion()
            if is_on:
                return f"நான் சேகரித்தவற்றிலிருந்து, நீங்கள் {mood} உணர்கிறீர்கள் போல் தெரிகிறது. உங்கள் மனதில் இருப்பதைப் பற்றி மேலும் பகிர்ந்து கொள்ள விரும்பினால் நான் இங்கே இருக்கிறேன்!"
            else:
                return f"From what I’ve gathered, it seems like you might be feeling {mood}. Does that sound right? I'm here if you want to share more about what’s on your mind!"
    
    else:
        
        response = k.respond(user_input)
        if response:
            return response.encode('utf-8').decode('utf-8')
        else:
            if analyze_combinations(lower_input):
                return analyze_combinations(lower_input)
            else:
                if user_input != "None":
                    return "மன்னிக்கவும், என்னால் உன்னைப் புரிந்து கொள்ள முடியவில்லை!  மீண்டும் சொல்ல முடியுமா?" if is_on else "Pardon, I cant understand you! Can you repeat it?"

def analyze_combinations(sentence):
    emotion_map = {
        # Joy/Happiness
        "happy": "joy", "joyful": "joy", "elated": "joy", "glad": "joy", "delighted": "joy",
        "cheerful": "joy", "ecstatic": "joy", "pleased": "joy", "content": "joy", "blissful": "joy",
        "good": "joy", "fine": "joy",
        
        # Sadness
        "sad": "sadness", "unhappy": "sadness", "depressed": "sadness", "gloomy": "sadness",
        "melancholy": "sadness", "heartbroken": "sadness", "downcast": "sadness",
        "sorrowful": "sadness", "miserable": "sadness", "grief": "sadness",
        
        # Anger
        "angry": "anger", "furious": "anger", "enraged": "anger", "irate": "anger",
        "outraged": "anger", "irritated": "anger", "annoyed": "anger", "frustrated": "anger",
        "exasperated": "anger", "hostile": "anger",
        
        # Fear
        "afraid": "fear", "scared": "fear", "frightened": "fear", "terrified": "fear",
        "anxious": "fear", "panicked": "fear", "nervous": "fear", "apprehensive": "fear",
        "worried": "fear", "dreadful": "fear",
        
        # Surprise
        "surprised": "surprise", "amazed": "surprise", "astonished": "surprise", "shocked": "surprise",
        "startled": "surprise", "stunned": "surprise", "bewildered": "surprise",
        "awestruck": "surprise", "dumbfounded": "surprise", "flabbergasted": "surprise",
        
        # Disgust
        "disgusted": "disgust", "repulsed": "disgust", "revolted": "disgust", "nauseated": "disgust",
        "appalled": "disgust", "sickened": "disgust", "grossed": "disgust", "repelled": "disgust",
        "loathing": "disgust", "aversion": "disgust",
        
        # Love
        "love": "love", "adore": "love", "cherish": "love", "affectionate": "love",
        "passionate": "love", "fond": "love", "devoted": "love", "enamored": "love",
        "smitten": "love", "infatuated": "love",
        
        # Excitement
        "excited": "excitement", "thrilled": "excitement", "enthusiastic": "excitement",
        "eager": "excitement", "animated": "excitement", "exhilarated": "excitement",
        "energetic": "excitement", "lively": "excitement", "zestful": "excitement",
        "pumped": "excitement",
        
        # Calmness
        "calm": "calmness", "peaceful": "calmness", "serene": "calmness", "tranquil": "calmness",
        "relaxed": "calmness", "composed": "calmness", "placid": "calmness", "at_ease": "calmness",
        "mellow": "calmness", "zen": "calmness",
        
        # Confusion
        "confused": "confusion", "perplexed": "confusion", "puzzled": "confusion",
        "baffled": "confusion", "mystified": "confusion", "disoriented": "confusion",
        "befuddled": "confusion", "muddled": "confusion", "uncertain": "confusion",
        "ambivalent": "confusion",

        
        "மகிழ்ச்சி": "சந்தோஷம்",
        "சந்தோஷம்": "சந்தோஷம்",
        "சந்தோஷமாக": "சந்தோஷம்",
        "நல்ல": "சந்தோஷம்",# conjugated verb: very happy
        "துக்கம்": "சோகமாக",
        "சோகம்": "சோகமாக",
        "துக்கமாக": "சோகமாக",  # conjugated verb: very sad
        "கோபம்": "கோபமாக",
        "சினம்": "கோபமாக",
        "கோபமாக": "கோபமாக",  # conjugated verb: very angry
        "பயம்": "பயம்",
        "அச்சம்": "பயம்",
        "பயமாக": "பயம்",  # conjugated verb: very afraid# conjugated verb: very surprised
        "அருவருப்பு": "சலிப்பு",
        "வெறுப்பு": "சலிப்பு",
        "அருவருப்புமாக": "சலிப்பு" # conjugated verb: very disgusted# conjugated verb: very loving
    }
    if sentence != "None" and sentence != None:
        words = sentence.split()
        combinations = []
        response=""
        generated_responses = set()
        for r in range(1, len(words) + 1):
            combinations.extend(itertools.combinations(words, r))
        
        for combination in combinations:
            combination_str = ' '.join(combination)
            for key, value in emotion_map.items():
                if key in combination_str:
                    combination_str = value
                    break
            res = k.respond(combination_str)
            if res and res not in generated_responses:
                generated_responses.add(res)
                response += f"{res}"
                if combination != combinations[-1] and res.strip()[-1] not in ('.', '?'):
                    response = response.rstrip() + "! "
        return response.strip()
        
#############################################################################################################################   Chatbot video interactions (mp4 usage)
def play_video():
    global cap, is_video_playing
    if is_video_playing:
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = cap.read()

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        img = img.resize((window.winfo_width(), window.winfo_height()))
        img_tk = ctk.CTkImage(light_image=img, dark_image=img, size=(1514,828))

        background_label.configure(image=img_tk)
        background_label.image = img_tk

    window.after(12, play_video)


def start_video():
    global is_video_playing
    is_video_playing = True

def stop_video():
    global is_video_playing
    is_video_playing = False

######################################################################################################################   Display the messages of both bot and user in UI

def display_message(message, sender, lang="en"):
    try: 
        chat_history = tamil_chat_history if lang == "ta" else english_chat_history
        if message != "None":
            chat_history.insert(tk.END, f"{sender}: ")
            for char in message:
                chat_history.insert(tk.END, char)
                chat_history.see(tk.END)
                window.update()
                window.after(1)  # adjust the delay as needed
            chat_history.insert(tk.END, "\n\n")
        else:
            chat_history.insert(tk.END, f"{sender}: \n\n")

        chat_history.see(tk.END)
    except Exception as e:
        print(f"Error in display_message: {e}")

################################################################################################################################  Theme for text box  (dialog box)

def apply_theme(theme_mode):
    ctk.set_appearance_mode(theme_mode)

###############################################################################################################################   UI widgets (buttons, switch)
    

def switch():
    global is_on
    is_on = not is_on
    t_btn.configure(image=on if is_on else off)
    tvoice_button.place(x=1095, y=710) if is_on else tvoice_button.place_forget()
    evoice_button.place_forget() if is_on else evoice_button.place(x=1095, y=710)
    tamil_chat_history.place(x=1392, y=55) if is_on else tamil_chat_history.place_forget()
    english_chat_history.place_forget() if is_on else english_chat_history.place(x=1392, y=55)
    tlabel.place(x=10, y=10) if is_on else tlabel.place_forget()
    elabel.place_forget() if is_on else elabel.place(x=10, y=10)


  # adjust the delay as needed
        
############################################################################################################################################# Main UI setup

def setup_ui():
    global window, background_label, english_chat_history, tamil_chat_history, input_entry, t_btn, evoice_button, tvoice_button, tlabel, elabel, gif_frames, gif_frames1, on, off, search_entry, gif_label, gif_frames_list

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    window = ctk.CTk()
    window.title("Chatbot")
    window.attributes('-fullscreen')  # Start in windowed mode
    window.geometry('1920x1080')  # Set the desired resolution

    # Function to toggle fullscreen
    def toggle_fullscreen():
        current_state = window.attributes('-fullscreen')
        window.attributes('-fullscreen', not current_state)



    # Bind the F11 key to toggle fullscreen
    window.bind("<F11>", lambda event: toggle_fullscreen())
    overlay = ctk.CTkLabel(window, text="", fg_color="black")
    overlay.place(x=0, y=0, relwidth=1, relheight=1)

    gif_image = Image.open("C:/Users/rishi/OneDrive/Desktop/college/fall_sem_24-25/ai/j_comp/loading1.gif")
    gif_frames_list = []
    for frame in ImageSequence.Iterator(gif_image):
        frame = frame.resize((50, 50))  # adjust the size as needed
        gif_frames_list.append(ctk.CTkImage(light_image=frame, dark_image=frame, size=(50, 50)))
    gif_label = ctk.CTkLabel(window, image=gif_frames_list[0])
    gif_label.place(x=100, y=100)  # adjust the position as needed
    gif_label.place_forget()
    
    bg_image = Image.open("C:/Users/rishi/OneDrive/Desktop/college/fall_sem_24-25/ai/j_comp/2_photo1.png")
    bg_photo = ctk.CTkImage(light_image=bg_image, dark_image=bg_image, size=(1514,828))

    background_label = ctk.CTkLabel(window, image=bg_photo, text="")
    background_label.pack(fill="both", expand=False)

    tlabel = ctk.CTkLabel(window, text="Tamil ChatBot™  ☻", font=("Ravie", 25))
    tlabel.place(x=10, y=10)

    elabel = ctk.CTkLabel(window, text="English ChatBot™  ☻", font=("Ravie", 25))
    elabel.place(x=10, y=10)
    elabel.place_forget()

    frame_width = 500  # Width of the frame when fully visible
    partially_visible_x = 1900  # Position for partial visibility (only scrollbar visible)
    fully_visible_x = 1392  # Target position when fully slid in
    animation_speed = 15  # Pixels per movement step
    delay = 5  # Delay in milliseconds between each step

    # Create frames for English and Tamil chat histories
    chat_frame_english = tk.Frame(window, width=frame_width, height=500, bg="black")
    chat_frame_english.place(x=partially_visible_x, y=55)

    chat_frame_tamil = tk.Frame(window, width=frame_width, height=500, bg="black")
    chat_frame_tamil.place(x=partially_visible_x, y=55)

    # Slide-in function for English chat
    def slide_in_chat_english():
        current_x = chat_frame_english.winfo_x()
        if current_x > fully_visible_x:
            chat_frame_english.place(x=current_x - animation_speed, y=55)
            window.after(delay, slide_in_chat_english)
        else:
            chat_frame_english.place(x=fully_visible_x, y=55)

    # Slide-out function for English chat
    def slide_out_chat_english():
        current_x = chat_frame_english.winfo_x()
        if current_x < partially_visible_x:
            chat_frame_english.place(x=current_x + animation_speed, y=55)
            window.after(delay, slide_out_chat_english)
        else:
            chat_frame_english.place(x=partially_visible_x, y=55)

    # Slide-in function for Tamil chat
    def slide_in_chat_tamil():
        current_x = chat_frame_tamil.winfo_x()
        if current_x > fully_visible_x:
            chat_frame_tamil.place(x=current_x - animation_speed, y=55)
            window.after(delay, slide_in_chat_tamil)
        else:
            chat_frame_tamil.place(x=fully_visible_x, y=55)

    # Slide-out function for Tamil chat
    def slide_out_chat_tamil():
        current_x = chat_frame_tamil.winfo_x()
        if current_x < partially_visible_x:
            chat_frame_tamil.place(x=current_x + animation_speed, y=55)
            window.after(delay, slide_out_chat_tamil)
        else:
            chat_frame_tamil.place(x=partially_visible_x, y=55)

    # English Chat History
    english_chat_history = scrolledtext.ScrolledText(
        chat_frame_english, wrap=tk.WORD, width=50, height=15, 
        font=("Segoe UI", 14), bg="#2b2b2b", fg="#ffffff"
    )
    english_chat_history.pack(fill="both", expand=True)

    # Tamil Chat History
    tamil_chat_history = scrolledtext.ScrolledText(
        chat_frame_tamil, wrap=tk.WORD, width=50, height=15, 
        font=("Segoe UI", 14), bg="#2b2b2b", fg="#ffffff"
    )
    tamil_chat_history.pack(fill="both", expand=True)

    # Bind hover events for sliding in/out
    chat_frame_english.bind("<Enter>", lambda e: slide_in_chat_english())
    chat_frame_english.bind("<Leave>", lambda e: slide_out_chat_english())
    chat_frame_tamil.bind("<Enter>", lambda e: slide_in_chat_tamil())
    chat_frame_tamil.bind("<Leave>", lambda e: slide_out_chat_tamil())

    '''class NeonBorder1:
        def __init__(self, text_area):
            self.text_area = text_area
            self.colors = ["#ff0000", "#ff7f00", "#ffff00", "#00ff00", "#0000ff", "#ff00ff", "#00ffff"]
            self.current_color_index = 0
            self.current_color = self.colors[self.current_color_index]
            self.target_color_index = (self.current_color_index + 1) % len(self.colors)
            self.target_color = self.colors[self.target_color_index]
            self.color_diff = [int(self.target_color[i:i+2], 16) - int(self.current_color[i:i+2], 16) for i in (1, 3, 5)]
            self.step = 0
            self.steps = 100
            self.animate()

        def animate(self):
            r = int(self.current_color[1:3], 16) + self.color_diff[0] * self.step // self.steps
            g = int(self.current_color[3:5], 16) + self.color_diff[1] * self.step // self.steps
            b = int(self.current_color[5:7], 16) + self.color_diff[2] * self.step // self.steps
            self.text_area.config(highlightbackground=f"#{r:02x}{g:02x}{b:02x}", highlightthickness=3)
            self.step += 1
            if self.step >= self.steps:
                self.current_color_index = self.target_color_index
                self.current_color = self.target_color
                self.target_color_index = (self.current_color_index + 1) % len(self.colors)
                self.target_color = self.colors[self.target_color_index]
                self.color_diff = [int(self.target_color[i:i+2], 16) - int(self.current_color[i:i+2], 16) for i in (1, 3, 5)]
                self.step = 0
            window.after(5, self.animate)

    # Call the function to start the animation
    neon_border = NeonBorder1(english_chat_history)
    neon_border_tamil = NeonBorder1(tamil_chat_history)'''

    # Modify the display_message function to use the new frames
    def display_message(message, sender, lang="en"):
        chat_history = tamil_chat_history if lang == "ta" else english_chat_history
        if message != "None":
            chat_history.insert(tk.END, f"{sender}: ")
            for char in message:
                chat_history.insert(tk.END, char)
                chat_history.see(tk.END)
                window.update()
                window.after(1)  # adjust the delay as needed
            chat_history.insert(tk.END, "\n\n")
        else:
            chat_history.insert(tk.END, f"{sender}: \n\n")

        chat_history.see(tk.END)

    # Modify the switch function to handle the new frames
    def switch():
        global is_on
        is_on = not is_on
        t_btn.configure(image=on if is_on else off)
        
        # Toggle voice buttons
        tvoice_button.place(x=1095, y=710) if is_on else tvoice_button.place_forget()
        evoice_button.place_forget() if is_on else evoice_button.place(x=1095, y=710)
        
        # Toggle chat histories
        if is_on:
            # Tamil mode
            chat_frame_tamil.place(x=1900, y=55)
            chat_frame_english.place_forget()
            tlabel.place(x=10, y=10)
            elabel.place_forget()
        else:
            # English mode
            chat_frame_english.place(x=1900, y=55)
            chat_frame_tamil.place_forget()
            elabel.place(x=10, y=10)
            tlabel.place_forget()
            
    '''class NeonBorder1:
        def __init__(self, text_area):
            self.text_area = text_area
            self.colors = ["#ff0000", "#ff7f00", "#ffff00", "#00ff00", "#0000ff", "#ff00ff", "#00ffff"]
            self.current_color_index = 0
            self.current_color = self.colors[self.current_color_index]
            self.target_color_index = (self.current_color_index + 1) % len(self.colors)
            self.target_color = self.colors[self.target_color_index]
            self.color_diff = [int(self.target_color[i:i+2], 16) - int(self.current_color[i:i+2], 16) for i in (1, 3, 5)]
            self.step = 0
            self.steps = 100
            self.animate()

        def animate(self):
            r = int(self.current_color[1:3], 16) + self.color_diff[0] * self.step // self.steps
            g = int(self.current_color[3:5], 16) + self.color_diff[1] * self.step // self.steps
            b = int(self.current_color[5:7], 16) + self.color_diff[2] * self.step // self.steps
            self.text_area.config(highlightbackground=f"#{r:02x}{g:02x}{b:02x}", highlightthickness=3)
            self.step += 1
            if self.step >= self.steps:
                self.current_color_index = self.target_color_index
                self.current_color = self.target_color
                self.target_color_index = (self.current_color_index + 1) % len(self.colors)
                self.target_color = self.colors[self.target_color_index]
                self.color_diff = [int(self.target_color[i:i+2], 16) - int(self.current_color[i:i+2], 16) for i in (1, 3, 5)]
                self.step = 0
            window.after(5, self.animate)

    # Call the function to start the animation
    neon_border = NeonBorder1(english_chat_history)
    neon_border_tamil = NeonBorder1(tamil_chat_history)'''
    
    
    input_entry = ctk.CTkEntry(window, font=("Arial", 12))
    input_entry.bind("<Return>", lambda event: send_message("l1"))

    switch_on = Image.open("C:/Users/rishi/OneDrive/Desktop/college/fall_sem_24-25/ai/j_comp/switch_on1.png")
    on = ctk.CTkImage(light_image=switch_on, dark_image=switch_on, size=(50, 24))

    switch_off = Image.open("C:/Users/rishi/OneDrive/Desktop/college/fall_sem_24-25/ai/j_comp/switch_off1.png")
    off = ctk.CTkImage(light_image=switch_off, dark_image=switch_off, size=(50, 24))

    t_btn = ctk.CTkButton(master=window, image=on, text="", compound="top", width=60, height=40, corner_radius=20, fg_color="#7E72B4", bg_color= "#7575a9", command=switch)
    t_btn.place(x=1425.5, y=0)


    def on_focus_in(event):
        placeholder_label.place_forget()

    def on_focus_out(event):
        if search_entry.get() == "":
            placeholder_label.place(x=160, y=715)
    
    search_entry = ctk.CTkEntry(window, font=("Arial", 12), width=1220, height =80, fg_color="#000000", bg_color="#b0b1c7",corner_radius=40)
    search_entry.place(x=150, y=700)
    search_entry.bind("<FocusIn>", on_focus_in)
    search_entry.bind("<FocusOut>", on_focus_out)

    placeholder_label = ctk.CTkLabel(window, text="Type your message...", font=("Arial", 21), text_color="#808080", bg_color="#000000")
    placeholder_label.place(x=160, y=720)

    # Add a send button next to the search box
    send_button = ctk.CTkButton(window, text="Send", width=140, height=60, bg_color="#000000", corner_radius=30,command=lambda: send_message_from_entry())
    send_button.place(x=1210, y=710)
    
    tvoice_image = ctk.CTkImage(light_image=Image.open("C:/Users/rishi/OneDrive/Desktop/college/fall_sem_24-25/ai/j_comp/tvoice.png"), dark_image=Image.open("C:/Users/rishi/OneDrive/Desktop/college/fall_sem_24-25/ai/j_comp/tvoice.png"), size=(40, 50))
    evoice_image = ctk.CTkImage(light_image=Image.open("C:/Users/rishi/OneDrive/Desktop/college/fall_sem_24-25/ai/j_comp/evoice.png"), dark_image=Image.open("C:/Users/rishi/OneDrive/Desktop/college/fall_sem_24-25/ai/j_comp/evoice.png"), size=(40, 50))

    tvoice_button = ctk.CTkButton(window, image=tvoice_image, command=lambda: send_message("l2"), text="", width=60, height=60, bg_color="#000000", corner_radius=30)
    evoice_button = ctk.CTkButton(window, image=evoice_image, command=lambda: send_message("l1"), text="", width=60, height=60, bg_color="#000000", corner_radius=30)    

    tvoice_button.place(x=1095, y=710)
    # Bind the Enter key to send the message
    search_entry.bind("<Return>", lambda event: send_message_from_entry())

    wishMe()
    
    def fade_in(alpha=0.5):
        if alpha > 0:
            overlay.configure(fg_color=(f"black", f"#{int(alpha*255):02x}{int(alpha*255):02x}{int(alpha*255):02x}"))
            window.after(200, fade_in, alpha - 0.01)
        else:
            overlay.destroy()

    class NeonBorder:
        def __init__(self, text_area):
            self.text_area = text_area
            self.colors = ["#ff0000", "#ff7f00", "#ffff00", "#00ff00", "#0000ff", "#ff00ff"]
            self.current_color_index = 0
            self.current_color = self.colors[self.current_color_index]
            self.target_color_index = (self.current_color_index + 1) % len(self.colors)
            self.target_color = self.colors[self.target_color_index]
            self.color_diff = [int(self.target_color[i:i+2], 16) - int(self.current_color[i:i+2], 16) for i in (1, 3, 5)]
            self.step = 0
            self.steps = 100
            self.animate()

        def animate(self):
            r = int(self.current_color[1:3], 16) + self.color_diff[0] * self.step // self.steps
            g = int(self.current_color[3:5], 16) + self.color_diff[1] * self.step // self.steps
            b = int(self.current_color[5:7], 16) + self.color_diff[2] * self.step // self.steps
            self.text_area.configure(border_color=f"#{r:02x}{g:02x}{b:02x}")
            self.step += 1
            if self.step >= self.steps:
                self.current_color_index = self.target_color_index
                self.current_color = self.target_color
                self.target_color_index = (self.current_color_index + 1) % len(self.colors)
                self.target_color = self.colors[self.target_color_index]
                self.color_diff = [int(self.target_color[i:i+2], 16) - int(self.current_color[i:i+2], 16) for i in (1, 3, 5)]
                self.step = 0
            window.after(5, self.animate)

    # Call the function to start the animation
    neon_border = NeonBorder(search_entry)


    # Start the fade-in effect after a short delay
    window.after(2000, fade_in)


    window.after(100, play_video)


################################################################################################################################  send query box

def wishMe():
    hour=datetime.datetime.now().hour
    if hour>=0 and hour<12:
        welcome_msg="காலை வணக்கம்" if is_on else "Hello, Good Morning"
    elif hour>=12 and hour<18:
        welcome_msg= "மதிய வணக்கம்" if is_on else "Hello, Good Afternoon"
    else:
        welcome_msg="மாலை வணக்கம்" if is_on else "Hello, Good Evening"
    display_message(welcome_msg, "Chatbot ", lang="ta" if  is_on else "en")
    speak(welcome_msg, lang="ta" if is_on else "en")

def send_message_from_entry():
    user_input = search_entry.get()
    if user_input and user_input.strip() != "" :
        lang = "tamil" if is_on else "english"
        if user_input and user_input.strip() != "quit":
            display_message(user_input, "User  ", lang="ta" if is_on else "en")
            append_input_to_file(user_input, lang)
            bot_response = get_bot_response(user_input)
            speak(bot_response, lang="ta" if is_on else "en")
            display_message(bot_response, "Chatbot", lang="ta" if is_on else "en")
            search_entry.delete(0, tk.END)
        else:
            bot_response = get_bot_response(user_input)

def send_message(lang, input_type="voice"):
    if input_type == "voice":
        user_input = listen('ta' if lang == "l2" else 'en')
    else:
        user_input = search_entry.get()
        search_entry.delete(0, tk.END)  # Clear the search box after sending

    if user_input and user_input.strip() != "":
        display_message(user_input, "User ", lang="ta" if lang == "l2" else "en")
          # Add this line
        bot_response = get_bot_response(user_input)
        if bot_response !="None" and user_input !="None" :
            append_input_to_file(user_input, "tamil" if lang == "l2" else "english")
        speak(bot_response, lang='ta' if lang == "l2" else 'en')
        display_message(bot_response, "Chatbot", lang="ta" if lang == "l2" else "en")


################################################################################################################################  LOGO


def animate_gif(frame_index):
    global gif_label, gif_frames_list
    gif_label.configure(image=gif_frames_list[frame_index])
    frame_index += 1
    if frame_index >= len(gif_frames_list):
        frame_index = 0
    window.after(100, lambda: animate_gif(frame_index))


def logo(video_path, speed_factor=1.0):
    # Initialize Pygame
    pygame.init()

    # Open video capture & check if successful
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error opening video file")
        return

    # Set the window to fullscreen
    cv2.namedWindow("Video Player", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Video Player", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    # Get video properties for FPS calculation
    video_fps = cap.get(cv2.CAP_PROP_FPS)

    # Initialize audio
    pygame.mixer.init()
    pygame.mixer.music.load(logo_audio_path)

    # Start playing audio
    pygame.mixer.music.play()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Display video frame
        cv2.imshow('Video Player', frame)

        # Wait for a short period to maintain the frame rate, adjusted by speed factor
        wait_time = int(1000 / (video_fps * speed_factor))  # Adjust wait time based on speed factor
        if cv2.waitKey(wait_time) & 0xFF == ord('q'):
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()
    pygame.mixer.music.stop()
    pygame.quit()

# Main function
if __name__ == "__main__":
    speed_factor = 1.75  # Set speed factor (e.g., 2.0 for double speed)
    logo(video_path, speed_factor)  # Call the logo function to play the video
    create_audio_dir()
    atexit.register(delete_audio_files)
    setup_ui()
    window.mainloop()
