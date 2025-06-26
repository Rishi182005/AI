import tkinter as tk

class LiquidButton(tk.Button):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.primary_color = "#000"
        self.secondary_color = "#fff"
        self.transition_time = 600  # in milliseconds
        self.aspect_ratio = 2 / 1
        self.width = 10  # in em
        self.height = self.width * self.aspect_ratio
        self.border_radius = 20
        self.box_shadow = (0, 0, 0, 1)
        self.transform_x = 0.5
        self.filter_blur = 0.66
        self.filter_contrast = 20
        self.mix_blend_mode = "darken"
        self.overflow = "hidden"

        self.before_element = tk.Canvas(self, width=self.width*2, height=self.height)
        self.before_element.pack(side=tk.BOTTOM)

        self.radial_gradients = []
        for i in range(2):
            gradient = self.before_element.create_oval(
                12.5 + i*75, 50, 87.5 + i*75, 50,
                fill=self.secondary_color,
                outline=self.secondary_color
            )
            self.radial_gradients.append(gradient)

        self.config(
            relief=tk.FLAT,
            cursor="hand2",
            width=int(self.width),  # Convert width to integer
            height=int(self.height),  # Convert height to integer
            bg=self.primary_color,
            fg=self.secondary_color,
            activebackground=self.primary_color,
            activeforeground=self.secondary_color,
            highlightthickness=0,
            borderwidth=0
        )

        self.bind("<Configure>", self.on_configure)

    def on_configure(self, event):
        self.before_element.place(
            relx=0.5, rely=0.5,
            anchor=tk.CENTER
        )

    def animate(self):
        self.after(self.transition_time, self.toggle_transform)

    def toggle_transform(self):
        if self.transform_x == 0.5:
            self.transform_x = -0.5
        else:
            self.transform_x = 0.5
        self.before_element.place(
            relx=0.5 + self.transform_x, rely=0.5,
            anchor=tk.CENTER
        )
        self.place(
            relx=0.5 + self.transform_x, rely=0.5,
            anchor=tk.CENTER
        )
root = tk.Tk()
button = LiquidButton(root, text="Click me!")
button.pack(pady=10, padx= 1500)
button.animate()
root.mainloop()
