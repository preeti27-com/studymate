"""
StudyMate — Academic Learning Workspace
CodeAlpha Internship Project

This module implements the professional Split Workspace Graphical User Interface (GUI)
using standard Tkinter widgets:
- Left Section: Dark navy navigation sidebar, branding, and topic navigation.
- Center Section: "Your Learning Desk" dashboard with 4 topic cards and Quick Actions.
- Right Section: Dedicated Question-and-Answer workspace with message cards and fixed input.
"""

import tkinter as tk
from tkinter import ttk
from datetime import datetime
import chatbot


# ==============================================================================
# DESIGN SYSTEM & COLOR PALETTE
# ==============================================================================
SIDEBAR_BG = "#15243A"
SIDEBAR_SELECTED = "#29466B"
SIDEBAR_HOVER = "#1E3352"
SIDEBAR_ACCENT = "#4B77BE"
SIDEBAR_TEXT = "#FFFFFF"
SIDEBAR_MUTED = "#8FA0B8"
SIDEBAR_BORDER = "#1E3352"

MAIN_BG = "#F4F6FA"
CARD_BG = "#FFFFFF"
CARD_BORDER = "#DFE5ED"
TEXT_PRIMARY = "#1E293B"
TEXT_SECONDARY = "#64748B"

BTN_PRIMARY = "#294E80"
BTN_HOVER = "#213F69"
BTN_TEXT = "#FFFFFF"

USER_MSG_BG = "#E7EDF5"
BOT_MSG_BG = "#FFFFFF"

FONT_FAMILY = "Segoe UI"


