import tkinter as tk
from components.cardComponentHP import CardComponentHP  # Import the card component
from PIL import Image, ImageTk


class HomePage:
    def __init__(self, root):
        self.root = root
        self.root.title("CodeCrux")
        self.root.geometry("1000x700")
        self.root.configure(bg="#1e1e1e")  # Set background color

        # Add "select an algorithm" section (with cards)
        self.create_select_an_algo_section()

        # Section for cards
        self.create_visualization_cards()

        # Add a button to go back to the previous page
        self.create_previous_button()

    def create_select_an_algo_section(self):
        """Creates the 'select an algo' section"""

        # Select an algo heading inside the border frame
        select_an_algo_label = tk.Label(
            text="Select an Algorithm",
            font=("Helvetica", 20, "bold"),
            fg="#ffffff",
            bg="#1e1e1e",
        )
        select_an_algo_label.pack(pady=(10, 3))

    def create_visualization_cards(self):
        """Creates the visualization cards."""
        frame = tk.Frame(self.root, bg="#1e1e1e")
        frame.pack(pady=(10, 10))

        # Create a frame for each row of cards
        for i in range(3):  # 3 rows
            row_frame = tk.Frame(frame, bg="#1e1e1e")
            row_frame.pack(pady=10)

            # Titles and button names for the cards
            cards_info = [
                "Sorting Algorithms",
                "Searching Algorithms",
                "Array Operations",
                "Linked List Operations",
                "Stack Operations",
                "Queue Operations",
            ]

            # Dynamically generate cards for each visualization type in the current row
            for j in range(3):  # 3 cards per row
                index = i * 3 + j
                if index < len(cards_info):
                    button_text = cards_info[index]
                    card = CardComponentHP(
                        row_frame,
                        button_text=button_text,
                        image_path = f"./images/homePage/img{index}.png",
                    )
                    card.pack(side=tk.LEFT, padx=10)

    def create_previous_button(self):
        """Creates the 'Go to Previous Page' button."""
        previous_button = tk.Button(
            self.root,
            text="Go to Previous Page",
            font=("Helvetica", 14),
            bg="#ffcc00",
            fg="#1e1e1e",
            cursor="hand2",
            activebackground="#ffcc00",  # Keep the same background color when pressed
            activeforeground="#1e1e1e",  # Keep the same text color when pressed
            command=self.go_back,
        )
        previous_button.pack(pady=20)

    def go_back(self):
        """Navigates back to the landing page."""
        from landingPage import LandingPage  # Local import to avoid circular imports

        for widget in self.root.winfo_children():
            widget.destroy()  # Clear the current widgets from the window
        LandingPage(self.root)  # Load the LandingPage class


def run_home_page():
    root = tk.Tk()
    app = HomePage(root)
    root.mainloop()


if __name__ == "__main__":
    run_home_page()