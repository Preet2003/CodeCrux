import tkinter as tk
from PIL import Image, ImageTk


class CardComponentHP(tk.Frame):
    def __init__(self, parent, button_text, image_path, prev_page=None):
        super().__init__(parent, bg="#2e2e2e", width=300, height=150, padx=10, pady=10)

        self.prev_page = prev_page  # Store the previous page

        # Add image (logo or any image for now)
        self.card_image = Image.open(image_path)
        self.card_image = self.card_image.resize((50, 50), Image.Resampling.LANCZOS)
        self.photo_image = ImageTk.PhotoImage(self.card_image)

        image_label = tk.Label(self, image=self.photo_image, bg="#2e2e2e")
        image_label.image = self.photo_image
        image_label.pack(pady=(5, 10))

        # Button (now acts as the title and action element)
        button = tk.Button(
            self,
            text=button_text,
            font=("Helvetica", 12, "bold"),
            bg="#ff5733",  # Distinct color for the button
            fg="#ffffff",
            cursor="hand2",  # Change cursor to hand
            activebackground="#ff5733",
            activeforeground="#ffffff",
            command=lambda: self.on_button_click(button_text),
        )
        button.pack(pady=(5, 10))

        self.pack_propagate(False)  # Prevent the frame from shrinking

    def on_button_click(self, button_text):
        # print(f"{button_text} clicked")  # Print button click message

        # Navigate to the algorithmPage for the selected button
        from algorithmPage import AlgorithmPage

        root = self.master  # Get the root window (Tk)
        while not isinstance(root, tk.Tk):
            root = root.master  # Keep traversing up until we find the Tk root window

        for widget in root.winfo_children():
            widget.destroy()  # Clear the current widgets from the window

        AlgorithmPage(
            root, button_text, prev_page=self.prev_page
        )  # Load the AlgorithmPage class with the clicked button text


if __name__ == "__main__":
    root = tk.Tk()

    # Example card usage
    card = CardComponentHP(root, button_text="Bubble Sort", image_path="path_to_image", prev_page="Sorting Algorithms")
    card.pack()

    root.mainloop()
