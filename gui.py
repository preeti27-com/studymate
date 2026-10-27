"""
StudyMate — Academic Learning Workspace
CodeAlpha Internship Project

This module implements the polished, professional academic desktop interface for StudyMate:
- Left Navigation Sidebar: Fixed dark navy sidebar (#15243A) with subtle indicator on active item (#29466B).
- Main Learning Dashboard: Interactive workspace supporting "Your Learning Desk", "Study Topics",
  "Calculator", "Date & Time", and "Ask a Question" guidance.
- Right Question-and-Answer Workspace: Dedicated message cards (assistant white, user muted blue-grey)
  with vertical scrolling and a permanently visible bottom input bar with Send and Clear controls.
"""

import tkinter as tk
from tkinter import ttk
from datetime import datetime
import chatbot


# ==============================================================================
# PROFESSIONAL ACADEMIC COLOR PALETTE (Strict adherence to design specifications)
# ==============================================================================
SIDEBAR_BG = "#15243A"
SIDEBAR_SELECTED = "#29466B"
SIDEBAR_HOVER = "#1E3352"
SIDEBAR_INDICATOR = "#294E80"
SIDEBAR_TEXT = "#FFFFFF"
SIDEBAR_MUTED = "#8FA0B8"
SIDEBAR_BORDER = "#1E3352"

MAIN_BG = "#F4F6FA"
CARD_BG = "#FFFFFF"
CARD_BORDER = "#DFE5ED"
TEXT_PRIMARY = "#1E293B"
TEXT_SECONDARY = "#64748B"

PRIMARY_BUTTON = "#294E80"
BUTTON_HOVER = "#213F69"
BTN_TEXT = "#FFFFFF"

USER_MSG_BG = "#E7EDF5"
BOT_MSG_BG = "#FFFFFF"

FONT_FAMILY = "Segoe UI"


