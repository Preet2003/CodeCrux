import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import threading


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class SinglyLinkedList:
    def __init__(self):
        self.head = None

    def insert_at_beginning(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def insert_at_end(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

    def insert_at_position(self, data, position):
        if position == 0:
            self.insert_at_beginning(data)
            return
        new_node = Node(data)
        current = self.head
        for _ in range(position - 1):
            if current is None:
                raise IndexError("Position out of range")
            current = current.next
        new_node.next = current.next
        current.next = new_node

    def delete_at_beginning(self):
        if not self.head:
            return
        self.head = self.head.next

    def delete_at_end(self):
        if not self.head:
            return
        if not self.head.next:
            self.head = None
            return
        current = self.head
        while current.next.next:
            current = current.next
        current.next = None

    def delete_at_position(self, position):
        if not self.head:
            return
        if position == 0:
            self.head = self.head.next
            return
        current = self.head
        for _ in range(position - 1):
            if current is None or current.next is None:
                raise IndexError("Position out of range")
            current = current.next
        current.next = current.next.next

    def traverse(self):
        elements = []
        current = self.head
        while current:
            elements.append(current.data)
            current = current.next
        return elements

    def search(self, data):
        current = self.head
        position = 0
        while current:
            if current.data == data:
                return position
            current = current.next
            position += 1
        return -1


class SinglyLinkedListVisualization:
    def __init__(self, root, prev_page):
        self.root = root
        self.prev_page = prev_page
        self.linked_list = SinglyLinkedList()
        self.is_paused = False
        self.speed = 0.5
        self.operation_thread = None
        self.step_mode = False
        self.step_event = threading.Event()
        self.create_algorithm_page()

    def create_algorithm_page(self):
        """Set up the Singly Linked List algorithm page."""
        # Clear current widgets in the root window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create a new frame for the algorithm page
        self.frame = tk.Frame(self.root, bg="#1e1e1e")
        self.frame.pack(expand=True, fill="both")

        # Heading (Algorithm Name)
        algo_label = tk.Label(
            self.frame,
            text="Singly Linked List Visualization",
            font=("Helvetica", 20, "bold"),
            fg="#ffffff",
            bg="#1e1e1e",
        )
        algo_label.pack(pady=(20, 10))

        # Fields frame
        field_frame = tk.Frame(self.frame, bg="#1e1e1e")
        field_frame.pack(fill="x", padx=20, pady=5)

        # Operation selection dropdown
        self.operation_var = tk.StringVar()
        self.operation_var.set("Insert at Beginning")  # default value
        operations = [
            "Insert at Beginning",
            "Insert at End",
            "Insert at Position",
            "Delete at Beginning",
            "Delete at End",
            "Delete at Position",
            "Traverse",
            "Search",
        ]
        operation_menu = ttk.OptionMenu(
            field_frame,
            self.operation_var,
            "Insert at Beginning",
            *operations,
            command=self.on_operation_change,
        )
        operation_menu.pack(side="left", expand=True, fill="x", padx=20, pady=(10, 5))

        # Input fields container
        self.input_frame = tk.Frame(field_frame, bg="#1e1e1e")
        self.input_frame.pack(side="left", expand=True, fill="x", padx=20)

        # Value input (always visible)
        self.value_label = tk.Label(
            self.input_frame, text="Value:", fg="#ffffff", bg="#1e1e1e"
        )
        self.value_label.pack(side="left", expand=True, fill="x", padx=(0, 5), pady=(10, 5))
        self.value_entry = tk.Entry(self.input_frame, width=10)
        self.value_entry.pack(side="left", expand=True, fill="x", padx=(0, 5))

        # Position input (initially hidden)
        self.position_label = tk.Label(
            self.input_frame, text="Position:", fg="#ffffff", bg="#1e1e1e"
        )
        self.position_entry = tk.Entry(self.input_frame, width=10)

        # Initially set up for default operation
        self.on_operation_change("Insert at Beginning")

        # Rest of the method remains the same as in the previous implementation
        # ... (Visualization frame, buttons, etc.)

        # Visualization frame
        self.viz_frame = tk.Frame(self.frame, bg="#1e1e1e")
        self.viz_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Buttons frame
        button_frame = tk.Frame(self.frame, bg="#1e1e1e")
        button_frame.pack(fill="x", padx=20, pady=5)

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
            text="Start Operation",
            font=("Helvetica", 12),
            bg="#ffcc00",
            fg="#1e1e1e",
            activebackground="#ffcc00",
            activeforeground="#1e1e1e",
            cursor="hand2",
            command=self.start_operation,
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

    def on_operation_change(self, operation):
        """
        Show/hide position input based on selected operation
        """
        # First, remove existing position label and entry if they exist
        if hasattr(self, "position_label"):
            self.position_label.pack_forget()
        if hasattr(self, "position_entry"):
            self.position_entry.pack_forget()
        if hasattr(self, "value_label"):
            self.value_label.pack_forget()
        if hasattr(self, "value_entry"):
            self.value_entry.pack_forget()
        

        # Only show position input for operations that require it
        if operation in ["Insert at Position", "Delete at Position"]:
            self.position_label.pack(
                side="left", expand=True, fill="x", padx=(10, 5), pady=(10, 5)
            )
            self.position_entry.pack(side="left", expand=True, fill="x", padx=(0, 5))

        if operation in ["Insert at Beginning", "Insert at Position", "Insert at End", "Search"]:
            self.value_label.pack(
                side="left", expand=True, fill="x", padx=(10, 5), pady=(10, 5)
            )
            self.value_entry.pack(side="left", expand=True, fill="x", padx=(0, 5))

    def start_operation(self):
        operation = self.operation_var.get()

        try:
            if operation in [
                "Insert at Beginning",
                "Insert at End",
                "Insert at Position",
                "Search",
            ]:
                value = int(self.value_entry.get())
            if operation in ["Insert at Position", "Delete at Position"]:
                position = int(self.position_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid integer values.")
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
        self.operation_thread = threading.Thread(
            target=self.perform_operation, args=(operation,)
        )
        self.operation_thread.start()

    def perform_operation(self, operation):
        if operation == "Insert at Beginning":
            value = int(self.value_entry.get())
            self.linked_list.insert_at_beginning(value)
        elif operation == "Insert at End":
            value = int(self.value_entry.get())
            self.linked_list.insert_at_end(value)
        elif operation == "Insert at Position":
            value = int(self.value_entry.get())
            position = int(self.position_entry.get())
            self.linked_list.insert_at_position(value, position)
        elif operation == "Delete at Beginning":
            self.linked_list.delete_at_beginning()
        elif operation == "Delete at End":
            self.linked_list.delete_at_end()
        elif operation == "Delete at Position":
            position = int(self.position_entry.get())
            self.linked_list.delete_at_position(position)
        elif operation == "Traverse":
            elements = self.linked_list.traverse()
            self.visualize(elements, highlight=list(range(len(elements))))
        elif operation == "Search":
            value = int(self.value_entry.get())
            position = self.linked_list.search(value)
            elements = self.linked_list.traverse()
            if position != -1:
                self.visualize(elements, highlight=[position])
            else:
                self.visualize(elements)
                messagebox.showinfo(
                    "Search Result", f"Value {value} not found in the list."
                )

        self.visualize(self.linked_list.traverse())

        # Re-enable start button and disable pause button
        self.start_button.config(state="normal")
        self.pause_button.config(state="disabled")

    # Rest of the methods remain the same as in the previous implementation
    def visualize(self, elements, highlight=None):
        self.ax.clear()
        x = list(range(len(elements)))
        y = [0] * len(elements)

        # Plot nodes
        self.ax.scatter(x, y, s=500, c="lightblue", zorder=2)

        # Plot arrows
        for i in range(len(elements) - 1):
            self.ax.annotate(
                "",
                xy=(i + 1, 0),
                xytext=(i, 0),
                arrowprops=dict(arrowstyle="->", color="gray"),
            )

        # Add node values
        for i, val in enumerate(elements):
            self.ax.text(i, 0, str(val), ha="center", va="center", fontweight="bold")

        # Highlight specific nodes if needed
        if highlight:
            self.ax.scatter(
                [x[i] for i in highlight],
                [y[i] for i in highlight],
                s=600,
                c="yellow",
                zorder=1,
            )

        self.ax.set_xlim(-0.5, len(elements) - 0.5)
        self.ax.set_ylim(-0.5, 0.5)
        self.ax.axis("off")
        self.ax.set_title("Singly Linked List Visualization")
        self.canvas.draw()
        self.viz_frame.update()

        if not self.step_mode:
            time.sleep(self.speed)

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
        doc_window.title("Singly Linked List Documentation")
        doc_window.geometry("600x400")

        doc_text = tk.Text(doc_window, wrap=tk.WORD, font=("Helvetica", 12))
        doc_text.pack(expand=True, fill="both", padx=20, pady=20)

        documentation = """
        Singly Linked List Operations Documentation

        1. Insert at Beginning: O(1)
           - Adds a new node at the start of the list.

        2. Insert at End: O(n)
           - Traverses to the end of the list and adds a new node.

        3. Insert at Position: O(n)
           - Traverses to the specified position and inserts a new node.

        4. Delete at Beginning: O(1)
           - Removes the first node of the list.

        5. Delete at End: O(n)
           - Traverses to the end of the list and removes the last node.

        6. Delete at Position: O(n)
           - Traverses to the specified position and removes the node.

        7. Traverse: O(n)
           - Visits each node in the list sequentially.

        8. Search: O(n)
           - Looks for a specific value in the list.

        Visualization Guide:
        - Blue circles: Nodes in the list
        - Arrows: Links between nodes
        - Yellow highlight: Current node being operated on

        Use the speed slider to adjust the visualization speed.
        Use the Step-by-Step mode to go through the operations one step at a time.
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
        1. what is a singly linked list
        
        A singly linked list is a linear data structure where each element (node) contains data and a reference (link) to the next node in the sequence. The last node typically points to null, indicating the end of the list.",
        
        2. what are the advantages of singly linked lists
        
        Advantages include dynamic size, efficient insertion and deletion at the beginning, and memory efficiency as it doesn't require contiguous memory allocation.",
        
        3. what are the disadvantages of singly linked lists
        
        Disadvantages include slower access time for arbitrary elements (as you need to traverse from the beginning), more memory usage per element due to storing the 'next' reference, and the inability to traverse backwards.",
        
        4. how does insertion work in a singly linked list
        
        Insertion in a singly linked list involves creating a new node, adjusting the 'next' reference of the previous node to point to the new node, and setting the new node's 'next' reference to point to the subsequent node.",
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
    """Wrapper function to create the Singly Linked List visualization page."""
    SinglyLinkedListVisualization(root, prev_page)


# If you want to run this file standalone for testing
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Singly Linked List Visualization")
    root.geometry("800x600")
    SinglyLinkedListVisualization(root, None)
    root.mainloop()
