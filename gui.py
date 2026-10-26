"""
StudyMate - Polished Speech Bubble GUI Interface (Tkinter)
CodeAlpha Internship Project

This module implements the modern speech-bubble Graphical User Interface (GUI) for StudyMate.
Layout uses a fixed-grid geometry so the bottom input area is ALWAYS visible:
- Row 0: Header with title, subtitle, and Clear Chat button (weight=0)
- Row 1: Scrollable Canvas with speech bubble cards (weight=1)
- Row 2: Fixed bottom input bar with placeholder and Send button (weight=0)
"""

import tkinter as tk
from tkinter import ttk
from datetime import datetime
import chatbot


class StudyMateGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("StudyMate – Student Assistant Chatbot")
        self.root.geometry("700x720")
        self.root.minsize(500, 550)
        self.root.configure(bg="#EEF2F7")
        self.user_name = None

        # Placeholder state
        self.placeholder = "Type your message..."
        self.entry_has_placeholder = True

        # Configure root grid geometry to guarantee fixed bottom bar
        self.root.grid_rowconfigure(0, weight=0)  # Header fixed
        self.root.grid_rowconfigure(1, weight=1)  # Chat area expands
        self.root.grid_rowconfigure(2, weight=0)  # Input bar fixed
        self.root.grid_columnconfigure(0, weight=1)

        # Apply modern TTK theme
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Build GUI Components
        self.create_header()
        self.create_chat_area()
        self.create_input_area()

        # Display initial welcome message as a StudyMate bubble
        self.display_welcome_message()

    def create_header(self):
        """Creates the header banner at Row 0 with title, subtitle, and clear chat button."""
        header = tk.Frame(self.root, bg="#172033", height=78)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_propagate(False)

        title_box = tk.Frame(header, bg="#172033")
        title_box.pack(side="left", fill="both", expand=True, padx=20, pady=10)

        tk.Label(
            title_box, text="StudyMate 🤖",
            font=("Segoe UI", 18, "bold"),
            fg="white", bg="#172033"
        ).pack(anchor="w")

        tk.Label(
            title_box, text="Student Assistant Chatbot",
            font=("Segoe UI", 9, "italic"),
            fg="#AAB6C8", bg="#172033"
        ).pack(anchor="w")

        self.clear_button = tk.Button(
            header, text="Clear Chat", command=self.clear_chat,
            font=("Segoe UI", 9, "bold"), bg="#2D3A50", fg="white",
            activebackground="#40506A", activeforeground="white",
            relief="flat", bd=0, padx=14, pady=7, cursor="hand2"
        )
        self.clear_button.pack(side="right", padx=18)
        self.clear_btn = self.clear_button

        # Hover effect
        self.clear_button.bind("<Enter>", lambda e: self.clear_button.config(bg="#40506A"))
        self.clear_button.bind("<Leave>", lambda e: self.clear_button.config(bg="#2D3A50"))

    def create_chat_area(self):
        """Creates the scrollable conversation area at Row 1 between header and input."""
        outer = tk.Frame(self.root, bg="#EEF2F7")
        outer.grid(row=1, column=0, sticky="nsew", padx=10, pady=(10, 0))

        self.canvas = tk.Canvas(outer, bg="#EEF2F7", highlightthickness=0, bd=0)
        scrollbar = ttk.Scrollbar(outer, orient="vertical", command=self.canvas.yview)

        self.messages_frame = tk.Frame(self.canvas, bg="#EEF2F7")
        self.window_id = self.canvas.create_window((0, 0), window=self.messages_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.messages_frame.bind(
            "<Configure>",
            lambda event: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.bind("<Configure>", self.resize_message_area)
        self.canvas.bind_all("<MouseWheel>", self.mouse_wheel)

    def resize_message_area(self, event):
        """Resizes the inner frame width and adjusts label wraplength on window resize."""
        self.canvas.itemconfigure(self.window_id, width=event.width)
        new_wrap = max(260, min(520, event.width - 150))
        for row in self.messages_frame.winfo_children():
            for bubble in row.winfo_children():
                for child in bubble.winfo_children():
                    if isinstance(child, tk.Label) and child.cget("wraplength") > 0:
                        child.config(wraplength=new_wrap)

    def mouse_wheel(self, event):
        """Scrolls canvas on mousewheel."""
        if self.canvas.winfo_exists():
            self.canvas.yview_scroll(int(-event.delta / 120), "units")

    def create_input_area(self):
        """Creates the fixed bottom input bar at Row 2 containing entry box and send button."""
        bottom = tk.Frame(
            self.root, bg="white", padx=14, pady=12,
            highlightthickness=1, highlightbackground="#D6DEE9"
        )
        bottom.grid(row=2, column=0, sticky="ew")

        # Entry container frame with border
        entry_frame = tk.Frame(
            bottom, bg="#F3F6FA",
            highlightthickness=1, highlightbackground="#CBD5E1"
        )
        entry_frame.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.entry = tk.Entry(
            entry_frame, font=("Segoe UI", 11),
            bg="#F3F6FA", fg="#94A3B8",
            insertbackground="#172033", relief="flat", bd=0
        )
        self.entry.pack(fill="x", padx=12, pady=10)
        self.entry_box = self.entry

        # Set placeholder text
        self.entry.insert(0, self.placeholder)
        self.entry.bind("<FocusIn>", self._on_entry_focus_in)
        self.entry.bind("<FocusOut>", self._on_entry_focus_out)
        self.entry.bind("<Return>", self.send_message)

        # Send Button
        self.send_button = tk.Button(
            bottom, text="Send ➤", command=self.send_message,
            font=("Segoe UI", 10, "bold"),
            bg="#2563EB", fg="white",
            activebackground="#1D4ED8", activeforeground="white",
            relief="flat", bd=0, padx=18, pady=9, cursor="hand2"
        )
        self.send_button.pack(side="right")
        self.send_btn = self.send_button

        # Hover effects on Send button
        self.send_button.bind("<Enter>", lambda e: self.send_button.config(bg="#1D4ED8"))
        self.send_button.bind("<Leave>", lambda e: self.send_button.config(bg="#2563EB"))

    def _on_entry_focus_in(self, event=None):
        """Clears placeholder when user focuses into entry box."""
        if self.entry_has_placeholder:
            self.entry.delete(0, tk.END)
            self.entry.config(fg="#172033")
            self.entry_has_placeholder = False

    def _on_entry_focus_out(self, event=None):
        """Restores placeholder if entry box is left empty."""
        if not self.entry.get().strip():
            self.entry.delete(0, tk.END)
            self.entry.insert(0, self.placeholder)
            self.entry.config(fg="#94A3B8")
            self.entry_has_placeholder = True

    def display_welcome_message(self):
        """Displays initial StudyMate greeting bubble."""
        self.display_bot_message(
            "Hello! 👋 I'm StudyMate, your student assistant.\n"
            "Ask me about Python, DBMS, HTML, CSS, Git, GitHub or programming."
        )

    def display_user_message(self, message):
        """Formats and displays user message bubble on the right."""
        timestamp = datetime.now().strftime("%I:%M %p").lstrip("0")
        self.add_bubble("You 👤", message, timestamp, user=True)

    def display_bot_message(self, message):
        """Formats and displays bot message card on the left."""
        timestamp = datetime.now().strftime("%I:%M %p").lstrip("0")
        self.add_bubble("🤖 StudyMate", message, timestamp, user=False)

    def add_bubble(self, sender, message, timestamp, user=False):
        """Creates a visually separated speech bubble card."""
        row = tk.Frame(self.messages_frame, bg="#EEF2F7")
        row.pack(fill="x", pady=6, padx=8)

        canvas_w = self.canvas.winfo_width()
        bubble_width = max(260, min(520, canvas_w - 150)) if canvas_w > 200 else 420

        if user:
            # User bubble on the RIGHT (Blue card)
            bubble = tk.Frame(row, bg="#2563EB", padx=14, pady=10)
            bubble.pack(side="right", anchor="e")

            tk.Label(
                bubble, text=sender, font=("Segoe UI", 9, "bold"),
                fg="#DCE8FF", bg="#2563EB"
            ).pack(anchor="e")

            tk.Label(
                bubble, text=message, font=("Segoe UI", 10),
                fg="white", bg="#2563EB", justify="left",
                wraplength=bubble_width
            ).pack(anchor="e", pady=(4, 4))

            tk.Label(
                bubble, text=timestamp, font=("Segoe UI", 8),
                fg="#C5D8FF", bg="#2563EB"
            ).pack(anchor="e")
        else:
            # Bot bubble on the LEFT (White card with slate border)
            bubble = tk.Frame(
                row, bg="white", padx=14, pady=10,
                highlightthickness=1, highlightbackground="#CBD5E1"
            )
            bubble.pack(side="left", anchor="w")

            tk.Label(
                bubble, text=sender, font=("Segoe UI", 9, "bold"),
                fg="#0F766E", bg="white"
            ).pack(anchor="w")

            tk.Label(
                bubble, text=message, font=("Segoe UI", 10),
                fg="#172033", bg="white", justify="left",
                wraplength=bubble_width
            ).pack(anchor="w", pady=(4, 4))

            tk.Label(
                bubble, text=timestamp, font=("Segoe UI", 8),
                fg="#718096", bg="white"
            ).pack(anchor="e")

        self.root.update_idletasks()
        self.canvas.yview_moveto(1.0)

    # Alias method for backward compatibility
    def add_message_bubble(self, sender, message, timestamp, is_user=False):
        self.add_bubble(sender, message, timestamp, user=is_user)

    def send_message(self, event=None):
        """Processes sending the message from the entry box to chatbot.py."""
        current_text = self.entry.get()
        if self.entry_has_placeholder and current_text == self.placeholder:
            raw_input = ""
        else:
            raw_input = current_text
            self.entry_has_placeholder = False

        user_input = raw_input.strip().lower()

        if not user_input:
            self.entry.delete(0, tk.END)
            self._on_entry_focus_out()
            self.display_bot_message("Please enter a message or question!")
            return "break"

        self.entry.delete(0, tk.END)
        self.display_user_message(raw_input)

        bot_response, self.user_name = chatbot.get_response(
            user_input, raw_input, self.user_name
        )

        display_response = bot_response
        if display_response.startswith("StudyMate: "):
            display_response = display_response[len("StudyMate: "):]

        self.display_bot_message(display_response)
        chatbot.save_chat_history(raw_input, bot_response)

        # If entry is not currently focused, restore placeholder
        if self.root.focus_get() != self.entry:
            self._on_entry_focus_out()

        return "break"

    def clear_chat(self):
        """Clears visible message bubbles and restores welcome bubble."""
        for widget in self.messages_frame.winfo_children():
            widget.destroy()
        self.display_welcome_message()


def create_gui():
    """Instantiates and starts the Tkinter mainloop for StudyMate."""
    root = tk.Tk()
    StudyMateGUI(root)
    root.mainloop()


if __name__ == "__main__":
    create_gui()