class StudyMateGUI:
    """
    Main Academic Desktop Application for StudyMate.
    Provides structured learning resources, topic exploration, working calculator,
    live date & time, and an integrated question-and-answer workspace.
    """

    def __init__(self, root):
        self.root = root
        self.root.title("StudyMate — Student Learning Workspace")
        self.root.geometry("1200x760")
        self.root.minsize(900, 600)
        self.root.configure(bg=MAIN_BG)

        self.user_name = None
        self.placeholder = "Type your question here..."
        self.entry_has_placeholder = True
        self.nav_buttons = {}
        self.current_nav = "Overview"

        # Calculator state variables
        self.calc_expr = ""
        self.calc_display_var = tk.StringVar(value="0")
        self.calc_status_var = tk.StringVar(value="Ready for calculation (+, -, *, /)")

        # Date & Time display variables
        self.date_var = tk.StringVar()
        self.time_var = tk.StringVar()

        # Apply clean TTK theme
        self.style = ttk.Style()
        try:
            self.style.theme_use("clam")
        except Exception:
            pass

        # Configure root layout
        self.setup_layout()

        # Build application regions
        self.create_sidebar()
        self.create_center_workspace()
        self.create_qa_workspace()

        # Display initial welcome card and default view
        self.show_view("Overview")
        self.display_welcome_message()

    def setup_layout(self):
        """Configures root grid layout with fixed sidebar and resizable workspaces."""
        self.root.grid_columnconfigure(0, weight=0, minsize=220)  # Left Sidebar
        self.root.grid_columnconfigure(1, weight=1, minsize=320)  # Main Learning Dashboard
        self.root.grid_columnconfigure(2, weight=1, minsize=340)  # Right Q&A Workspace
        self.root.grid_rowconfigure(0, weight=1)

    # ==========================================================================
    # REGION 1: LEFT NAVIGATION SIDEBAR
    # ==========================================================================
    def create_sidebar(self):
        """Creates the dark navy sidebar with application branding and text navigation."""
        self.sidebar = tk.Frame(self.root, bg=SIDEBAR_BG, width=220)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)

        # Application Branding Header
        brand_frame = tk.Frame(self.sidebar, bg=SIDEBAR_BG, padx=20, pady=24)
        brand_frame.pack(fill="x")

        tk.Label(
            brand_frame, text="StudyMate",
            font=(FONT_FAMILY, 18, "bold"),
            fg=SIDEBAR_TEXT, bg=SIDEBAR_BG
        ).pack(anchor="w")

        tk.Label(
            brand_frame, text="Student Learning Workspace",
            font=(FONT_FAMILY, 9),
            fg=SIDEBAR_MUTED, bg=SIDEBAR_BG
        ).pack(anchor="w", pady=(4, 0))

        # Subtle separator
        divider = tk.Frame(self.sidebar, bg=SIDEBAR_BORDER, height=1)
        divider.pack(fill="x", padx=16, pady=(0, 16))

        # Navigation Controls
        nav_container = tk.Frame(self.sidebar, bg=SIDEBAR_BG)
        nav_container.pack(fill="x", padx=10)

        nav_items = [
            ("Overview", lambda: self.show_view("Overview")),
            ("Ask a Question", lambda: self.show_view("Ask a Question")),
            ("Study Topics", lambda: self.show_view("Study Topics")),
            ("Calculator", lambda: self.show_view("Calculator")),
            ("Date & Time", lambda: self.show_view("Date & Time"))
        ]

        for name, command in nav_items:
            btn_frame = tk.Frame(nav_container, bg=SIDEBAR_BG, height=40)
            btn_frame.pack(fill="x", pady=2)
            btn_frame.pack_propagate(False)

            # Left indicator bar (active state indicator)
            indicator = tk.Frame(btn_frame, bg=SIDEBAR_BG, width=3)
            indicator.pack(side="left", fill="y")

            btn = tk.Button(
                btn_frame, text=name, anchor="w",
                font=(FONT_FAMILY, 10, "normal"),
                fg=SIDEBAR_MUTED, bg=SIDEBAR_BG,
                activebackground=SIDEBAR_SELECTED, activeforeground=SIDEBAR_TEXT,
                relief="flat", bd=0, padx=14, cursor="hand2",
                command=command
            )
            btn.pack(side="left", fill="both", expand=True)

            self.nav_buttons[name] = {"frame": btn_frame, "indicator": indicator, "button": btn}

            btn.bind("<Enter>", lambda e, n=name: self._on_nav_hover(n))
            btn.bind("<Leave>", lambda e, n=name: self._on_nav_leave(n))

    def set_active_nav(self, nav_name):
        """Updates sidebar highlight state to indicate active section."""
        self.current_nav = nav_name
        for name, refs in self.nav_buttons.items():
            if name == nav_name:
                refs["frame"].configure(bg=SIDEBAR_SELECTED)
                refs["indicator"].configure(bg=SIDEBAR_INDICATOR)
                refs["button"].configure(
                    bg=SIDEBAR_SELECTED, fg=SIDEBAR_TEXT, font=(FONT_FAMILY, 10, "bold")
                )
            else:
                refs["frame"].configure(bg=SIDEBAR_BG)
                refs["indicator"].configure(bg=SIDEBAR_BG)
                refs["button"].configure(
                    bg=SIDEBAR_BG, fg=SIDEBAR_MUTED, font=(FONT_FAMILY, 10, "normal")
                )

    def _on_nav_hover(self, name):
        if name != self.current_nav:
            self.nav_buttons[name]["frame"].configure(bg=SIDEBAR_HOVER)
            self.nav_buttons[name]["button"].configure(bg=SIDEBAR_HOVER, fg=SIDEBAR_TEXT)

    def _on_nav_leave(self, name):
        if name != self.current_nav:
            self.nav_buttons[name]["frame"].configure(bg=SIDEBAR_BG)
            self.nav_buttons[name]["button"].configure(bg=SIDEBAR_BG, fg=SIDEBAR_MUTED)

    # Legacy navigation handlers preserved for compatibility
    def nav_overview(self):
        self.show_view("Overview")

    def nav_ask_question(self):
        self.show_view("Ask a Question")

    def nav_study_topics(self):
        self.show_view("Study Topics")

    def nav_calculator(self):
        self.show_view("Calculator")

    def nav_date_time(self):
        self.show_view("Date & Time")

    # ==========================================================================
    # REGION 2: MAIN LEARNING DASHBOARD (DYNAMIC SCROLLABLE VIEWS)
    # ==========================================================================
    def create_center_workspace(self):
        """Creates the container frame with vertical scrolling for center study content."""
        self.center_container = tk.Frame(self.root, bg=MAIN_BG)
        self.center_container.grid(row=0, column=1, sticky="nsew", padx=12, pady=14)
        self.center_container.grid_rowconfigure(0, weight=1)
        self.center_container.grid_columnconfigure(0, weight=1)

        self.center_canvas = tk.Canvas(self.center_container, bg=MAIN_BG, highlightthickness=0, bd=0)
        self.center_scrollbar = ttk.Scrollbar(self.center_container, orient="vertical", command=self.center_canvas.yview)

        self.center_frame = tk.Frame(self.center_canvas, bg=MAIN_BG)
        self.center_window = self.center_canvas.create_window((0, 0), window=self.center_frame, anchor="nw")

        self.center_canvas.configure(yscrollcommand=self.center_scrollbar.set)
        self.center_canvas.grid(row=0, column=0, sticky="nsew")
        self.center_scrollbar.grid(row=0, column=1, sticky="ns")

        self.center_frame.bind(
            "<Configure>",
            lambda event: self.center_canvas.configure(scrollregion=self.center_canvas.bbox("all"))
        )
        self.center_canvas.bind(
            "<Configure>",
            lambda event: self.center_canvas.itemconfigure(self.center_window, width=event.width)
        )

        self.center_canvas.bind("<Enter>", lambda e: self._bind_mousewheel(self.center_canvas, self._on_mousewheel_center))
        self.center_canvas.bind("<Leave>", lambda e: self._unbind_mousewheel())

    def _bind_mousewheel(self, widget, handler):
        self.root.bind_all("<MouseWheel>", handler)

    def _unbind_mousewheel(self):
        self.root.unbind_all("<MouseWheel>")

    def _on_mousewheel_center(self, event):
        if self.center_canvas.winfo_exists():
            self.center_canvas.yview_scroll(int(-event.delta / 120), "units")

    def _on_mousewheel_qa(self, event):
        if self.canvas.winfo_exists():
            self.canvas.yview_scroll(int(-event.delta / 120), "units")

    def clear_center_workspace(self):
        """Clears existing widgets inside the center workspace and resets scroll."""
        for child in self.center_frame.winfo_children():
            child.destroy()
        self.center_canvas.yview_moveto(0.0)

    def show_view(self, view_name):
        """Switches the active view in the center learning workspace."""
        self.set_active_nav(view_name)
        self.clear_center_workspace()

        if view_name == "Overview":
            self._render_overview_view()
        elif view_name == "Ask a Question":
            self._render_ask_question_view()
            self._focus_input()
        elif view_name == "Study Topics":
            self._render_study_topics_view()
        elif view_name == "Calculator":
            self._render_calculator_view()
        elif view_name == "Date & Time":
            self._render_date_time_view()

    # --------------------------------------------------------------------------
    # View 1: Overview (Your Learning Desk)
    # --------------------------------------------------------------------------
    def _render_overview_view(self):
        """Renders the Learning Desk dashboard with 4 topic cards and quick actions."""
        tk.Label(
            self.center_frame, text="Your Learning Desk",
            font=(FONT_FAMILY, 20, "bold"),
            fg=TEXT_PRIMARY, bg=MAIN_BG
        ).pack(anchor="w", pady=(6, 0))

        tk.Label(
            self.center_frame,
            text="Explore programming concepts and practise fundamental computer science skills.",
            font=(FONT_FAMILY, 10),
            fg=TEXT_SECONDARY, bg=MAIN_BG
        ).pack(anchor="w", pady=(4, 18))

        # 4 Topic Cards Arranged in a Neat Two-Column Grid
        cards_grid = tk.Frame(self.center_frame, bg=MAIN_BG)
        cards_grid.pack(fill="x", pady=(0, 20))
        cards_grid.grid_columnconfigure(0, weight=1)
        cards_grid.grid_columnconfigure(1, weight=1)

        topics = [
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

        for title, desc, sample_q, r, c in topics:
            card = tk.Frame(
                cards_grid, bg=CARD_BG,
                highlightthickness=1, highlightbackground=CARD_BORDER,
                padx=16, pady=16
            )
            card.grid(row=r, column=c, padx=6, pady=6, sticky="nsew")

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
                bg=PRIMARY_BUTTON, fg=BTN_TEXT,
                activebackground=BUTTON_HOVER, activeforeground=BTN_TEXT,
                relief="flat", bd=0, padx=12, pady=6, cursor="hand2",
                command=lambda q=sample_q: self.send_query_directly(q)
            )
            btn.pack(anchor="w")
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=BUTTON_HOVER))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=PRIMARY_BUTTON))

        # Compact Quick Actions Section Below Cards
        tk.Label(
            self.center_frame, text="Quick Actions",
            font=(FONT_FAMILY, 13, "bold"),
            fg=TEXT_PRIMARY, bg=MAIN_BG
        ).pack(anchor="w", pady=(4, 8))

        actions_box = tk.Frame(
            self.center_frame, bg=CARD_BG,
            highlightthickness=1, highlightbackground=CARD_BORDER,
            padx=14, pady=12
        )
        actions_box.pack(fill="x")

        quick_buttons = [
            ("Open Calculator", lambda: self.show_view("Calculator")),
            ("Check Date & Time", lambda: self.show_view("Date & Time")),
            ("Browse Topics", lambda: self.show_view("Study Topics"))
        ]

        for label, cmd in quick_buttons:
            btn = tk.Button(
                actions_box, text=label, command=cmd,
                font=(FONT_FAMILY, 9, "bold"),
                bg=MAIN_BG, fg=TEXT_PRIMARY,
                activebackground=CARD_BORDER, activeforeground=TEXT_PRIMARY,
                relief="flat", bd=1, highlightthickness=1,
                highlightbackground=CARD_BORDER, padx=12, pady=6,
                cursor="hand2"
            )
            btn.pack(side="left", padx=(0, 8))
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=CARD_BORDER))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=MAIN_BG))

    # --------------------------------------------------------------------------
    # View 2: Ask a Question Guidance
    # --------------------------------------------------------------------------
    def _render_ask_question_view(self):
        """Displays helpful query tips and supported sample questions."""
        tk.Label(
            self.center_frame, text="Ask a Question",
            font=(FONT_FAMILY, 20, "bold"),
            fg=TEXT_PRIMARY, bg=MAIN_BG
        ).pack(anchor="w", pady=(6, 0))

        tk.Label(
            self.center_frame,
            text="Enter a question about a supported programming topic.",
            font=(FONT_FAMILY, 10),
            fg=TEXT_SECONDARY, bg=MAIN_BG
        ).pack(anchor="w", pady=(4, 18))

        info_card = tk.Frame(
            self.center_frame, bg=CARD_BG,
            highlightthickness=1, highlightbackground=CARD_BORDER,
            padx=16, pady=16
        )
        info_card.pack(fill="x", pady=(0, 16))

        tk.Label(
            info_card, text="Supported Topics & Capabilities",
            font=(FONT_FAMILY, 11, "bold"),
            fg=TEXT_PRIMARY, bg=CARD_BG
        ).pack(anchor="w")

        topics_text = (
            "• Python Programming (variables, loops, functions, lists)\n"
            "• Database Systems & SQL (relational tables, primary keys, normalization)\n"
            "• Web Development (HTML document markup, CSS visual styling)\n"
            "• Version Control (Git distributed tracking, GitHub repositories)\n"
            "• Safe Arithmetic (e.g., 25 + 30, 45 * 12, 144 / 12)\n"
            "• Live System Date and Time\n"
            "• Name Memory (e.g., 'My name is Alex', 'What is my name?')"
        )
        tk.Label(
            info_card, text=topics_text,
            font=(FONT_FAMILY, 9),
            fg=TEXT_SECONDARY, bg=CARD_BG, justify="left"
        ).pack(anchor="w", pady=(8, 0))

        # Sample Questions Box
        samples_card = tk.Frame(
            self.center_frame, bg=CARD_BG,
            highlightthickness=1, highlightbackground=CARD_BORDER,
            padx=16, pady=16
        )
        samples_card.pack(fill="x")

        tk.Label(
            samples_card, text="Sample Questions (Click to Ask)",
            font=(FONT_FAMILY, 11, "bold"),
            fg=TEXT_PRIMARY, bg=CARD_BG
        ).pack(anchor="w")

        samples = [
            "What is a primary key?",
            "Explain functions in Python",
            "What is HTML?",
            "Difference between Git and GitHub",
            "calculate 25 + 30",
            "What is today's date?",
            "What is the time?",
            "help"
        ]

        for s in samples:
            btn = tk.Button(
                samples_card, text=f"•  {s}",
                anchor="w", font=(FONT_FAMILY, 9),
                bg=CARD_BG, fg=PRIMARY_BUTTON,
                activebackground=USER_MSG_BG, activeforeground=PRIMARY_BUTTON,
                relief="flat", bd=0, padx=6, pady=3, cursor="hand2",
                command=lambda q=s: self.send_query_directly(q)
            )
            btn.pack(fill="x", pady=2)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=USER_MSG_BG))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=CARD_BG))

    # --------------------------------------------------------------------------
    # View 3: Study Topics Directory
    # --------------------------------------------------------------------------
    def _render_study_topics_view(self):
        """Displays organized directory of supported educational topics."""
        tk.Label(
            self.center_frame, text="Study Topics",
            font=(FONT_FAMILY, 20, "bold"),
            fg=TEXT_PRIMARY, bg=MAIN_BG
        ).pack(anchor="w", pady=(6, 0))

        tk.Label(
            self.center_frame,
            text="Comprehensive reference list of foundational computer science topics.",
            font=(FONT_FAMILY, 10),
            fg=TEXT_SECONDARY, bg=MAIN_BG
        ).pack(anchor="w", pady=(4, 16))

        sections = [
            (
                "Python Programming",
                [
                    ("Python Language", "Interpreted high-level language with clear syntax.", "What is Python?"),
                    ("Variables", "Reserved memory locations used to store program data.", "What is a variable?"),
                    ("Loops", "Control structures that repeat code blocks on condition.", "What is a loop?"),
                    ("Functions", "Reusable blocks of code designed to perform a task.", "What is a function?"),
                    ("Lists", "Ordered, mutable collections of items in square brackets.", "What is a list?")
                ]
            ),
            (
                "Database Systems & SQL",
                [
                    ("DBMS", "Software to manage, store, and organize structured data.", "What is DBMS?"),
                    ("SQL", "Standard language for querying relational databases.", "What is SQL?"),
                    ("Database", "Electronic repository of organized information.", "What is a database?"),
                    ("Primary Key", "Unique identifier assigned to each record in a table.", "What is a primary key?"),
                    ("Normalization", "Process of organizing data to eliminate redundancy.", "What is normalization?")
                ]
            ),
            (
                "Web Development",
                [
                    ("HTML Markup", "Standard structure and semantic elements of web pages.", "What is HTML?"),
                    ("CSS Styling", "Style sheets defining layout, colors, and typography.", "Why use CSS?")
                ]
            ),
            (
                "Version Control",
                [
                    ("Git", "Distributed version control system for source code tracking.", "What is Git?"),
                    ("GitHub", "Cloud platform for repository hosting and collaboration.", "What is GitHub?")
                ]
            ),
            (
                "Programming Basics",
                [
                    ("Algorithms", "Step-by-step set of instructions to solve a problem.", "What is an algorithm?"),
                    ("Debugging", "Locating and resolving defects or errors in code.", "What is debugging?"),
                    ("Syntax", "Grammatical rules governing valid program statements.", "What is syntax?"),
                    ("Comments", "Human-readable notes within source code.", "What is a comment?")
                ]
            )
        ]

        for sec_title, items in sections:
            sec_hdr = tk.Label(
                self.center_frame, text=sec_title,
                font=(FONT_FAMILY, 12, "bold"),
                fg=TEXT_PRIMARY, bg=MAIN_BG
            )
            sec_hdr.pack(anchor="w", pady=(12, 6))

            for title, desc, sample_q in items:
                row_box = tk.Frame(
                    self.center_frame, bg=CARD_BG,
                    highlightthickness=1, highlightbackground=CARD_BORDER,
                    padx=14, pady=8
                )
                row_box.pack(fill="x", pady=3)

                info_sub = tk.Frame(row_box, bg=CARD_BG)
                info_sub.pack(side="left", fill="both", expand=True)

                tk.Label(
                    info_sub, text=title,
                    font=(FONT_FAMILY, 9, "bold"),
                    fg=TEXT_PRIMARY, bg=CARD_BG
                ).pack(anchor="w")

                tk.Label(
                    info_sub, text=desc,
                    font=(FONT_FAMILY, 8),
                    fg=TEXT_SECONDARY, bg=CARD_BG, justify="left"
                ).pack(anchor="w")

                btn = tk.Button(
                    row_box, text="Review",
                    font=(FONT_FAMILY, 8, "bold"),
                    bg=PRIMARY_BUTTON, fg=BTN_TEXT,
                    activebackground=BUTTON_HOVER, activeforeground=BTN_TEXT,
                    relief="flat", bd=0, padx=12, pady=4, cursor="hand2",
                    command=lambda q=sample_q: self.send_query_directly(q)
                )
                btn.pack(side="right")
                btn.bind("<Enter>", lambda e, b=btn: b.config(bg=BUTTON_HOVER))
                btn.bind("<Leave>", lambda e, b=btn: b.config(bg=PRIMARY_BUTTON))

    # --------------------------------------------------------------------------
    # View 4: Calculator
    # --------------------------------------------------------------------------
    def _render_calculator_view(self):
        """Renders an interactive working calculator for addition, subtraction, multiplication, and division."""
        tk.Label(
            self.center_frame, text="Calculator",
            font=(FONT_FAMILY, 20, "bold"),
            fg=TEXT_PRIMARY, bg=MAIN_BG
        ).pack(anchor="w", pady=(6, 0))

        tk.Label(
            self.center_frame,
            text="Safe arithmetic evaluator for addition, subtraction, multiplication, and division.",
            font=(FONT_FAMILY, 10),
            fg=TEXT_SECONDARY, bg=MAIN_BG
        ).pack(anchor="w", pady=(4, 16))

        # Main Calculator Card
        calc_card = tk.Frame(
            self.center_frame, bg=CARD_BG,
            highlightthickness=1, highlightbackground=CARD_BORDER,
            padx=18, pady=16
        )
        calc_card.pack(fill="x", pady=(0, 16))

        # Display screen
        display_frame = tk.Frame(
            calc_card, bg=MAIN_BG,
            highlightthickness=1, highlightbackground=CARD_BORDER,
            padx=10, pady=8
        )
        display_frame.pack(fill="x", pady=(0, 12))

        self.calc_display_entry = tk.Entry(
            display_frame, textvariable=self.calc_display_var,
            font=(FONT_FAMILY, 14, "bold"),
            bg=MAIN_BG, fg=TEXT_PRIMARY,
            justify="right", relief="flat", bd=0
        )
        self.calc_display_entry.pack(fill="x")

        # Status label
        tk.Label(
            calc_card, textvariable=self.calc_status_var,
            font=(FONT_FAMILY, 9),
            fg=TEXT_SECONDARY, bg=CARD_BG, anchor="w"
        ).pack(fill="x", pady=(0, 10))

        # Keypad Grid
        keypad_frame = tk.Frame(calc_card, bg=CARD_BG)
        keypad_frame.pack(fill="x")

        for col_idx in range(4):
            keypad_frame.grid_columnconfigure(col_idx, weight=1)

        keypad = [
            ("7", 0, 0), ("8", 0, 1), ("9", 0, 2), ("/", 0, 3),
            ("4", 1, 0), ("5", 1, 1), ("6", 1, 2), ("*", 1, 3),
            ("1", 2, 0), ("2", 2, 1), ("3", 2, 2), ("-", 2, 3),
            ("C", 3, 0), ("0", 3, 1), (".", 3, 2), ("+", 3, 3)
        ]

        for label, r, c in keypad:
            is_op = label in ["/", "*", "-", "+"]
            is_c = (label == "C")

            bg_c = CARD_BORDER if is_op else (MAIN_BG if not is_c else MAIN_BG)
            fg_c = PRIMARY_BUTTON if is_op else (TEXT_PRIMARY)

            btn = tk.Button(
                keypad_frame, text=label,
                font=(FONT_FAMILY, 10, "bold"),
                bg=bg_c, fg=fg_c,
                activebackground=CARD_BORDER, activeforeground=TEXT_PRIMARY,
                relief="flat", bd=1, highlightthickness=1,
                highlightbackground=CARD_BORDER, pady=8, cursor="hand2",
                command=lambda val=label: self._on_calc_btn_click(val)
            )
            btn.grid(row=r, column=c, padx=3, pady=3, sticky="nsew")

        # Bottom Action Row: Equals & Send to Workspace
        calc_actions = tk.Frame(calc_card, bg=CARD_BG)
        calc_actions.pack(fill="x", pady=(8, 0))

        equals_btn = tk.Button(
            calc_actions, text="=  Calculate",
            font=(FONT_FAMILY, 10, "bold"),
            bg=PRIMARY_BUTTON, fg=BTN_TEXT,
            activebackground=BUTTON_HOVER, activeforeground=BTN_TEXT,
            relief="flat", bd=0, padx=16, pady=8, cursor="hand2",
            command=self._execute_local_calc
        )
        equals_btn.pack(side="left", fill="x", expand=True, padx=(0, 6))
        equals_btn.bind("<Enter>", lambda e: equals_btn.config(bg=BUTTON_HOVER))
        equals_btn.bind("<Leave>", lambda e: equals_btn.config(bg=PRIMARY_BUTTON))

        send_to_qa_btn = tk.Button(
            calc_actions, text="Send to Workspace",
            font=(FONT_FAMILY, 9, "bold"),
            bg=MAIN_BG, fg=TEXT_PRIMARY,
            activebackground=CARD_BORDER, activeforeground=TEXT_PRIMARY,
            relief="flat", bd=1, highlightthickness=1,
            highlightbackground=CARD_BORDER, padx=14, pady=8, cursor="hand2",
            command=self._send_calc_to_qa
        )
        send_to_qa_btn.pack(side="right")
        send_to_qa_btn.bind("<Enter>", lambda e: send_to_qa_btn.config(bg=CARD_BORDER))
        send_to_qa_btn.bind("<Leave>", lambda e: send_to_qa_btn.config(bg=MAIN_BG))

        # Quick Calculation Presets
        presets_card = tk.Frame(
            self.center_frame, bg=CARD_BG,
            highlightthickness=1, highlightbackground=CARD_BORDER,
            padx=16, pady=14
        )
        presets_card.pack(fill="x")

        tk.Label(
            presets_card, text="Quick Calculations (Run Expression)",
            font=(FONT_FAMILY, 11, "bold"),
            fg=TEXT_PRIMARY, bg=CARD_BG
        ).pack(anchor="w")

        tk.Label(
            presets_card,
            text="Click any standard math test to evaluate arithmetic safety and zero division guard.",
            font=(FONT_FAMILY, 9),
            fg=TEXT_SECONDARY, bg=CARD_BG
        ).pack(anchor="w", pady=(2, 8))

        presets_row = tk.Frame(presets_card, bg=CARD_BG)
        presets_row.pack(anchor="w")

        presets = ["25 + 30", "100 - 45", "12 * 8", "144 / 12", "10 / 0"]
        for p in presets:
            btn = tk.Button(
                presets_row, text=p,
                font=(FONT_FAMILY, 9, "bold"),
                bg=MAIN_BG, fg=TEXT_PRIMARY,
                activebackground=CARD_BORDER, activeforeground=TEXT_PRIMARY,
                relief="flat", bd=1, highlightthickness=1,
                highlightbackground=CARD_BORDER, padx=8, pady=4, cursor="hand2",
                command=lambda expr=p: self._load_and_run_preset(expr)
            )
            btn.pack(side="left", padx=(0, 6), pady=2)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=CARD_BORDER))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=MAIN_BG))

    def _on_calc_btn_click(self, char):
        """Appends digits and operators to calculator display."""
        if char == "C":
            self.calc_expr = ""
            self.calc_display_var.set("0")
            self.calc_status_var.set("Ready for calculation (+, -, *, /)")
            return

        current = self.calc_expr
        if current == "" and char in ["+", "-", "*", "/"]:
            if char != "-":
                return

        # Replace operators or append
        if char in ["+", "-", "*", "/"]:
            self.calc_expr = f"{current} {char} "
        else:
            self.calc_expr = current + char

        self.calc_display_var.set(self.calc_expr.strip())

    def _execute_local_calc(self):
        """Evaluates active calculator expression using chatbot.safe_calculate."""
        expr = self.calc_expr.strip()
        if not expr:
            self.calc_status_var.set("Please enter an expression.")
            return

        result_msg, is_success = chatbot.safe_calculate(expr)
        self.calc_status_var.set(result_msg)

        if is_success:
            # Extract number from "The result is <val>."
            val = result_msg.replace("The result is", "").replace(".", "").strip()
            self.calc_display_var.set(val)
            self.calc_expr = val

    def _send_calc_to_qa(self):
        """Sends current calculator expression directly into the Q&A conversation."""
        expr = self.calc_expr.strip()
        if not expr:
            expr = "25 + 30"
        self.send_query_directly(f"calculate {expr}")

    def _load_and_run_preset(self, expr):
        """Loads and executes a math preset expression."""
        self.calc_expr = expr
        self.calc_display_var.set(expr)
        self._execute_local_calc()

    # --------------------------------------------------------------------------
    # View 5: Date & Time
    # --------------------------------------------------------------------------
    def _render_date_time_view(self):
        """Renders live system calendar date and clock with working Refresh control."""
        tk.Label(
            self.center_frame, text="Date & Time",
            font=(FONT_FAMILY, 20, "bold"),
            fg=TEXT_PRIMARY, bg=MAIN_BG
        ).pack(anchor="w", pady=(6, 0))

        tk.Label(
            self.center_frame,
            text="Query live calendar date and current system clock from the Python runtime.",
            font=(FONT_FAMILY, 10),
            fg=TEXT_SECONDARY, bg=MAIN_BG
        ).pack(anchor="w", pady=(4, 16))

        card = tk.Frame(
            self.center_frame, bg=CARD_BG,
            highlightthickness=1, highlightbackground=CARD_BORDER,
            padx=18, pady=18
        )
        card.pack(fill="x", pady=(0, 16))

        # Initial timestamp population
        self._refresh_date_time()

        date_row = tk.Frame(card, bg=CARD_BG)
        date_row.pack(anchor="w", pady=(0, 6))

        tk.Label(
            date_row, text="Current Date:  ",
            font=(FONT_FAMILY, 11, "bold"),
            fg=TEXT_PRIMARY, bg=CARD_BG
        ).pack(side="left")

        tk.Label(
            date_row, textvariable=self.date_var,
            font=(FONT_FAMILY, 11),
            fg=PRIMARY_BUTTON, bg=CARD_BG
        ).pack(side="left")

        time_row = tk.Frame(card, bg=CARD_BG)
        time_row.pack(anchor="w", pady=(0, 16))

        tk.Label(
            time_row, text="Current Time:  ",
            font=(FONT_FAMILY, 11, "bold"),
            fg=TEXT_PRIMARY, bg=CARD_BG
        ).pack(side="left")

        tk.Label(
            time_row, textvariable=self.time_var,
            font=(FONT_FAMILY, 11),
            fg=PRIMARY_BUTTON, bg=CARD_BG
        ).pack(side="left")

        actions_row = tk.Frame(card, bg=CARD_BG)
        actions_row.pack(anchor="w")

        # Working Refresh Button
        refresh_btn = tk.Button(
            actions_row, text="Refresh",
            font=(FONT_FAMILY, 9, "bold"),
            bg=PRIMARY_BUTTON, fg=BTN_TEXT,
            activebackground=BUTTON_HOVER, activeforeground=BTN_TEXT,
            relief="flat", bd=0, padx=14, pady=6, cursor="hand2",
            command=self._refresh_date_time
        )
        refresh_btn.pack(side="left", padx=(0, 8))
        refresh_btn.bind("<Enter>", lambda e, b=refresh_btn: b.config(bg=BUTTON_HOVER))
        refresh_btn.bind("<Leave>", lambda e, b=refresh_btn: b.config(bg=PRIMARY_BUTTON))

        date_btn = tk.Button(
            actions_row, text="Ask Date in Workspace",
            font=(FONT_FAMILY, 9),
            bg=MAIN_BG, fg=TEXT_PRIMARY,
            activebackground=CARD_BORDER, activeforeground=TEXT_PRIMARY,
            relief="flat", bd=1, highlightthickness=1,
            highlightbackground=CARD_BORDER, padx=12, pady=6, cursor="hand2",
            command=lambda: self.send_query_directly("What is today's date?")
        )
        date_btn.pack(side="left", padx=(0, 8))
        date_btn.bind("<Enter>", lambda e, b=date_btn: b.config(bg=CARD_BORDER))
        date_btn.bind("<Leave>", lambda e, b=date_btn: b.config(bg=MAIN_BG))

        time_btn = tk.Button(
            actions_row, text="Ask Time in Workspace",
            font=(FONT_FAMILY, 9),
            bg=MAIN_BG, fg=TEXT_PRIMARY,
            activebackground=CARD_BORDER, activeforeground=TEXT_PRIMARY,
            relief="flat", bd=1, highlightthickness=1,
            highlightbackground=CARD_BORDER, padx=12, pady=6, cursor="hand2",
            command=lambda: self.send_query_directly("What is the time?")
        )
        time_btn.pack(side="left")
        time_btn.bind("<Enter>", lambda e, b=time_btn: b.config(bg=CARD_BORDER))
        time_btn.bind("<Leave>", lambda e, b=time_btn: b.config(bg=MAIN_BG))

    def _refresh_date_time(self):
        """Updates the system date and clock strings live."""
        now = datetime.now()
        self.date_var.set(now.strftime("%A, %B %d, %Y"))
        self.time_var.set(now.strftime("%I:%M:%S %p"))

    def _focus_input(self):
        """Focuses the input entry on the right workspace."""
        self.entry.focus_set()
        if self.entry_has_placeholder:
            self._on_entry_focus_in()

    # ==========================================================================
    # REGION 3: RIGHT QUESTION-AND-ANSWER WORKSPACE
    # ==========================================================================
    def create_qa_workspace(self):
        """Creates the right side Question-and-Answer workspace with scrollable cards and fixed bottom input."""
        self.qa_frame = tk.Frame(
            self.root, bg=MAIN_BG, padx=16, pady=16,
            highlightthickness=1, highlightbackground=CARD_BORDER
        )
        self.qa_frame.grid(row=0, column=2, sticky="nsew", padx=(0, 14), pady=14)

        self.qa_frame.grid_rowconfigure(0, weight=0)  # QA Header (fixed)
        self.qa_frame.grid_rowconfigure(1, weight=1)  # Scrollable Conversation (expands)
        self.qa_frame.grid_rowconfigure(2, weight=0)  # Bottom Input Bar (fixed)
        self.qa_frame.grid_columnconfigure(0, weight=1)

        # Header Section
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

        # Scrollable Conversation Container
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

        self.canvas.bind("<Enter>", lambda e: self._bind_mousewheel(self.canvas, self._on_mousewheel_qa))
        self.canvas.bind("<Leave>", lambda e: self._unbind_mousewheel())

        # Fixed Bottom Input Bar
        self.create_qa_input_area()

    def resize_message_area(self, event):
        """Dynamically adjusts message inner frame and text wrapping on window resize."""
        self.canvas.itemconfigure(self.window_id, width=event.width)
        calc_wrap = max(200, event.width - 75)
        for row in self.messages_frame.winfo_children():
            for card in row.winfo_children():
                for child in card.winfo_children():
                    if isinstance(child, tk.Label) and child.cget("wraplength") > 0:
                        child.config(wraplength=calc_wrap)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def create_qa_input_area(self):
        """Creates the fixed bottom input bar with Send and Clear controls."""
        bottom = tk.Frame(
            self.qa_frame, bg=CARD_BG,
            highlightthickness=1, highlightbackground=CARD_BORDER,
            padx=10, pady=10
        )
        bottom.grid(row=2, column=0, sticky="ew")

        # Input Entry Container
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
        self.entry_box = self.entry  # Alias for compatibility

        self.entry.insert(0, self.placeholder)
        self.entry.bind("<FocusIn>", self._on_entry_focus_in)
        self.entry.bind("<FocusOut>", self._on_entry_focus_out)
        self.entry.bind("<Return>", self.send_message)

        # Primary Button: Send
        self.send_button = tk.Button(
            bottom, text="Send", command=self.send_message,
            font=(FONT_FAMILY, 9, "bold"),
            bg=PRIMARY_BUTTON, fg=BTN_TEXT,
            activebackground=BUTTON_HOVER, activeforeground=BTN_TEXT,
            relief="flat", bd=0, padx=16, pady=7, cursor="hand2"
        )
        self.send_button.pack(side="left", padx=(0, 6))
        self.send_btn = self.send_button  # Alias for compatibility

        self.send_button.bind("<Enter>", lambda e: self.send_button.config(bg=BUTTON_HOVER))
        self.send_button.bind("<Leave>", lambda e: self.send_button.config(bg=PRIMARY_BUTTON))

        # Secondary Button: Clear
        self.clear_button = tk.Button(
            bottom, text="Clear", command=self.clear_chat,
            font=(FONT_FAMILY, 9),
            bg=CARD_BG, fg=TEXT_SECONDARY,
            activebackground=MAIN_BG, activeforeground=TEXT_PRIMARY,
            relief="flat", bd=1, highlightthickness=1,
            highlightbackground=CARD_BORDER, padx=12, pady=6, cursor="hand2"
        )
        self.clear_button.pack(side="left")
        self.clear_btn = self.clear_button  # Alias for compatibility

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
        """Displays initial StudyMate greeting card without emojis."""
        welcome_text = (
            "Hello! I'm StudyMate, your student learning assistant.\n\n"
            "I can help you understand basic programming concepts and answer "
            "questions about Python, DBMS, HTML, CSS, Git, and GitHub.\n\n"
            "Type a question below to get started."
        )
        self.display_bot_message(welcome_text)

    def display_user_message(self, message):
        """Displays user message aligned right in a muted blue-grey card."""
        timestamp = datetime.now().strftime("%I:%M %p").lstrip("0")
        self.add_message_card("You", message, timestamp, is_user=True)

    def display_bot_message(self, message):
        """Displays StudyMate assistant message aligned left in a white card."""
        timestamp = datetime.now().strftime("%I:%M %p").lstrip("0")
        self.add_message_card("StudyMate", message, timestamp, is_user=False)

    def add_message_card(self, sender, message, timestamp, is_user=False):
        """Renders an individual rectangular message card with clean borders and no emojis."""
        row = tk.Frame(self.messages_frame, bg=MAIN_BG)
        row.pack(fill="x", pady=4, padx=6)

        canvas_w = self.canvas.winfo_width()
        wrap_width = max(200, canvas_w - 75) if canvas_w > 150 else 300

        if is_user:
            # User Message Card (Align Right, Muted Blue-Grey)
            card = tk.Frame(
                row, bg=USER_MSG_BG,
                highlightthickness=1, highlightbackground=CARD_BORDER,
                padx=14, pady=10
            )
            card.pack(side="right", anchor="e")

            # Header
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

            # Content
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

            # Header
            hdr = tk.Frame(card, bg=BOT_MSG_BG)
            hdr.pack(anchor="w", fill="x")

            tk.Label(
                hdr, text=sender,
                font=(FONT_FAMILY, 9, "bold"),
                fg=PRIMARY_BUTTON, bg=BOT_MSG_BG
            ).pack(side="left")

            tk.Label(
                hdr, text=f" • {timestamp}",
                font=(FONT_FAMILY, 8),
                fg=TEXT_SECONDARY, bg=BOT_MSG_BG
            ).pack(side="left")

            # Content
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
        """Directly executes a query into the Question-and-Answer workspace."""
        clean_input = raw_input.strip()
        if not clean_input:
            return

        user_input = clean_input.lower()
        self.display_user_message(clean_input)

        bot_response, self.user_name = chatbot.get_response(
            user_input, clean_input, self.user_name
        )

        display_response = bot_response
        if display_response.startswith("StudyMate: "):
            display_response = display_response[len("StudyMate: "):]

        self.display_bot_message(display_response)
        chatbot.save_chat_history(clean_input, bot_response)

        # Refocus entry
        self.entry.focus_set()

    def send_message(self, event=None):
        """Processes user input from the bottom entry box."""
        if self.entry_has_placeholder:
            raw_input = ""
        else:
            raw_input = self.entry.get()

        user_input = raw_input.strip().lower()

        if not user_input:
            self.entry.delete(0, tk.END)
            self._on_entry_focus_out()
            self.display_bot_message("Please enter a question or topic.")
            self.entry.focus_set()
            return "break"

        self.entry.delete(0, tk.END)
        self.entry_has_placeholder = False
        self.send_query_directly(raw_input)

        # Always return focus to entry field for consecutive questions
        self.entry.focus_set()
        return "break"

    def clear_chat(self):
        """Clears visible message cards and restores welcome card without clearing session name or history file."""
        for widget in self.messages_frame.winfo_children():
            widget.destroy()
        self.display_welcome_message()
        self.canvas.yview_moveto(0.0)
        self.entry.focus_set()


def create_gui():
    """Instantiates and starts the Tkinter mainloop for StudyMate."""
    root = tk.Tk()
    StudyMateGUI(root)
    root.mainloop()


if __name__ == "__main__":
    create_gui()
