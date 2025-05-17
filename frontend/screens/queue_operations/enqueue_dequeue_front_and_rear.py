import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import threading
import queue


class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if not self.is_empty():
            return self.items.pop(0)
        return None

    def front(self):
        if not self.is_empty():
            return self.items[0]
        return None

    def rear(self):
        if not self.is_empty():
            return self.items[-1]
        return None

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

    def get_items(self):
        return self.items.copy()


class QueueVisualization:
    def __init__(self, root, prev_page):
        self.root = root
        self.prev_page = prev_page
        self.queue = Queue()
        self.is_paused = False
        self.speed = 0.5
        self.operation_thread = None
        self.step_mode = False
        self.step_event = threading.Event()
        self.update_queue = queue.Queue()
        self.create_algorithm_page()

    def create_algorithm_page(self):
        """Set up the Queue operations visualization page."""
        # Clear current widgets in the root window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create a new frame for the algorithm page
        self.frame = tk.Frame(self.root, bg="#1e1e1e")
        self.frame.pack(expand=True, fill="both")

        # Heading (Algorithm Name)
        algo_label = tk.Label(
            self.frame,
            text="Queue Operations Visualization",
            font=("Helvetica", 20, "bold"),
            fg="#ffffff",
            bg="#1e1e1e",
        )
        algo_label.pack(pady=(20, 10))

        # Operation selection dropdown
        self.operation_var = tk.StringVar(value="Enqueue")
        operations = ["Enqueue", "Dequeue", "Front and Rear"]
        operation_menu = ttk.OptionMenu(
            self.frame,
            self.operation_var,
            "Enqueue",
            *operations,
            command=self.update_input_visibility,
        )
        operation_menu.pack(pady=(0, 10))

        # Input field for value to enqueue
        self.input_frame = tk.Frame(self.frame, bg="#1e1e1e")
        self.input_frame.pack(pady=(0, 10))

        self.value_label = tk.Label(
            self.input_frame, text="Value to Enqueue:", fg="#ffffff", bg="#1e1e1e"
        )
        self.value_label.grid(row=0, column=0, padx=5, pady=5)
        self.value_entry = tk.Entry(self.input_frame, width=10)
        self.value_entry.grid(row=0, column=1, padx=5, pady=5)

        # Visualization frame
        self.viz_frame = tk.Frame(self.frame, bg="#1e1e1e")
        self.viz_frame.pack(fill="both", padx=20, pady=20)

        # Buttons frame
        button_frame = tk.Frame(self.frame, bg="#1e1e1e")
        button_frame.pack(fill="x", padx=20, pady=10)

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

        # Operation button
        self.operation_button = tk.Button(
            button_frame,
            text="Start Operation",
            font=("Helvetica", 12),
            bg="#ffcc00",
            fg="#1e1e1e",
            activebackground="#ffcc00",
            activeforeground="#1e1e1e",
            cursor="hand2",
            command=self.start_operation,
        )
        self.operation_button.pack(side="left", expand=True, fill="x", padx=5)

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

        # Create initial visualization
        self.visualize()

        # Start the update loop
        self.root.after(100, self.update_gui)

    def update_input_visibility(self, *args):
        if self.operation_var.get() == "Enqueue":
            self.input_frame.pack(pady=(0, 10))
        else:
            self.input_frame.pack_forget()

    def start_operation(self):
        operation = self.operation_var.get()

        if operation == "Enqueue":
            try:
                value = int(self.value_entry.get())
            except ValueError:
                tk.messagebox.showerror("Error", "Please enter a valid integer.")
                return

        if operation in ["Dequeue", "Front and Rear"] and self.queue.is_empty():
            tk.messagebox.showerror(
                "Error", "Cannot perform operation on an empty queue."
            )
            return

        # Disable operation button and enable pause button
        self.operation_button.config(state="disabled")
        self.pause_button.config(state="normal")

        # Start operation in a separate thread
        self.operation_thread = threading.Thread(
            target=self.perform_operation, args=(operation,)
        )
        self.operation_thread.start()

    def perform_operation(self, operation):
        if operation == "Enqueue":
            value = int(self.value_entry.get())
            self.queue.enqueue(value)
            self.update_queue.put(("highlight", len(self.queue.get_items()) - 1))
        elif operation == "Dequeue":
            dequeued_value = self.queue.dequeue()
            self.update_queue.put(("highlight", 0))
            self.update_queue.put(("message", f"Dequeued value: {dequeued_value}"))
        elif operation == "Front and Rear":
            front_value = self.queue.front()
            rear_value = self.queue.rear()
            self.update_queue.put(
                ("highlight_front_rear", (0, len(self.queue.get_items()) - 1))
            )
            self.update_queue.put(
                ("message", f"Front: {front_value}, Rear: {rear_value}")
            )

        time.sleep(self.speed)
        self.update_queue.put(("enable_buttons", None))

    def update_gui(self):
        try:
            while True:
                action, data = self.update_queue.get_nowait()
                if action == "highlight":
                    self.visualize(highlight=data)
                elif action == "highlight_front_rear":
                    self.visualize(highlight_front=data[0], highlight_rear=data[1])
                elif action == "message":
                    tk.messagebox.showinfo("Operation Result", data)
                elif action == "enable_buttons":
                    self.operation_button.config(state="normal")
                    self.pause_button.config(state="disabled")
        except queue.Empty:
            pass
        finally:
            self.root.after(100, self.update_gui)

    def visualize(self, highlight=None, highlight_front=None, highlight_rear=None):
        # Clear previous visualization
        for widget in self.viz_frame.winfo_children():
            widget.destroy()

        # Create matplotlib figure and axis
        fig, ax = plt.subplots(figsize=(8, 4))
        canvas = FigureCanvasTkAgg(fig, master=self.viz_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)
        canvas_widget.configure(height=400, width=400)

        items = self.queue.get_items()
        n = len(items)

        box_width = 0.6
        box_height = 0.6

        if n == 0:
            ax.text(0.5, 0.5, "Queue is empty", ha="center", va="center", fontsize=12)
        else:
            for i, item in enumerate(items):
                color = "lightblue"
                if i == highlight or i == highlight_front:
                    color = "yellow"
                elif i == highlight_rear:
                    color = "lightgreen"
                ax.add_patch(
                    plt.Rectangle(
                        (i * box_width, 0.2),
                        box_width,
                        box_height,
                        fill=True,
                        facecolor=color,
                        edgecolor="black",
                        linewidth=2,
                    )
                )
                ax.text(
                    i * box_width + box_width / 2,
                    0.5,
                    str(item),
                    ha="center",
                    va="center",
                    fontsize=10,
                    fontweight="bold",
                )

            # Add front and rear labels
            ax.text(0, 0, "Front", ha="center", va="center", fontsize=10)
            ax.text(
                (n - 1) * box_width, 0, "Rear", ha="center", va="center", fontsize=10
            )

        ax.set_xlim(-0.2, max(n * box_width, 1))
        ax.set_ylim(0, 1)
        ax.axis("off")
        ax.set_title("Queue Visualization")
        canvas.draw()

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
        doc_window.title("Queue Operations Documentation")
        doc_window.geometry("600x400")

        doc_text = tk.Text(doc_window, wrap=tk.WORD, font=("Helvetica", 12))
        doc_text.pack(expand=True, fill="both", padx=20, pady=20)

        documentation = """
        Queue Operations Documentation

        1. Enqueue Operation:
           - Adds an element to the rear of the queue.
           - Time Complexity: O(1)
           - Space Complexity: O(1)

        2. Dequeue Operation:
           - Removes and returns the front element from the queue.
           - Time Complexity: O(1)
           - Space Complexity: O(1)

        3. Front and Rear Operation:
           - Returns the front and rear elements of the queue without removing them.
           - Time Complexity: O(1)
           - Space Complexity: O(1)

        Visualization Guide:
        - Blue rectangles: Elements in the queue
        - Yellow rectangle: Element being operated on (enqueue, dequeue, or front)
        - Green rectangle: Rear element (when showing front and rear)
        - Queue grows from left to right, with the front on the left and rear on the right

        Use the speed slider to adjust the visualization speed.
        """

        doc_text.insert(tk.END, documentation)
        doc_text.config(state="disabled")

    def ask_ai(self):
        ai_window = tk.Toplevel(self.root)
        ai_window.title("Q & A About Queue Operations")
        ai_window.geometry("600x400")

        ai_text = tk.Text(ai_window, wrap=tk.WORD, font=("Helvetica", 12))
        ai_text.pack(expand=True, fill="both", padx=20, pady=20)

        qa = """
        1. What are the main operations of a queue?
        
        The main operations of a queue are:
        - Enqueue: Adds an element to the rear of the queue.
        - Dequeue: Removes and returns the front element from the queue.
        - Front: Returns the front element without removing it.
        - Rear: Returns the rear element without removing it.
        
        2. What is the time complexity of queue operations?
        
        The time complexity for enqueue, dequeue, front, and rear operations in a queue is typically O(1), which means they take constant time regardless of the queue's size.
        
        3. What is FIFO and how does it relate to queues?
        
        FIFO stands for First-In-First-Out. It's the principle that governs how queues work. The first element added to the queue (enqueued) is the first one to be removed (dequeued).
        
        4. What are some applications of queues?
        
        Queues are used in many applications, including:
        - Task scheduling in operating systems
        - Breadth-First Search algorithms in graph theory
        - Handling of requests in web servers
        - Buffering in data streams
        - Printer job scheduling
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
    """Wrapper function to create the Queue operations visualization page."""
    QueueVisualization(root, prev_page)

# If you want to run this file standalone for testing
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Queue Operations Visualization")
    root.geometry("800x600")
    QueueVisualization(root, None)
    root.mainloop()
