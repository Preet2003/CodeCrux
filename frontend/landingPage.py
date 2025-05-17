import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from components.cardComponentLP import CardComponent  # Import the card component


class LandingPage:
    def __init__(self, root):
        self.root = root
        self.root.title("CodeCrux")
        self.root.geometry("1000x700")
        self.root.configure(bg="#1e1e1e")  # Set background color

        # Step 1: Set Favicon (Window Icon)
        self.set_icon()

        # Step 2: Add Exit Button (Top-Right)
        self.create_exit_button()

        # Step 3: Add Logo, Title, and Tagline
        self.create_logo()
        self.create_title()
        self.create_tagline()

        # Step 4: Add "What we do" section (with cards)
        self.create_what_we_do_section()

        # Step 5: Add "Let's visualize" and "Contact Us" buttons
        self.create_buttons()

    def set_icon(self):
        """Sets the window favicon/icon."""
        icon_image = tk.PhotoImage(file="./images/landingPage/favicon.png")
        self.root.iconphoto(False, icon_image)

    from PIL import Image, ImageTk  # Make sure to import these for handling images


    def create_exit_button(self):
        """Creates an exit button with an image at the top-right corner of the window."""
        # Load the image
        exit_image = Image.open("./images/landingPage/exit.png")  # Ensure the image path is correct
        exit_image = exit_image.resize(
            (30, 30), Image.Resampling.LANCZOS
        )  # Resize image as necessary
        exit_photo = ImageTk.PhotoImage(exit_image)

        # Create the button with the image instead of text
        exit_button = tk.Button(
            self.root,
            image=exit_photo,
            bg="#ff3333",  # Red background
            cursor="hand2",  # Change cursor to hand
            command=self.on_exit_button_click,
            activebackground="#ff3333",
            relief=tk.FLAT,  # No border
        )
        exit_button.image = exit_photo  # Keep a reference to avoid garbage collection

        # Place the button at the top-right corner
        exit_button.place(relx=0.98, rely=0.03, anchor=tk.CENTER)

    def on_exit_button_click(self):
        """Handles the exit button click and shows a confirmation dialog."""
        response = messagebox.askquestion(
            "Exit", "Are you sure you want to exit?", icon="warning"
        )
        if response == "yes":
            self.root.quit()  # Close the application
        # 'No' option is automatically handled, so it closes the dialog if selected.

    def create_logo(self):
        """Creates and places the application logo."""
        logo_image = Image.open("./images/landingPage/logo.png")
        logo_image = logo_image.resize((100, 100), Image.Resampling.LANCZOS)
        logo_photo = ImageTk.PhotoImage(logo_image)
        logo_label = tk.Label(self.root, image=logo_photo, bg="#1e1e1e")
        logo_label.image = logo_photo
        logo_label.pack(pady=(30, 10))

    def create_title(self):
        """Creates the main application title."""
        title_label = tk.Label(
            self.root,
            text="CodeCrux",
            font=("Helvetica", 36, "bold"),
            fg="#ffcc00",
            bg="#1e1e1e",
        )
        title_label.pack(pady=(10, 10))

    def create_tagline(self):
        """Creates the application tagline."""
        tagline_label = tk.Label(
            self.root,
            text="Visualize. Learn. Master.",
            font=("Helvetica", 15, "italic"),
            fg="#ffffff",
            bg="#1e1e1e",
        )
        tagline_label.pack(pady=(0, 10))

    def create_what_we_do_section(self):
        """Creates the 'What we do' section with a border and cards."""
        # Frame with border for the "What We Do" section
        what_we_do_frame = tk.Frame(
            self.root, bg="#1e1e1e", bd=2, relief=tk.SOLID
        )  # Border added
        what_we_do_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

        # What We Do heading inside the border frame
        what_we_do_label = tk.Label(
            what_we_do_frame,
            text="What We Do :",
            font=("Helvetica", 20, "bold"),
            fg="#ffffff",
            bg="#1e1e1e",
        )
        what_we_do_label.pack(pady=(10, 10))

        # Frame to hold cards inside the border frame
        cards_frame = tk.Frame(what_we_do_frame, bg="#1e1e1e")
        cards_frame.pack(pady=(0, 10))

        # Card 1: Visualization of algorithms
        card1 = CardComponent(
            cards_frame,
            title="Algorithm Visualization",
            description="Visualize algorithms including sorting, searching, and more.",
            image_path="./images/landingPage/eye.png",  # Different image for this card
        )
        card1.pack(side=tk.LEFT, padx=10)

        # Card 2: Chatbot functionality
        card2 = CardComponent(
            cards_frame,
            title="Documentation and FAQs", 
            description="Get answers to common questions and access documentation.",
            image_path="./images/landingPage/bot.png",  # Different image for this card
        )
        card2.pack(side=tk.LEFT, padx=10)

        # Card 3: Additional feature
        card3 = CardComponent(
            cards_frame,
            title="More Features Coming",
            description="Stay tuned for more exciting features. (Trees, Graphs, Other Advanced Algorithms)",
            image_path="./images/landingPage/feature.png",  # Different image for this card
        )
        card3.pack(side=tk.LEFT, padx=10)

    def create_buttons(self):
        """Creates the 'Let's visualize' and 'Contact Us' buttons."""
        button_frame = tk.Frame(self.root, bg="#1e1e1e")
        button_frame.pack(pady=10)

        # "Let's Visualize" button
        visualize_button = tk.Button(
            button_frame,
            text="Let's Visualize",
            font=("Helvetica", 16),
            bg="#ffcc00",
            fg="#1e1e1e",
            cursor="hand2",
            activebackground="#ffcc00",
            activeforeground="#1e1e1e",
            command=self.go_to_home_page,
        )
        visualize_button.pack(side=tk.LEFT, padx=10)

        # "Contact Us" button
        contact_button = tk.Button(
            button_frame,
            text="Contact Us",
            font=("Helvetica", 16),
            bg="#ffcc00",
            fg="#1e1e1e",
            cursor="hand2",
            activebackground="#ffcc00",
            activeforeground="#1e1e1e",
            command=self.go_to_contact_us_page,
        )
        contact_button.pack(side=tk.LEFT, padx=10)

    def go_to_home_page(self):
        """Switches to the home page."""
        from homePage import HomePage  # Local import to avoid circular imports

        for widget in self.root.winfo_children():
            widget.destroy()  # Clear the current widgets from the window
        HomePage(self.root)  # Load the HomePage class

    def go_to_contact_us_page(self):
        """Switches to the contact us page."""
        from contactUs import ContactUs  # Local import to avoid circular imports

        for widget in self.root.winfo_children():
            widget.destroy()  # Clear the current widgets from the window
        ContactUs(self.root)  # Load the ContactUs class


def run_app():
    root = tk.Tk()
    app = LandingPage(root)
    root.mainloop()


if __name__ == "__main__":
    run_app()