class StudyMateGUI:
    """
    Main Tkinter Split Workspace application for StudyMate.
    """

    def __init__(self, root):
        self.root = root
        self.root.title("StudyMate — Academic Learning Workspace")
        self.root.geometry("1200x760")
        self.root.minsize(900, 600)
        self.root.configure(bg=MAIN_BG)

        self.user_name = None
        self.placeholder = "Type a question or math expression..."
        self.entry_has_placeholder = True
        self.nav_buttons = {}
        self.current_nav = "Overview"

        # Apply ttk style
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Build Main Layout (Sidebar + Split Main Workspace)
        self.setup_layout()
        self.create_sidebar()
        self.create_dashboard()
        self.create_qa_workspace()

        # Display initial greeting in QA Workspace
        self.display_welcome_message()

    def setup_layout(self):
        """Configures root grid with fixed sidebar and resizable workspace."""
        self.root.grid_columnconfigure(0, weight=0, minsize=220)  # Left Sidebar
        self.root.grid_columnconfigure(1, weight=1)               # Center Dashboard
        self.root.grid_columnconfigure(2, weight=1)               # Right QA Workspace
        self.root.grid_rowconfigure(0, weight=1)

    # ==========================================================================
    # REGION 1: LEFT SIDEBAR
    # ==========================================================================
    def create_sidebar(self):
        """Creates the dark navy sidebar with branding and navigation controls."""
        self.sidebar = tk.Frame(self.root, bg=SIDEBAR_BG, width=220)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)

        # Branding Header
        brand_frame = tk.Frame(self.sidebar, bg=SIDEBAR_BG, padx=20, pady=24)
        brand_frame.pack(fill="x")

        tk.Label(
            brand_frame, text="StudyMate",
            font=(FONT_FAMILY, 16, "bold"),
            fg=SIDEBAR_TEXT, bg=SIDEBAR_BG
        ).pack(anchor="w")

        tk.Label(
            brand_frame, text="Student Learning Workspace",
            font=(FONT_FAMILY, 9),
            fg=SIDEBAR_MUTED, bg=SIDEBAR_BG
        ).pack(anchor="w", pady=(3, 0))

        # Thin divider line
        divider = tk.Frame(self.sidebar, bg=SIDEBAR_BORDER, height=1)
        divider.pack(fill="x", padx=16, pady=(0, 16))

        # Navigation Menu
        nav_container = tk.Frame(self.sidebar, bg=SIDEBAR_BG)
        nav_container.pack(fill="x", padx=10)

        nav_items = [
            ("Overview", self.nav_overview),
            ("Ask a Question", self.nav_ask_question),
            ("Study Topics", self.nav_study_topics),
            ("Calculator", self.nav_calculator),
            ("Date & Time", self.nav_date_time)
        ]

        for name, command in nav_items:
            btn_frame = tk.Frame(nav_container, bg=SIDEBAR_BG, height=38)
            btn_frame.pack(fill="x", pady=2)
            btn_frame.pack_propagate(False)

            # Left accent indicator strip
            indicator = tk.Frame(btn_frame, bg=SIDEBAR_BG, width=3)
            indicator.pack(side="left", fill="y")

            btn = tk.Button(
                btn_frame, text=name, anchor="w",
                font=(FONT_FAMILY, 9, "normal"),
                fg=SIDEBAR_MUTED, bg=SIDEBAR_BG,
                activebackground=SIDEBAR_SELECTED, activeforeground=SIDEBAR_TEXT,
                relief="flat", bd=0, padx=12, cursor="hand2",
                command=command
            )
            btn.pack(side="left", fill="both", expand=True)

            # Store references for state management
            self.nav_buttons[name] = {"frame": btn_frame, "indicator": indicator, "button": btn}

            # Hover events (only applied if not currently selected)
            btn.bind("<Enter>", lambda e, n=name: self._on_nav_hover(n))
            btn.bind("<Leave>", lambda e, n=name: self._on_nav_leave(n))

        # Set default active item
        self.set_active_nav("Overview")

    def set_active_nav(self, nav_name):
        """Highlights the selected navigation item with accent indicator."""
        self.current_nav = nav_name
        for name, refs in self.nav_buttons.items():
            if name == nav_name:
                refs["frame"].configure(bg=SIDEBAR_SELECTED)
                refs["indicator"].configure(bg=SIDEBAR_ACCENT)
                refs["button"].configure(
                    bg=SIDEBAR_SELECTED, fg=SIDEBAR_TEXT, font=(FONT_FAMILY, 9, "bold")
                )
            else:
                refs["frame"].configure(bg=SIDEBAR_BG)
                refs["indicator"].configure(bg=SIDEBAR_BG)
                refs["button"].configure(
                    bg=SIDEBAR_BG, fg=SIDEBAR_MUTED, font=(FONT_FAMILY, 9, "normal")
                )

    def _on_nav_hover(self, name):
        if name != self.current_nav:
            self.nav_buttons[name]["frame"].configure(bg=SIDEBAR_HOVER)
            self.nav_buttons[name]["button"].configure(bg=SIDEBAR_HOVER, fg=SIDEBAR_TEXT)

    def _on_nav_leave(self, name):
        if name != self.current_nav:
            self.nav_buttons[name]["frame"].configure(bg=SIDEBAR_BG)
            self.nav_buttons[name]["button"].configure(bg=SIDEBAR_BG, fg=SIDEBAR_MUTED)

    # Navigation Actions
    def nav_overview(self):
        self.set_active_nav("Overview")
        self.display_bot_message(
            "Overview: You are viewing your Learning Desk. Explore topics on the left or type any question on the right."
        )

    def nav_ask_question(self):
        self.set_active_nav("Ask a Question")
        self.entry.focus_set()
        self._on_entry_focus_in()

    def nav_study_topics(self):
        self.set_active_nav("Study Topics")
        self.send_query_directly("help")

    def nav_calculator(self):
        self.set_active_nav("Calculator")
        if self.entry_has_placeholder:
            self._on_entry_focus_in()
        self.entry.delete(0, tk.END)
        self.entry.insert(0, "calculate 25 + 30")
        self.entry.focus_set()
        self.display_bot_message(
            "Calculator ready: You can evaluate expressions like 'calculate 25 + 30', '45 * 12', or '100 / 4'."
        )

    def nav_date_time(self):
        self.set_active_nav("Date & Time")
        self.send_query_directly("What is today's date?")
        self.send_query_directly("What is the time?")

    # ==========================================================================
    # REGION 2: CENTER LEARNING DASHBOARD
    # ==========================================================================
    def create_dashboard(self):
        """Creates the 'Your Learning Desk' dashboard with 4 topic cards and quick actions."""
        self.dashboard_frame = tk.Frame(self.root, bg=MAIN_BG, padx=24, pady=24)
        self.dashboard_frame.grid(row=0, column=1, sticky="nsew")

        # Heading Section
        tk.Label(
            self.dashboard_frame, text="Your Learning Desk",
            font=(FONT_FAMILY, 16, "bold"),
            fg=TEXT_PRIMARY, bg=MAIN_BG
        ).pack(anchor="w")

        tk.Label(
            self.dashboard_frame,
            text="Explore programming concepts and practise fundamental computer science skills.",
            font=(FONT_FAMILY, 9),
            fg=TEXT_SECONDARY, bg=MAIN_BG
        ).pack(anchor="w", pady=(4, 20))

        # 4 Topic Cards in a 2x2 Grid
        cards_container = tk.Frame(self.dashboard_frame, bg=MAIN_BG)
        cards_container.pack(fill="x", pady=(0, 24))
        cards_container.grid_columnconfigure(0, weight=1)
        cards_container.grid_columnconfigure(1, weight=1)

        topic_data = [
            (
                "Python",
                "Programming fundamentals and syntax.",
                "What is Python?",
                0, 0
            ),
            (
                "Database Systems",
                "DBMS, SQL, databases and keys.",
                "What is DBMS?",
                0, 1
            ),
            (
                "Web Development",
                "HTML and CSS fundamentals.",
                "What is HTML?",
                1, 0
            ),
            (
                "Version Control",
                "Git, GitHub and repositories.",
                "What is Git?",
                1, 1
            )
        ]

        for title, desc, sample_q, r, c in topic_data:
            self._create_topic_card(cards_container, title, desc, sample_q, r, c)

        # Quick Actions Section
        tk.Label(
            self.dashboard_frame, text="Quick Actions",
            font=(FONT_FAMILY, 12, "bold"),
            fg=TEXT_PRIMARY, bg=MAIN_BG
        ).pack(anchor="w", pady=(0, 8))

        actions_box = tk.Frame(
            self.dashboard_frame, bg=CARD_BG,
            highlightthickness=1, highlightbackground=CARD_BORDER,
            padx=16, pady=14
        )
        actions_box.pack(fill="x")

        actions = [
            ("Open Calculator", lambda: self.nav_calculator()),
            ("Check Date & Time", lambda: self.nav_date_time()),
            ("Browse Topics", lambda: self.nav_study_topics())
        ]

        for label, cmd in actions:
            btn = tk.Button(
                actions_box, text=label, command=cmd,
                font=(FONT_FAMILY, 9, "bold"),
                bg=MAIN_BG, fg=TEXT_PRIMARY,
                activebackground=CARD_BORDER, activeforeground=TEXT_PRIMARY,
                relief="flat", bd=1, highlightthickness=1,
                highlightbackground=CARD_BORDER, padx=12, pady=7,
                cursor="hand2"
            )
            btn.pack(side="left", padx=(0, 8))
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=CARD_BORDER))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=MAIN_BG))

    def _create_topic_card(self, parent, title, desc, sample_question, row, col):
        """Creates an individual white card for a learning topic."""
        card = tk.Frame(
            parent, bg=CARD_BG,
            highlightthickness=1, highlightbackground=CARD_BORDER,
            padx=16, pady=16
        )
        card.grid(row=row, column=col, padx=6, pady=6, sticky="nsew")

        tk.Label(
            card, text=title,
            font=(FONT_FAMILY, 11, "bold"),
            fg=TEXT_PRIMARY, bg=CARD_BG
        ).pack(anchor="w")

        tk.Label(
            card, text=desc,
            font=(FONT_FAMILY, 9),
            fg=TEXT_SECONDARY, bg=CARD_BG,
            wraplength=180, justify="left"
        ).pack(anchor="w", pady=(6, 14))

        btn = tk.Button(
            card, text="Explore Topic",
            font=(FONT_FAMILY, 9, "bold"),
            bg=BTN_PRIMARY, fg=BTN_TEXT,
            activebackground=BTN_HOVER, activeforeground=BTN_TEXT,
            relief="flat", bd=0, padx=12, pady=6, cursor="hand2",
            command=lambda q=sample_question: self.send_query_directly(q)
        )
        btn.pack(anchor="w")
        btn.bind("<Enter>", lambda e, b=btn: b.config(bg=BTN_HOVER))
        btn.bind("<Leave>", lambda e, b=btn: b.config(bg=BTN_PRIMARY))

    # ==========================================================================
    # REGION 3: RIGHT QUESTION-AND-ANSWER WORKSPACE
    # ==========================================================================
    def create_qa_workspace(self):
        """Creates the right side QA workspace with scrollable card stream and fixed input."""
        self.qa_frame = tk.Frame(
            self.root, bg=MAIN_BG, padx=16, pady=16,
            highlightthickness=1, highlightbackground=CARD_BORDER
        )
        self.qa_frame.grid(row=0, column=2, sticky="nsew", padx=(0, 12), pady=12)

        self.qa_frame.grid_rowconfigure(0, weight=0)  # Header
        self.qa_frame.grid_rowconfigure(1, weight=1)  # Scrollable Conversation
        self.qa_frame.grid_rowconfigure(2, weight=0)  # Fixed Bottom Input
        self.qa_frame.grid_columnconfigure(0, weight=1)

        # QA Header
        header = tk.Frame(self.qa_frame, bg=MAIN_BG)
        header.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        tk.Label(
            header, text="Ask a Question",
            font=(FONT_FAMILY, 15, "bold"),
            fg=TEXT_PRIMARY, bg=MAIN_BG
        ).pack(anchor="w")

        tk.Label(
            header, text="Enter a question about a supported programming topic.",
            font=(FONT_FAMILY, 9),
            fg=TEXT_SECONDARY, bg=MAIN_BG
        ).pack(anchor="w")

        # Scrollable Conversation Area
        conv_container = tk.Frame(self.qa_frame, bg=MAIN_BG)
        conv_container.grid(row=1, column=0, sticky="nsew", pady=(0, 10))

        self.canvas = tk.Canvas(conv_container, bg=MAIN_BG, highlightthickness=0, bd=0)
        self.scrollbar = ttk.Scrollbar(conv_container, orient="vertical", command=self.canvas.yview)

        self.messages_frame = tk.Frame(self.canvas, bg=MAIN_BG)
        self.window_id = self.canvas.create_window((0, 0), window=self.messages_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.messages_frame.bind(
            "<Configure>",
            lambda event: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.bind("<Configure>", self.resize_message_area)
        self.canvas.bind_all("<MouseWheel>", self.mouse_wheel)

        # Fixed Bottom Input Area
        self.create_qa_input_area()

    def resize_message_area(self, event):
        """Dynamically adjusts message inner frame and text wraplength on window resize."""
        self.canvas.itemconfigure(self.window_id, width=event.width)
        calc_wrap = max(220, event.width - 90)
        for row in self.messages_frame.winfo_children():
            for card in row.winfo_children():
                for child in card.winfo_children():
                    if isinstance(child, tk.Label) and child.cget("wraplength") > 0:
                        child.config(wraplength=calc_wrap)

    def mouse_wheel(self, event):
        """Scrolls canvas on mouse wheel action."""
        if self.canvas.winfo_exists():
            self.canvas.yview_scroll(int(-event.delta / 120), "units")

    def create_qa_input_area(self):
        """Creates the bottom input bar with Send and Clear controls."""
        bottom = tk.Frame(
            self.qa_frame, bg=CARD_BG,
            highlightthickness=1, highlightbackground=CARD_BORDER,
            padx=10, pady=10
        )
        bottom.grid(row=2, column=0, sticky="ew")

        # Entry container
        entry_frame = tk.Frame(
            bottom, bg=MAIN_BG,
            highlightthickness=1, highlightbackground=CARD_BORDER
        )
        entry_frame.pack(side="left", fill="x", expand=True, padx=(0, 8))

        self.entry = tk.Entry(
            entry_frame, font=(FONT_FAMILY, 10),
            bg=MAIN_BG, fg=TEXT_SECONDARY,
            insertbackground=TEXT_PRIMARY, relief="flat", bd=0
        )
        self.entry.pack(fill="x", padx=10, pady=8)
        self.entry_box = self.entry

        self.entry.insert(0, self.placeholder)
        self.entry.bind("<FocusIn>", self._on_entry_focus_in)
        self.entry.bind("<FocusOut>", self._on_entry_focus_out)
        self.entry.bind("<Return>", self.send_message)

        # Send Button
        self.send_button = tk.Button(
            bottom, text="Send", command=self.send_message,
            font=(FONT_FAMILY, 9, "bold"),
            bg=BTN_PRIMARY, fg=BTN_TEXT,
            activebackground=BTN_HOVER, activeforeground=BTN_TEXT,
            relief="flat", bd=0, padx=16, pady=7, cursor="hand2"
        )
        self.send_button.pack(side="left", padx=(0, 6))
        self.send_btn = self.send_button

        self.send_button.bind("<Enter>", lambda e: self.send_button.config(bg=BTN_HOVER))
        self.send_button.bind("<Leave>", lambda e: self.send_button.config(bg=BTN_PRIMARY))

        # Clear Button
        self.clear_button = tk.Button(
            bottom, text="Clear", command=self.clear_chat,
            font=(FONT_FAMILY, 9),
            bg=CARD_BG, fg=TEXT_SECONDARY,
            activebackground=MAIN_BG, activeforeground=TEXT_PRIMARY,
            relief="flat", bd=1, highlightthickness=1,
            highlightbackground=CARD_BORDER, padx=12, pady=6, cursor="hand2"
        )
        self.clear_button.pack(side="left")
        self.clear_btn = self.clear_button

        self.clear_button.bind("<Enter>", lambda e: self.clear_button.config(bg=MAIN_BG))
        self.clear_button.bind("<Leave>", lambda e: self.clear_button.config(bg=CARD_BG))

    def _on_entry_focus_in(self, event=None):
        if self.entry_has_placeholder:
            self.entry.delete(0, tk.END)
            self.entry.config(fg=TEXT_PRIMARY)
            self.entry_has_placeholder = False

    def _on_entry_focus_out(self, event=None):
        if not self.entry.get().strip():
            self.entry.delete(0, tk.END)
            self.entry.insert(0, self.placeholder)
            self.entry.config(fg=TEXT_SECONDARY)
            self.entry_has_placeholder = True

    # ==========================================================================
    # MESSAGE RENDERING & PROCESSING
    # ==========================================================================
    def display_welcome_message(self):
        """Displays initial StudyMate greeting card."""
        self.display_bot_message(
            "Welcome to StudyMate. You can ask questions about Python, DBMS, HTML, CSS, "
            "Git, date, time, or perform basic arithmetic. Select a topic from your "
            "Learning Desk or enter a question below to begin."
        )

    def display_user_message(self, message):
        """Displays user message aligned right in a muted blue-grey card."""
        timestamp = datetime.now().strftime("%I:%M %p").lstrip("0")
        self.add_message_card("You", message, timestamp, is_user=True)

    def display_bot_message(self, message):
        """Displays StudyMate assistant message aligned left in a white card."""
        timestamp = datetime.now().strftime("%I:%M %p").lstrip("0")
        self.add_message_card("StudyMate", message, timestamp, is_user=False)

    def add_message_card(self, sender, message, timestamp, is_user=False):
        """Renders an individual rectangular message card with clean borders."""
        row = tk.Frame(self.messages_frame, bg=MAIN_BG)
        row.pack(fill="x", pady=4, padx=6)

        canvas_w = self.canvas.winfo_width()
        wrap_width = max(220, canvas_w - 90) if canvas_w > 150 else 340

        if is_user:
            # User Question Card (Align Right, Muted Blue-Grey)
            card = tk.Frame(
                row, bg=USER_MSG_BG,
                highlightthickness=1, highlightbackground=CARD_BORDER,
                padx=14, pady=10
            )
            card.pack(side="right", anchor="e")

            # Sender and Time Header
            hdr = tk.Frame(card, bg=USER_MSG_BG)
            hdr.pack(anchor="e", fill="x")

            tk.Label(
                hdr, text=sender,
                font=(FONT_FAMILY, 9, "bold"),
                fg=TEXT_PRIMARY, bg=USER_MSG_BG
            ).pack(side="left")

            tk.Label(
                hdr, text=f" • {timestamp}",
                font=(FONT_FAMILY, 8),
                fg=TEXT_SECONDARY, bg=USER_MSG_BG
            ).pack(side="left")

            # Message Text
            tk.Label(
                card, text=message,
                font=(FONT_FAMILY, 9),
                fg=TEXT_PRIMARY, bg=USER_MSG_BG,
                justify="left", wraplength=wrap_width
            ).pack(anchor="w", pady=(4, 0))
        else:
            # Assistant Response Card (Align Left, White)
            card = tk.Frame(
                row, bg=BOT_MSG_BG,
                highlightthickness=1, highlightbackground=CARD_BORDER,
                padx=14, pady=10
            )
            card.pack(side="left", anchor="w")

            # Sender and Time Header
            hdr = tk.Frame(card, bg=BOT_MSG_BG)
            hdr.pack(anchor="w", fill="x")

            tk.Label(
                hdr, text=sender,
                font=(FONT_FAMILY, 9, "bold"),
                fg=BTN_PRIMARY, bg=BOT_MSG_BG
            ).pack(side="left")

            tk.Label(
                hdr, text=f" • {timestamp}",
                font=(FONT_FAMILY, 8),
                fg=TEXT_SECONDARY, bg=BOT_MSG_BG
            ).pack(side="left")

            # Message Text
            tk.Label(
                card, text=message,
                font=(FONT_FAMILY, 9),
                fg=TEXT_PRIMARY, bg=BOT_MSG_BG,
                justify="left", wraplength=wrap_width
            ).pack(anchor="w", pady=(4, 0))

        self.root.update_idletasks()
        self.canvas.yview_moveto(1.0)

    # Alias for backward compatibility
    def add_message_bubble(self, sender, message, timestamp, is_user=False):
        self.add_message_card(sender, message, timestamp, is_user=is_user)

    def send_query_directly(self, raw_input):
        """Directly executes a query into the QA workspace."""
        user_input = raw_input.strip().lower()
        if not user_input:
            return

        self.display_user_message(raw_input)

        bot_response, self.user_name = chatbot.get_response(
            user_input, raw_input, self.user_name
        )

        display_response = bot_response
        if display_response.startswith("StudyMate: "):
            display_response = display_response[len("StudyMate: "):]

        self.display_bot_message(display_response)
        chatbot.save_chat_history(raw_input, bot_response)

    def send_message(self, event=None):
        """Processes user input from the bottom entry box."""
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
            self.display_bot_message("Please enter a question or topic.")
            return "break"

        self.entry.delete(0, tk.END)
        self.send_query_directly(raw_input)

        if self.root.focus_get() != self.entry:
            self._on_entry_focus_out()

        return "break"

    def clear_chat(self):
        """Clears visible message cards and restores welcome card."""
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
