# StudyMate – Student Assistant Chatbot
**CodeAlpha Internship Project**

![Python](https://img.shields.io/badge/Python-3.7+-3776AB?logo=python&logoColor=white)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Tests](https://img.shields.io/badge/Tests-25%20Passing-brightgreen)
![GUI](https://img.shields.io/badge/GUI-Tkinter-blue)

StudyMate is a Python rule-based student assistant chatbot designed to help students learn foundational computer science concepts, perform safe basic arithmetic calculations, query current system date/time, and remember user names within a session.

---

## Features Overview

### Part 1: Core Chatbot Engine
- Rule-based conversation matching using pattern dictionaries.
- Topics covered: Python, DBMS, HTML, CSS, Git, GitHub, Programming Basics.
- Basic greetings, exit commands (`bye`, `exit`, `quit`), and fallback handling.

### Part 2: Knowledge Base Expansion & Name Memory
- Comprehensive educational Q&A dictionary.
- Session-based name memory (`My name is [Name]`, `Call me [Name]`, `What is my name?`).
- Personalized greetings and responses when user name is stored.

### Part 3: System Date, Time, Safe Calculator & Help System
- **Date Feature**: Fetches live system date using Python's `datetime` module.
- **Time Feature**: Fetches live system time in 12-hour AM/PM format.
- **Safe Basic Calculator**: Evaluates basic math expressions (`+`, `-`, `*`, `/`) safely without `eval()`, preventing division by zero crashes.
- **Help Feature**: Displays available topics and sample questions (`help`).

### Part 4: Conversational Polish & Chat History
- **Randomized Responses**: Uses `random.choice()` for varied small talk and greetings.
- **Extended Greetings**: Support for `good morning`, `good afternoon`, `good evening`, `thanks`.
- **Local Chat History**: Automatically logs timestamped turns (`[10:30:25 PM]`) into `chat_history.txt`.
- **Input Validation**: Graceful handling of empty/whitespace inputs and unknown question suggestions.

### Part 5: Academic Learning Workspace (Tkinter Split Workspace GUI)
- **Split Workspace Architecture**: Three-region layout with Left Sidebar, Center Learning Desk, and Right Question-and-Answer Workspace.
- **Left Navy Navigation Sidebar** (`#15243A`): Application branding (`StudyMate • Student Learning Workspace`) and active navigation controls (Overview, Ask a Question, Study Topics, Calculator, Date & Time).
- **Learning Desk Dashboard**: Clean cards for foundational topics (Python, Database Systems, Web Development, Version Control) with interactive `Explore Topic` triggers and a `Quick Actions` suite.
- **Dedicated Question Workspace**: Separate rectangular message cards with subtle borders (`#DFE5ED`), comfortable padding, automatic text wrapping, and clean timestamps (Assistant on left `#FFFFFF`, User on right `#E7EDF5`).
- **Fixed Bottom Input Area**: Integrated input field with `Send` (`#294E80`) and `Clear` controls, keyboard navigation (`Enter` to submit), and persistent canvas auto-scrolling.
- **Mature Academic Aesthetic**: Segoe UI typography, cohesive academic color palette, zero emojis, zero artificial animations or marketing hype.
- **Window Specs**: 1200 x 760 initial dimensions with a 900 x 600 minimum size for reliable, responsive desktop performance.

---

## Directory Structure

```text
StudyMate-Chatbot/
├── main.py            # Main application launcher (GUI by default, CLI optional)
├── gui.py             # Tkinter desktop GUI implementation
├── chatbot.py         # Core rule-based chatbot engine & knowledge base
├── test_chatbot.py    # Automated test suite (25 unit tests)
├── index.html         # Handcrafted modern web chat interface (Vercel ready)
├── style.css          # Human-designed warm stylesheet with light/dark theme
├── script.js          # Interactive web client with Vercel API & offline engine
├── vercel.json        # Vercel serverless deployment routing configuration
├── api/
│   └── chat.py        # Vercel Python serverless endpoint (/api/chat)
├── requirements.txt   # Dependencies specification (Standard Library only)
├── LICENSE            # MIT open-source license
├── .gitignore         # Git ignore rules for Python bytecode and IDE files
├── chat_history.txt   # Local persistent conversation log file
└── README.md          # Project documentation
```

---

## Requirements & Installation

- **Python Version**: Python 3.7 or higher
- **Dependencies**: Uses Python built-in standard modules only (`tkinter`, `random`, `datetime`, `sys`, `os`, `unittest`, `http.server`). No external packages required!

---

## How to Run

### 1. Launch GUI Application (Default)
Run `main.py` or `gui.py`:

```bash
python main.py
```
or
```bash
python gui.py
```

### 2. Launch Terminal Mode (CLI)
Pass `--cli` flag to `main.py` or run `chatbot.py` directly:

```bash
python main.py --cli
```
or
```bash
python chatbot.py
```

### 3. Run Automated Tests
Run the complete unit test suite:

```bash
python -m unittest test_chatbot.py -v
```

### 4. Deploy to Vercel (Web Version)
You can deploy StudyMate live to the web using Vercel with zero server setup:

1. Push your repository to GitHub.
2. Go to [vercel.com](https://vercel.com) and click **"Add New Project"**.
3. Import your `StudyMate-Chatbot` GitHub repository.
4. Click **Deploy**. Vercel will automatically build the static frontend (`index.html`) and configure the Python serverless API function ([api/chat.py](file:///c:/Users/proku/Desktop/StudyMate-Chatbot/api/chat.py)).

---

## Sample Questions & Commands

- **Python**: *"What is Python?"*, *"Explain variable"*, *"What is a function?"*
- **DBMS**: *"What is DBMS?"*, *"What is SQL?"*, *"What is a primary key?"*
- **HTML & CSS**: *"What is HTML?"*, *"What is an HTML tag?"*, *"What is CSS?"*, *"Why use CSS?"*
- **Git & GitHub**: *"What is Git?"*, *"What is GitHub?"*, *"What is a repository?"*
- **Date & Time**: *"What is today's date?"*, *"What is the time?"*
- **Calculator**: *"calculate 25 + 30"*, *"20 - 8"*, *"6 * 7"*, *"20 / 4"*, *"10 / 0"*
- **Name Memory**: *"My name is Preeti"*, *"What is my name?"*
- **Help**: *"help"*

