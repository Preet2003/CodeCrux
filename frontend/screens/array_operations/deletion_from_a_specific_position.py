import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import threading

class DeleteFromArrayVisualization:
    def __init__(self, root, prev_page):
        self.root = root
        self.prev_page = prev_page
        self.is_paused = False
        self.speed = 0.5
        self.operation_thread = None
        self.step_mode = False
        self.step_event = threading.Event()
        self.create_algorithm_page()

    def create_algorithm_page(self):
        """Set up the Delete From Array algorithm page."""
        # Clear current widgets in the root window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create a new frame for the algorithm page
        self.frame = tk.Frame(self.root, bg="#1e1e1e")
        self.frame.pack(expand=True, fill="both")

        # Heading (Algorithm Name)
        algo_label = tk.Label(
            self.frame,
            text="Delete From Array Visualization",
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
            text="Enter numbers (comma-separated):",
            fg="#ffffff",
            bg="#1e1e1e",
        )
        input_label.pack(side="left", expand=True, fill="x", padx=20, pady=(10, 5))
        self.input_entry = tk.Entry(entry_frame, width=40)
        self.input_entry.pack(side="left", expand=True, fill="x", padx=20)

        # Input field for target number
        position_label = tk.Label(
            field_frame, text="Enter position to delete (0-indexed):", fg="#ffffff", bg="#1e1e1e"
        )
        position_label.pack(side="left", expand=True, fill="x", padx=20,pady=(10, 5))
        self.position_entry = tk.Entry(entry_frame, width=10)
        self.position_entry.pack(side="left", expand=True, fill="x", padx=20)

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
        self.speed_slider = ttk.Scale(button_frame, from_=0.1, to=2.0, orient="horizontal", length=200, value=0.5, command=self.update_speed)
        self.speed_slider.pack(side="left", padx=(10, 0))

        # Start button
        self.start_button = tk.Button(
            button_frame,
            text="Start Operation",
            font=("Helvetica", 12),
            bg="#ffcc00",
            fg="#1e1e1e",
            activebackground="#ffcc00",
            activeforeground="#1e1e1e",
            cursor="hand2",
            command=self.start_operation
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
            state="disabled"
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
            command=self.show_documentation
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
            command=self.ask_ai
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
            command=self.go_back
        )
        back_button.pack(side="left", expand=True, fill="x", padx=5)

    def start_operation(self):
        # Parse input
        try:
            self.numbers = [int(x.strip()) for x in self.input_entry.get().split(',')]
            self.delete_position = int(self.position_entry.get())
            if self.delete_position < 0 or self.delete_position >= len(self.numbers):
                raise ValueError("Invalid delete position")
        except ValueError as e:
            tk.messagebox.showerror("Error", str(e))
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

        # Start operation in a separate thread
        self.operation_thread = threading.Thread(target=self.delete_from_array)
        self.operation_thread.start()

    def delete_from_array(self):
        self.visualize(highlight=self.delete_position)
        time.sleep(self.speed)

        # Delete the element
        del self.numbers[self.delete_position]

        # Shift elements
        for i in range(self.delete_position, len(self.numbers)):
            if self.is_paused:
                self.pause_event.wait()
            if self.step_mode:
                self.step_event.wait()
                self.step_event.clear()

            self.visualize(highlight=i)
            time.sleep(self.speed)

        self.visualize()  # Final state

        # Re-enable start button and disable pause button
        self.start_button.config(state="normal")
        self.pause_button.config(state="disabled")

    def visualize(self, highlight=None):
        self.ax.clear()
        bars = self.ax.bar(range(len(self.numbers)), self.numbers)
        
        if highlight is not None:
            bars[highlight].set_color('r')
        
        self.ax.set_xlabel('Index')
        self.ax.set_ylabel('Value')
        self.ax.set_title('Delete From Array Visualization')
        self.canvas.draw()
        self.viz_frame.update()

    def toggle_pause(self):
        if not hasattr(self, 'pause_event'):
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
        doc_window.title("Delete From Array Documentation")
        doc_window.geometry("600x400")
        
        doc_text = tk.Text(doc_window, wrap=tk.WORD, font=("Helvetica", 12))
        doc_text.pack(expand=True, fill="both", padx=20, pady=20)
        
        documentation = """
        Delete From Array Operation Documentation

        This operation removes an element from a specific position in the array and shifts the remaining elements to fill the gap.

        Time Complexity:
        - Worst Case: O(n)
        - Average Case: O(n)
        - Best Case: O(1) (when deleting the last element)

        Space Complexity: O(1)

        Steps:
        1. Remove the element at the specified position.
        2. Shift all elements after the deleted position one step to the left.
        3. Decrease the size of the array by 1.

        Visualization Guide:
        - Red bar: Element being deleted or position being shifted
        - Blue bars: Unaffected elements

        Use the speed slider to adjust the visualization speed.
        Use the Step-by-Step mode to go through the operation one step at a time.
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
        1. what is delete from array
        
        Delete From Array is an operation that removes an element from a specific position in the array and shifts the remaining elements to fill the gap.",
        
        2. what is the time complexity
        
        The time complexity of Delete From Array is O(n) in the worst and average cases, where n is the number of elements in the array. In the best case (when deleting the last element), it's O(1).",
        
        3. how does it work
        
        The operation works by first removing the element at the specified position, then shifting all elements after the deleted position one step to the left, and finally decreasing the size of the array by 1.",
        
        4. what are the applications
        
        Delete From Array is commonly used in dynamic array implementations, stack and queue data structures, and in algorithms that require removing elements from a list or array.",
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
    """Wrapper function to create the Delete From Array visualization page."""
    DeleteFromArrayVisualization(root, prev_page)

# If you want to run this file standalone for testing
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Delete From Array Visualization")
    root.geometry("800x600")
    DeleteFromArrayVisualization(root, None)
    root.mainloop()

