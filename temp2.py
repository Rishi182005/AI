import customtkinter as ctk
import os
import webbrowser
from googleapiclient.discovery import build
from CTkMessagebox import CTkMessagebox

# Global variables
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

def fetch_playlist():
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
    
    # Filter songs
    matching_songs = [
        song for song in songs 
        if query in song['title'].lower()
    ]
    
    # Populate with matching songs
    if matching_songs:
        populate_songs(matching_songs)
    else:
        show_notification("No matching songs found")

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

def initialize_app(playlist_id_input):
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
    playlist_id = playlist_id_input
    
    # Create UI
    create_ui()
    
    # Fetch playlist
    fetch_playlist()
    
    # Start the application
    root.mainloop()

# Example usage
if __name__ == "__main__":
    # Replace with your YouTube playlist ID
    playlist_id = "RDCLAK5uy_mfdqvCAl8wodlx2P2_Ai2gNkiRDAufkkI"
    initialize_app(playlist_id)
