import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


class CardComponent(tk.Frame):  # Inherit from tk.Frame
    def __init__(self, parent, title, description, image_path):
        super().__init__(parent, bg="#2e2e2e", width=300, height=200, padx=10, pady=10)

        # Add image (logo), dynamically based on image_path
        self.logo_image = Image.open(image_path)
        self.logo_image = self.logo_image.resize((50, 50), Image.Resampling.LANCZOS)
        self.logo_photo = ImageTk.PhotoImage(self.logo_image)

        logo_label = tk.Label(self, image=self.logo_photo, bg="#2e2e2e")
        logo_label.image = self.logo_photo
        logo_label.pack(side=tk.TOP, pady=(5, 10))

        # Title
        title_label = tk.Label(
            self, text=title, font=("Helvetica", 15, "bold"), fg="#ffffff", bg="#2e2e2e"
        )
        title_label.pack(pady=(0, 5))

        # Description
        description_label = tk.Label(
            self,
            text=description,
            font=("Helvetica", 12),
            fg="#ffffff",
            bg="#2e2e2e",
            wraplength=200,
        )
        description_label.pack(pady=(0, 5))

        self.pack_propagate(False)  # Prevent the frame from shrinking
