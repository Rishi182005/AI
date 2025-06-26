import customtkinter as ctk  # Import custom tkinter
import tkinter as tk
from PIL import Image, ImageSequence

# Initialize customtkinter with the appearance mode and color theme
ctk.set_appearance_mode("dark")  # or "light"
  # Optional theme

# Create the main window
root = ctk.CTk()  # Use CTk instead of Tk
root.title("Animated GIF Background with Fade Transitions")
root.geometry("1920x1080")

# Load the GIF image using Pillow (PIL)
gif_image = Image.open("C:/Users/rishi/OneDrive/Desktop/college/fall_sem_24-25/ai/j_comp/Purple-Modern-Vezzra-Entertain-unscreen.gif")

# Create a label to display the animated GIF with opacity
class AnimatedLabel(ctk.CTkLabel):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.alpha = 0.0
        self.delta = 0.01
        self.frames = [frame.copy() for frame in ImageSequence.Iterator(gif_image)]  # Work with Image objects
        self.current_frame = 0
        self.ctk_image = None  # Placeholder for CTkImage object
        self.play_gif()
        self.animate_fade_in()

    def animate_fade_in(self):
        """Fade in and cycle through frames of GIF"""
        self.alpha += self.delta
        self.update_alpha()
        if self.alpha < 1.0:
            root.after(4, self.animate_fade_in)
        else:
            root.after(2000, self.animate_fade_out)
             # Start playing GIF after fade-in is complete

    def animate_fade_out(self):
        """Fade out and stop the animation""" 
        self.alpha -= self.delta
        self.update_alpha()
        if self.alpha > 0.0:
            root.after(3, self.animate_fade_out)
        else:
            root.destroy()  # Close the window after fade-out

    def update_alpha(self):
        """Update image transparency (alpha)"""
        alpha = int(255 * self.alpha)
        frame = self.frames[self.current_frame].convert("RGBA")  # Convert current frame to RGBA
        frame.putalpha(alpha)  # Apply the alpha transparency
        self.ctk_image = ctk.CTkImage(light_image=frame, size=(360,360))  # Convert Image to CTkImage
        self.configure(image=self.ctk_image)  # Use CTkImage instead of PhotoImage

    def play_gif(self):
        """Play the GIF by cycling through frames"""
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        self.update_alpha()  # Update the frame with current alpha transparency
        root.after(30, self.play_gif)  # Adjust delay to control the speed of GIF

# Create and place the animated label
bg_label = AnimatedLabel(root, text = "")
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Add other widgets (optional)
label = ctk.CTkLabel(root, text="", font=("Helvetica", 24), fg_color="#000000")
label.pack(pady=20)

# Start the Tkinter main loop
root.mainloop()
