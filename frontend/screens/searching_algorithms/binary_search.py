import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import threading
import random


class BinarySearchVisualization:
    def __init__(self, root, prev_page):
        self.root = root
        self.prev_page = prev_page
        self.is_paused = False
        self.speed = 0.5
        self.search_thread = None
        self.step_mode = False
        self.step_event = threading.Event()
        self.create_algorithm_page()

    def create_algorithm_page(self):
        """Set up the Binary Search algorithm page."""
        # Clear current widgets in the root window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create a new frame for the algorithm page
        self.frame = tk.Frame(self.root, bg="#1e1e1e")
        self.frame.pack(expand=True, fill="both")

        # Heading (Algorithm Name)
        algo_label = tk.Label(
            self.frame,
            text="Binary Search Visualization",
            font=("Helvetica", 20, "bold"),
            fg="#ffffff",
            bg="#1e1e1e",
        )
        algo_label.pack(pady=(20, 10))

        # Fields frame
        field_frame = tk.Frame(self.frame, bg="#1e1e1e")
        field_frame.pack(fill="x", padx=20, pady=5)

        # Entry frame
        entry_frame = tk.Frame(self.frame, bg="#1e1e1e")
        entry_frame.pack(fill="x", padx=20, pady=5)

        # Input field for numbers
        input_label = tk.Label(
            field_frame,
            text="Enter sorted numbers (comma-separated):",
            fg="#ffffff",
            bg="#1e1e1e",
        )
        input_label.pack(side="left", expand=True, fill="x", padx=20, pady=(10, 5))
        self.input_entry = tk.Entry(entry_frame, width=40)
        self.input_entry.pack(side="left", expand=True, fill="x", padx=20)

        # Input field for target number
        target_label = tk.Label(
            field_frame, text="Enter target number:", fg="#ffffff", bg="#1e1e1e"
        )
        target_label.pack(side="left", expand=True, fill="x", padx=20,pady=(10, 5))
        self.target_entry = tk.Entry(entry_frame, width=10)
        self.target_entry.pack(side="left", expand=True, fill="x", padx=20)

        # Visualization frame
        self.viz_frame = tk.Frame(self.frame, bg="#1e1e1e")
        self.viz_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Buttons frame
        button_frame = tk.Frame(self.frame, bg="#1e1e1e")
        button_frame.pack(fill="x", padx=20, pady=5)

        # Speed control slider
        button_frame = tk.Frame(self.frame, bg="#1e1e1e")
        button_frame.pack(fill="x", padx=20, pady=10)
        speed_label = tk.Label(button_frame, text="Speed:", fg="#ffffff", bg="#1e1e1e")
        speed_label.pack(side="left")
        self.speed_slider = ttk.Scale(
            button_frame,
            from_=0.1,
            to=2.0,
            orient="horizontal",
            length=200,
            value=0.5,
            command=self.update_speed,
        )
        self.speed_slider.pack(side="left", padx=(10, 0))

        # Start button
        self.start_button = tk.Button(
            button_frame,
            text="Start Search",
            font=("Helvetica", 12),
            bg="#ffcc00",
            fg="#1e1e1e",
            activebackground="#ffcc00",
            activeforeground="#1e1e1e",
            cursor="hand2",
            command=self.start_search,
        )
        self.start_button.pack(side="left", expand=True, fill="x", padx=5)

        # Pause/Resume button
        self.pause_button = tk.Button(
            button_frame,
            text="Pause",
            font=("Helvetica", 12),
            bg="#ffcc00",
            fg="#1e1e1e",
            activebackground="#ffcc00",
            activeforeground="#1e1e1e",
            cursor="hand2",
            command=self.toggle_pause,
            state="disabled",
        )
        self.pause_button.pack(side="left", expand=True, fill="x", padx=5)

        # Documentation button
        doc_button = tk.Button(
            button_frame,
            text="Documentation",
            font=("Helvetica", 12),
            bg="#ffcc00",
            fg="#1e1e1e",
            activebackground="#ffcc00",
            activeforeground="#1e1e1e",
            cursor="hand2",
            command=self.show_documentation,
        )
        doc_button.pack(side="left", expand=True, fill="x", padx=5)

        # Ask AI button
        ai_button = tk.Button(
            button_frame,
            text="Q & A",
            font=("Helvetica", 12),
            bg="#ffcc00",
            fg="#1e1e1e",
            activebackground="#ffcc00",
            activeforeground="#1e1e1e",
            cursor="hand2",
            command=self.ask_ai,
        )
        ai_button.pack(side="left", expand=True, fill="x", padx=5)

        # Back button
        back_button = tk.Button(
            button_frame,
            text="Go Back",
            font=("Helvetica", 12),
            bg="#ffcc00",
            fg="#1e1e1e",
            activebackground="#ffcc00",
            activeforeground="#1e1e1e",
            cursor="hand2",
            command=self.go_back,
        )
        back_button.pack(side="left", expand=True, fill="x", padx=5)

    def start_search(self):
        # Parse input
        try:
            self.numbers = sorted(
                [int(x.strip()) for x in self.input_entry.get().split(",")]
            )
            self.target = int(self.target_entry.get())
        except ValueError:
            tk.messagebox.showerror(
                "Error",
                "Invalid input. Please enter comma-separated numbers and a valid target number.",
            )
            return

        # Clear previous visualization
        for widget in self.viz_frame.winfo_children():
            widget.destroy()

        # Create matplotlib figure and axis
        self.fig, self.ax = plt.subplots(figsize=(8, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.viz_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)

        # Disable start button and enable pause button
        self.start_button.config(state="disabled")
        self.pause_button.config(state="normal")

        # Start searching in a separate thread
        self.search_thread = threading.Thread(target=self.binary_search)
        self.search_thread.start()

    def binary_search(self):
        left, right = 0, len(self.numbers) - 1

        while left <= right:
            if self.is_paused:
                self.pause_event.wait()
            if self.step_mode:
                self.step_event.wait()
                self.step_event.clear()

            mid = (left + right) // 2
            self.visualize(left=left, right=right, mid=mid)
            time.sleep(self.speed)

            if self.numbers[mid] == self.target:
                self.visualize(left=left, right=right, mid=mid, found=True)
                tk.messagebox.showinfo(
                    "Search Result", f"Target {self.target} found at index {mid}"
                )
                break
            elif self.numbers[mid] < self.target:
                left = mid + 1
            else:
                right = mid - 1
        else:
            tk.messagebox.showinfo(
                "Search Result", f"Target {self.target} not found in the list"
            )

        # Re-enable start button and disable pause button
        self.start_button.config(state="normal")
        self.pause_button.config(state="disabled")

    def visualize(self, left, right, mid, found=False):
        self.ax.clear()
        bars = self.ax.bar(range(len(self.numbers)), self.numbers)

        for i, bar in enumerate(bars):
            if left <= i <= right:
                bar.set_color("b")
            if i == mid:
                bar.set_color("r" if not found else "g")

        self.ax.set_xlabel("Index")
        self.ax.set_ylabel("Value")
        self.ax.set_title("Binary Search Visualization")
        self.canvas.draw()
        self.viz_frame.update()

    def toggle_pause(self):
        if not hasattr(self, "pause_event"):
            self.pause_event = threading.Event()
            self.pause_event.set()

        if self.is_paused:
            self.pause_event.set()
            self.pause_button.config(text="Pause")
            self.is_paused = False
        else:
            self.pause_event.clear()
            self.pause_button.config(text="Resume")
            self.is_paused = True

    def update_speed(self, value):
        self.speed = float(value)

    def show_documentation(self):
        doc_window = tk.Toplevel(self.root)
        doc_window.title("Binary Search Documentation")
        doc_window.geometry("600x400")

        doc_text = tk.Text(doc_window, wrap=tk.WORD, font=("Helvetica", 12))
        doc_text.pack(expand=True, fill="both", padx=20, pady=20)

        documentation = """
        Binary Search Algorithm Documentation

        Binary Search is an efficient search algorithm that works on sorted arrays by repeatedly dividing the search interval in half.

        Time Complexity:
        - Worst Case: O(log n)
        - Average Case: O(log n)
        - Best Case: O(1)

        Space Complexity: O(1)

        Advantages:
        - Very efficient for large sorted datasets
        - Logarithmic time complexity

        Disadvantages:
        - Requires a sorted array
        - Not suitable for small datasets (linear search might be faster)

        Visualization Guide:
        - Blue bars: Current search range
        - Red bar: Middle element being checked
        - Green bar: Target element found

        Use the speed slider to adjust the visualization speed.
        Use the Step-by-Step mode to go through the algorithm one step at a time.
        """

        doc_text.insert(tk.END, documentation)
        doc_text.config(state="disabled")

    def ask_ai(self):
        ai_window = tk.Toplevel(self.root)
        ai_window.title("Q & A About Bubble Sort")
        ai_window.geometry("600x400")

        ai_text = tk.Text(ai_window, wrap=tk.WORD, font=("Helvetica", 12))
        ai_text.pack(expand=True, fill="both", padx=20, pady=20)

        qa = """
        1. what is binary search
        
        Binary Search is an efficient algorithm that searches for a target value in a sorted array by repeatedly dividing the search interval in half.",
        
        2. what is the time complexity
        
        The time complexity of Binary Search is O(log n) in the worst and average cases, where n is the number of elements in the array. In the best case (when the target is at the middle), it's O(1).",
        
        3. how does it compare to other search algorithms
        
        Binary Search is much more efficient than Linear Search for large sorted datasets, with a time complexity of O(log n) compared to Linear Search's O(n). However, it requires the data to be sorted first.",
        
        4. when should i use binary search
        
        Binary Search is ideal when you have a large, sorted dataset that you need to search frequently. It's particularly useful in situations where the cost of sorting the data once is outweighed by the benefits of faster subsequent searches.",
        """
        
        ai_text.insert(tk.END, qa)
        ai_text.config(state="disabled")

    def go_back(self):
        """Navigate back to the previous page."""
        from algorithmPage import AlgorithmPage  # Adjust import as necessary

        # Clear current widgets in the root window
        for widget in self.root.winfo_children():
            widget.destroy()

        AlgorithmPage(self.root, self.prev_page)  # Load the previous page


def create_algorithm_page(root, prev_page):
    """Wrapper function to create the Binary Search visualization page."""
    BinarySearchVisualization(root, prev_page)


# If you want to run this file standalone for testing
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Binary Search Visualization")
    root.geometry("800x600")
    BinarySearchVisualization(root, None)
    root.mainloop()
