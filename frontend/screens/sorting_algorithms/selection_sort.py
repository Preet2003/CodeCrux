import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import threading


class SelectionSortVisualization:
    def __init__(self, root, prev_page):
        self.root = root
        self.prev_page = prev_page
        self.is_paused = False
        self.speed = 0.5
        self.sorting_thread = None
        self.step_mode = False
        self.step_event = threading.Event()
        self.create_algorithm_page()

    def create_algorithm_page(self):
        """Set up the Selection Sort algorithm page."""
        # Clear current widgets in the root window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create a new frame for the algorithm page
        self.frame = tk.Frame(self.root, bg="#1e1e1e")
        self.frame.pack(expand=True, fill="both")

        # Heading (Algorithm Name)
        algo_label = tk.Label(
            self.frame,
            text="Selection Sort Visualization",
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
        button_frame.pack(fill="x", padx=20, pady=10)

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
        self.sorting_thread = threading.Thread(target=self.selection_sort)
        self.sorting_thread.start()

    def selection_sort(self):
        n = len(self.numbers)
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                if self.is_paused:
                    self.pause_event.wait()
                if self.step_mode:
                    self.step_event.wait()
                    self.step_event.clear()

                self.visualize(highlight=[i, j], min_idx=min_idx)
                time.sleep(self.speed)

                if self.numbers[j] < self.numbers[min_idx]:
                    min_idx = j

            self.numbers[i], self.numbers[min_idx] = (
                self.numbers[min_idx],
                self.numbers[i],
            )
            self.visualize(highlight=[i, min_idx])
            time.sleep(self.speed)

        self.visualize(sorted=True)

        # Re-enable start button and disable pause button
        self.start_button.config(state="normal")
        self.pause_button.config(state="disabled")

    def visualize(self, highlight=[], min_idx=None, sorted=False):
        self.ax.clear()
        bars = self.ax.bar(range(len(self.numbers)), self.numbers)

        for i, bar in enumerate(bars):
            if i in highlight:
                bar.set_color("r")
            elif i == min_idx:
                bar.set_color("g")
            elif sorted:
                bar.set_color("g")

        self.ax.set_xlabel("Index")
        self.ax.set_ylabel("Value")
        self.ax.set_title("Selection Sort Visualization")
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
        doc_window.title("Selection Sort Documentation")
        doc_window.geometry("600x400")

        doc_text = tk.Text(doc_window, wrap=tk.WORD, font=("Helvetica", 12))
        doc_text.pack(expand=True, fill="both", padx=20, pady=20)

        documentation = """
        Selection Sort Algorithm Documentation

        Selection Sort is a simple comparison-based sorting algorithm. It divides the input list into two parts: a sorted portion at the left end and an unsorted portion at the right end. Initially, the sorted portion is empty and the unsorted portion is the entire list.

        Time Complexity:
        - Worst Case: O(n^2)
        - Average Case: O(n^2)
        - Best Case: O(n^2)

        Space Complexity: O(1)

        Advantages:
        - Simple implementation
        - Performs well on small lists
        - In-place sorting algorithm (doesn't require much additional memory)

        Disadvantages:
        - Inefficient for large lists
        - Not stable (doesn't preserve the relative order of equal elements)

        Visualization Guide:
        - Red bars: Elements being compared
        - Green bar: Current minimum element in the unsorted portion
        - Blue bars: Unsorted elements
        - Green bars: Sorted elements (final state)

        Use the speed slider to adjust the visualization speed.
        Use the Step-by-Step mode to go through the algorithm one step at a time.
        """

        doc_text.insert(tk.END, documentation)
        doc_text.config(state="disabled")

    def ask_ai(self):
        ai_window = tk.Toplevel(self.root)
        ai_window.title("Q & A About Selection Sort")
        ai_window.geometry("600x400")

        ai_text = tk.Text(ai_window, wrap=tk.WORD, font=("Helvetica", 12))
        ai_text.pack(expand=True, fill="both", padx=20, pady=20)

        qa = """
        1. what is selection sort
        
        Selection Sort is a simple comparison-based sorting algorithm that works by repeatedly finding the minimum element from the unsorted part of the list and putting it at the beginning of the sorted part.",
        
        2. what is the time complexity
        
        The time complexity of Selection Sort is O(n^2) for all cases (worst, average, and best), where n is the number of elements to be sorted.",
        
        3. how does it compare to other sorting algorithms
        
        Selection Sort is generally less efficient than more advanced algorithms like Quick Sort or Merge Sort for large datasets. However, it has the advantage of being simple to implement and performs well on small lists.",
        
        4. is selection sort stable
        
        No, Selection Sort is not a stable sorting algorithm. It does not preserve the relative order of equal elements in the sorted output.",
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
    """Wrapper function to create the Selection Sort visualization page."""
    SelectionSortVisualization(root, prev_page)


## If you want to run this file standalone for testing
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Selection Sort Visualization")
    root.geometry("800x600")
    SelectionSortVisualization(root, None)
    root.mainloop()
