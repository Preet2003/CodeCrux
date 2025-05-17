import tkinter as tk
from components.cardComponentAP import CardComponentAP  # Import the card component
from PIL import Image, ImageTk


class AlgorithmPage:
    def __init__(self, root, algo_type, prev_page=None):
        self.root = root
        self.root.title("CodeCrux")
        self.root.geometry("1000x700")
        self.root.configure(bg="#1e1e1e")  # Set background color

        self.algo_type = algo_type  # Algorithm type (e.g., Sorting, Searching)
        self.prev_page = prev_page  # Save previous page to navigate back properly
        self.algo_options = self.get_algo_options(
            algo_type
        )  # Retrieve specific algorithms

        # Add "select an algorithm" section (with cards)
        self.create_algo_section()

        # Section for algorithm cards
        self.create_algorithm_cards()

        # Add a button to go back to the home page or previous page
        self.create_previous_button()

    def get_algo_options(self, algo_type):
        """Returns the options available under each algorithm type."""
        options = {
            "Sorting Algorithms": [
                "Bubble Sort",
                "Selection Sort",
                "Insertion Sort",
                "Merge Sort",
                "Quick Sort",
                "Heap Sort",
                "Radix Sort",
                "Counting Sort",
                "Bucket Sort",
            ],
            "Searching Algorithms": [
                "Linear Search",
                "Binary Search",
            ],
            "Array Operations": [
                "Insertion at a specific position",
                "Deletion from a specific position",
                "Update element at a given index",
            ],
            "Linked List Operations": [
                "Singly Linked List",
                "Doubly Linked List",
            ],
            "Stack Operations": [
                "Push Pop Peek",
            ],
            "Queue Operations": [
                "Enqueue Dequeue Front and Rear",
            ],
        }
        return options.get(algo_type, [])

    def create_algo_section(self):
        """Creates the 'Select Algorithm' section."""
        algo_label = tk.Label(
            text=f"{self.algo_type}",
            font=("Helvetica", 20, "bold"),
            fg="#ffffff",
            bg="#1e1e1e",
        )
        algo_label.pack(pady=(10, 3))

    def create_algorithm_cards(self):
        """Creates cards for each specific algorithm."""
        frame = tk.Frame(self.root, bg="#1e1e1e")
        frame.pack(pady=(10, 10))

        # Map of main algorithms to folder numbers (0 to 8)
        algo_folder_map = {
            "Sorting Algorithms": 0,
            "Searching Algorithms": 1,
            "Array Operations": 2,
            "Linked List Operations": 3,
            "Stack Operations": 4,
            "Queue Operations": 5,
            "Tree Operations": 6,
            "Graph Algorithms": 7,
            "Other Advanced Algorithms": 8,
        }

        # Determine the folder number based on the main algorithm
        folder_number = algo_folder_map.get(self.algo_type, 0)

        # Determine the number of columns based on the algorithm type
        num_columns = 4 if self.algo_type == "Sorting Algorithms" else 3

        # Create a frame for each row of cards (3 or 4 cards per row)
        for i in range(0, len(self.algo_options), num_columns):
            row_frame = tk.Frame(frame, bg="#1e1e1e")
            row_frame.pack(pady=10)

            # Dynamically generate cards for each specific algorithm in the current row
            for j in range(num_columns):
                index = i + j
                if index < len(self.algo_options):
                    button_text = self.algo_options[index]

                    # Dynamically select the image path based on algorithm folder and sub-algorithm index
                    image_path = (
                        f"./images/algorithmPage/algo{folder_number}/img{index}.png"
                    )

                    card = CardComponentAP(
                        row_frame,
                        button_text=button_text,
                        image_path=image_path,  # Set the dynamically generated image path
                        prev_page=self.algo_type,  # Pass the current algorithm type to the card
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
            activebackground="#ffcc00",
            activeforeground="#1e1e1e",
            command=self.go_back,
        )
        previous_button.pack(pady=20)

    def go_back(self):
        """Navigates back to the previous page."""
        if self.prev_page:  # Check if there's a previous page to go back to
            from algorithmPage import AlgorithmPage

            for widget in self.root.winfo_children():
                widget.destroy()  # Clear the current widgets from the window
            AlgorithmPage(
                self.root, self.prev_page
            )  # Navigate back to the previous page
        else:
            from homePage import HomePage  # Local import to avoid circular imports

            for widget in self.root.winfo_children():
                widget.destroy()  # Clear the current widgets from the window
            HomePage(self.root)  # Load the HomePage class


def run_algorithm_page(algo_type):
    root = tk.Tk()
    app = AlgorithmPage(root, algo_type)
    root.mainloop()


if __name__ == "__main__":
    run_algorithm_page(
        "Sorting Algorithms"
    )  # Example to launch the Sorting Algorithms page