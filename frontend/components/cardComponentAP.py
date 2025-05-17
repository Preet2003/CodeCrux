import tkinter as tk
from PIL import Image, ImageTk
import importlib
import os


class CardComponentAP(tk.Frame):
    def __init__(self, parent, button_text, image_path, prev_page):
        super().__init__(parent, bg="#2e2e2e", width=300, height=150, padx=10, pady=10)
        self.prev_page = prev_page.replace(" ", "_").lower()  # Normalize folder name

        # Add image (logo or any image for now)
        self.card_image = Image.open(image_path).resize(
            (50, 50), Image.Resampling.LANCZOS
        )
        self.photo_image = ImageTk.PhotoImage(self.card_image)

        tk.Label(self, image=self.photo_image, bg="#2e2e2e").pack(pady=(5, 10))

        # Button (title + action element)
        button = tk.Button(
            self,
            text=button_text,
            font=("Helvetica", 12, "bold"),
            bg="#ff5733",
            fg="#ffffff",
            cursor="hand2",
            activebackground="#ff5733",
            activeforeground="#ffffff",
            command=lambda: self.on_button_click(button_text),
        )
        button.pack(pady=(5, 10))
        self.pack_propagate(False)

    def on_button_click(self, button_text):
        """Dynamically load the correct file based on the button text."""
        # Convert text to lowercase and replace spaces with underscores
        file_name = button_text.lower().replace(" ", "_")
        print(f"{file_name} clicked")
        module_path = f"screens.{self.prev_page}.{file_name}"
        print(module_path)

        try:
            # Dynamically import the selected algorithm/module
            algorithm_module = importlib.import_module(module_path)

            # Clear the current window and display the new algorithm page
            root = self.master
            while not isinstance(root, tk.Tk):
                root = root.master

            for widget in root.winfo_children():
                widget.destroy()

            # Call the algorithm page's initializer function
            algorithm_module.create_algorithm_page(root, self.prev_page)

        except ImportError as e:
            print(f"Error: {file_name}.py not found in {self.prev_page} ({e})")


if __name__ == "__main__":
    root = tk.Tk()
    card = CardComponentAP(
        root,
        button_text="Singly Linked List",
        image_path="path_to_image",
        prev_page="Linked List Operations",
    )
    card.pack()
    root.mainloop()
