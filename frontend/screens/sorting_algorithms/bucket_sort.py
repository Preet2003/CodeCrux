import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import threading


class BucketSortVisualization:
    def __init__(self, root, prev_page):
        self.root = root
        self.prev_page = prev_page
        self.is_paused = False
        self.speed = 0.5
        self.sorting_thread = None
        self.create_algorithm_page()

    def create_algorithm_page(self):
        """Set up the Bucket Sort algorithm page."""
        # Clear current widgets in the root window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create a new frame for the algorithm page
        self.frame = tk.Frame(self.root, bg="#1e1e1e")
        self.frame.pack(expand=True, fill="both")

        # Heading (Algorithm Name)
        algo_label = tk.Label(
            self.frame,
            text="Bucket Sort Visualization",
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
            self.numbers = [float(x.strip()) for x in self.input_entry.get().split(",")]
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
        self.sorting_thread = threading.Thread(target=self.bucket_sort)
        self.sorting_thread.start()

    def bucket_sort(self):
        # Find range of values
        min_val, max_val = min(self.numbers), max(self.numbers)

        # Create buckets
        bucket_range = (max_val - min_val) / 10
        buckets = [[] for _ in range(10)]

        # Distribute elements into buckets
        for num in self.numbers:
            if self.is_paused:
                self.pause_event.wait()

            index = int((num - min_val) // bucket_range)
            if index != 10:
                buckets[index].append(num)
            else:
                buckets[9].append(num)

            self.visualize_buckets(buckets)
            time.sleep(self.speed)

        # Sort individual buckets
        sorted_array = []
        for bucket in buckets:
            bucket.sort()
            sorted_array.extend(bucket)
            self.visualize_buckets(buckets, sorted_array)
            time.sleep(self.speed)

        self.numbers = sorted_array
        self.visualize(self.numbers)

        # Re-enable start button and disable pause button
        self.start_button.config(state="normal")
        self.pause_button.config(state="disabled")

    def visualize_buckets(self, buckets, sorted_array=None):
        self.ax.clear()

        total_elements = sum(len(bucket) for bucket in buckets)
        bar_width = 0.8 / total_elements

        x = 0
        for i, bucket in enumerate(buckets):
            for element in bucket:
                self.ax.bar(x, element, width=bar_width, color="b", align="edge")
                x += bar_width

            if i < len(buckets) - 1:
                self.ax.axvline(x, color="r", linestyle="--")

        if sorted_array:
            sorted_x = [i * bar_width for i in range(len(sorted_array))]
            self.ax.bar(
                sorted_x, sorted_array, width=bar_width, color="g", align="edge"
            )

        self.ax.set_xlabel("Buckets")
        self.ax.set_ylabel("Value")
        self.ax.set_title("Bucket Sort Visualization")
        self.canvas.draw()
        self.viz_frame.update()

    def visualize(self, data):
        self.ax.clear()
        self.ax.bar(range(len(data)), data)
        self.ax.set_xlabel("Index")
        self.ax.set_ylabel("Value")
        self.ax.set_title("Bucket Sort Visualization")
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
        doc_window.title("Bucket Sort Documentation")
        doc_window.geometry("600x400")

        doc_text = tk.Text(doc_window, wrap=tk.WORD, font=("Helvetica", 12))
        doc_text.pack(expand=True, fill="both", padx=20, pady=20)

        documentation = """
        Bucket Sort Algorithm Documentation

        Bucket Sort is a distribution sort that works by distributing the elements of an array into a number of buckets. Each bucket is then sorted individually, either using a different sorting algorithm, or by recursively applying the bucket sorting algorithm.

        Time Complexity: 
        - Average case: O(n + k)
        - Worst case: O(n^2)
        where n is the number of elements and k is the number of buckets

        Space Complexity: O(n + k)

        Advantages:
        - Efficient when input is uniformly distributed over a range
        - Can be used as an external sort

        Disadvantages:
        - Not efficient when data is not uniformly distributed
        - Requires linked lists or dynamic arrays for bucket storage

        Visualization Guide:
        - Blue bars: Elements in buckets
        - Red lines: Bucket separators
        - Green bars: Sorted elements

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
        1. what is bucket sort
        
        Bucket Sort is a sorting algorithm that works by distributing the elements of an array into a number of buckets. Each bucket is then sorted individually, either using a different sorting algorithm, or by recursively applying the bucket sorting algorithm.
        
        2. what is the time complexity
        
        The average time complexity of Bucket Sort is O(n + k), where n is the number of elements and k is the number of buckets. However, in the worst case, it can be O(n^2) if all elements are placed into a single bucket.
        
        3. how does it compare to other sorting algorithms
        
        Bucket Sort can be very efficient when the input is uniformly distributed over a range, outperforming comparison-based sorting algorithms like Quick Sort or Merge Sort in such cases. However, it's not as efficient when the data is not uniformly distributed."""
        
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
    """Wrapper function to create the Bucket Sort visualization page."""
    BucketSortVisualization(root, prev_page)


# If you want to run this file standalone for testing
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Bucket Sort Visualization")
    root.geometry("800x600")
    BucketSortVisualization(root, None)
    root.mainloop()
