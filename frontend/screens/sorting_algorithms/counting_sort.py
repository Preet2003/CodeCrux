import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import threading


class CountingSortVisualization:
    def __init__(self, root, prev_page):
        self.root = root
        self.prev_page = prev_page
        self.is_paused = False
        self.speed = 0.5
        self.sorting_thread = None
        self.create_algorithm_page()

    def create_algorithm_page(self):
        """Set up the Counting Sort algorithm page."""
        # Clear current widgets in the root window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create a new frame for the algorithm page
        self.frame = tk.Frame(self.root, bg="#1e1e1e")
        self.frame.pack(expand=True, fill="both")

        # Heading (Algorithm Name)
        algo_label = tk.Label(
            self.frame,
            text="Counting Sort Visualization",
            font=("Helvetica", 20, "bold"),
            fg="#ffffff",
            bg="#1e1e1e",
        )
        algo_label.pack(pady=(20, 10))

        # Input field for numbers
        input_label = tk.Label(
            self.frame,
            text="Enter numbers (comma-separated):",
            fg="#ffffff",
            bg="#1e1e1e",
        )
        input_label.pack(pady=(10, 5))
        self.input_entry = tk.Entry(self.frame, width=40)
        self.input_entry.pack(pady=(0, 10))

        # Visualization frame
        self.viz_frame = tk.Frame(self.frame, bg="#1e1e1e")
        self.viz_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Buttons frame
        button_frame = tk.Frame(self.frame, bg="#1e1e1e")
        button_frame.pack(side="bottom", fill="x", padx=20, pady=10)

        # Speed control slider
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
            text="Start Sorting",
            font=("Helvetica", 12),
            bg="#ffcc00",
            fg="#1e1e1e",
            activebackground="#ffcc00",
            activeforeground="#1e1e1e",
            cursor="hand2",
            command=self.start_sorting,
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

    def start_sorting(self):
        # Parse input
        try:
            self.numbers = [int(x.strip()) for x in self.input_entry.get().split(",")]
        except ValueError:
            tk.messagebox.showerror(
                "Error", "Invalid input. Please enter comma-separated numbers."
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

        # Start sorting in a separate thread
        self.sorting_thread = threading.Thread(target=self.counting_sort)
        self.sorting_thread.start()

    def counting_sort(self):
        n = len(self.numbers)
        max_val = max(self.numbers)
        min_val = min(self.numbers)
        range_val = max_val - min_val + 1

        count = [0] * range_val
        output = [0] * n

        for i in range(n):
            if self.is_paused:
                self.pause_event.wait()

            count[self.numbers[i] - min_val] += 1
            self.visualize(self.numbers, highlight=[i])
            time.sleep(self.speed)

        for i in range(1, range_val):
            if self.is_paused:
                self.pause_event.wait()

            count[i] += count[i - 1]
            self.visualize(count, highlight=[i, i - 1])
            time.sleep(self.speed)

        for i in range(n - 1, -1, -1):
            if self.is_paused:
                self.pause_event.wait()

            output[count[self.numbers[i] - min_val] - 1] = self.numbers[i]
            count[self.numbers[i] - min_val] -= 1
            self.visualize(output, highlight=[count[self.numbers[i] - min_val]])
            time.sleep(self.speed)

        self.numbers = output
        self.visualize(self.numbers)

        # Re-enable start button and disable pause button
        self.start_button.config(state="normal")
        self.pause_button.config(state="disabled")

    def visualize(self, data, highlight=[]):
        self.ax.clear()
        bars = self.ax.bar(range(len(data)), data)
        for i in highlight:
            if 0 <= i < len(data):
                bars[i].set_color("r")
        self.ax.set_xlabel("Index")
        self.ax.set_ylabel("Value")
        self.ax.set_title("Counting Sort Visualization")
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
        doc_window.title("Counting Sort Documentation")
        doc_window.geometry("600x400")

        doc_text = tk.Text(doc_window, wrap=tk.WORD, font=("Helvetica", 12))
        doc_text.pack(expand=True, fill="both", padx=20, pady=20)

        documentation = """
        Counting Sort Algorithm Documentation

        Counting Sort is an integer sorting algorithm that operates by counting the number of objects that possess distinct key values, and applying prefix sum on those counts to determine the positions of each key value in the output sequence.

        Time Complexity: O(n + k), where n is the number of elements and k is the range of input
        Space Complexity: O(n + k)

        Advantages:
        - Efficient for sorting integers or strings with small range
        - Stable sorting algorithm

        Disadvantages:
        - Not suitable for large ranges of input values
        - Requires extra space proportional to the range of input

        Visualization Guide:
        - Blue bars: Unsorted/intermediate elements
        - Red bars: Elements being processed or compared

        Use the speed slider to adjust the visualization speed.
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
        1. what is counting sort
        
        Counting Sort is a non-comparison-based sorting algorithm that works by counting the number of objects having distinct key values, and using arithmetic to determine the positions of each key value in the output sequence.
        
        2. what is the time complexity
        
        The time complexity of Counting Sort is O(n + k), where n is the number of elements and k is the range of input.
        
        3. how does it compare to other sorting algorithms
        
        Counting Sort is very efficient for sorting integers or strings with small ranges. It outperforms comparison-based sorting algorithms like Quick Sort or Merge Sort for such inputs. However, it's not suitable for large ranges of input values."""
        
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
    """Wrapper function to create the Counting Sort visualization page."""
    CountingSortVisualization(root, prev_page)


# If you want to run this file standalone for testing
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Counting Sort Visualization")
    root.geometry("800x600")
    CountingSortVisualization(root, None)
    root.mainloop()
