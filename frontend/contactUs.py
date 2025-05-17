import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk  # Import for handling images
import webbrowser


class ContactUs:
    def __init__(self, root):
        self.root = root
        self.root.title("CodeCrux")
        self.root.geometry("1000x700")
        self.root.configure(bg="#1e1e1e")  # Set background color

        # Load the icon image (replace all icons with logo.png)
        icon_image1 = Image.open("./images/contactUs/developer.png")
        icon_image1 = icon_image1.resize((30, 30), Image.Resampling.LANCZOS)
        icon_photo1 = ImageTk.PhotoImage(icon_image1)

        # Load the icon image (replace all icons with logo.png)
        icon_image2 = Image.open("./images/contactUs/gmail.png")
        icon_image2 = icon_image2.resize((30, 30), Image.Resampling.LANCZOS)
        icon_photo2 = ImageTk.PhotoImage(icon_image2)

        # Load the icon image (replace all icons with logo.png)
        icon_image3 = Image.open("./images/contactUs/github.png")
        icon_image3 = icon_image3.resize((30, 30), Image.Resampling.LANCZOS)
        icon_photo3 = ImageTk.PhotoImage(icon_image3)

        # Center all elements vertically and horizontally
        content_frame = tk.Frame(self.root, bg="#1e1e1e")
        content_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # Center align

        # Heading 1: Developer
        developer_label = tk.Label(
            content_frame,
            text="Developer",
            font=("Helvetica", 24, "bold"),
            fg="#ffcc00",
            bg="#1e1e1e",
        )
        developer_label.pack(pady=(30, 10))

        # Developer name and email
        developer_frame = tk.Frame(content_frame, bg="#1e1e1e")
        developer_frame.pack(pady=10)

        developer_icon = tk.Label(
            developer_frame,
            image=icon_photo1,  # Use image instead of text icon
            bg="#1e1e1e",
        )
        developer_icon.image = icon_photo1
        developer_icon.pack(side=tk.LEFT, padx=5)

        developer_name = tk.Label(
            developer_frame,
            text="Preet K Mistry",
            font=("Helvetica", 18),
            bg="#1e1e1e",
            fg="#ffffff",
        )
        developer_name.pack(side=tk.LEFT, padx=5)

        email_icon = tk.Label(
            developer_frame,
            image=icon_photo2,  # Use image instead of text icon
            bg="#1e1e1e",
        )
        email_icon.image = icon_photo2
        email_icon.pack(side=tk.LEFT, padx=5)

        email_link = tk.Label(
            developer_frame,
            text="33preetmistry@gmail.com",
            font=("Helvetica", 18),
            fg="#ffffff",
            bg="#1e1e1e",
        )
        email_link.pack(side=tk.LEFT, padx=5)

        # Heading 2: Reference
        reference_label = tk.Label(
            content_frame,
            text="Reference",
            font=("Helvetica", 24, "bold"),
            fg="#ffcc00",
            bg="#1e1e1e",
        )
        reference_label.pack(pady=(30, 10))

        # Reference (GitHub)
        reference_frame = tk.Frame(content_frame, bg="#1e1e1e")
        reference_frame.pack(pady=10)

        github_icon = tk.Label(
            reference_frame,
            image=icon_photo3,  # Use image instead of text icon
            bg="#1e1e1e",
        )
        github_icon.image = icon_photo3
        github_icon.pack(side=tk.LEFT, padx=5)

        github_link = tk.Label(
            reference_frame,
            text="GitHub Repository",
            font=("Helvetica", 18),
            fg="#ffffff",
            bg="#1e1e1e",
            cursor="hand2",
        )
        github_link.pack(side=tk.LEFT, padx=5)
        github_link.bind(
            "<Button-1>",
            lambda e: webbrowser.open("https://github.com/Preet2003"),
        )

        # Go back button
        go_back_button = tk.Button(
            content_frame,
            text="Go to Previous Page",
            font=("Helvetica", 14),
            bg="#ffcc00",
            fg="#1e1e1e",
            cursor="hand2",
            activebackground="#ffcc00",
            activeforeground="#1e1e1e",
            command=self.go_back,
        )
        go_back_button.pack(pady=20)

    def go_back(self):
        """Navigates back to the landing page."""
        from landingPage import LandingPage  # Local import to avoid circular imports

        for widget in self.root.winfo_children():
            widget.destroy()  # Clear the current widgets from the window
        LandingPage(self.root)  # Load the LandingPage class


def run_contact_us():
    root = tk.Tk()
    app = ContactUs(root)
    root.mainloop()


if __name__ == "__main__":
    run_contact_us()
