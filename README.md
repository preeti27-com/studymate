# StudyMate – Student Assistant Chatbot
**CodeAlpha Internship Project**

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

### Part 5: Graphical User Interface (Tkinter GUI)
- **Modern Interface**: Header with title, subtitle, and Clear Chat button.
- **Message Alignment**: User messages aligned to the right (blue), bot messages aligned to the left (teal/dark slate).
- **Timestamps**: Every message features a formatted timestamp.
- **Keyboard Shortcuts**: Pressing `Enter` sends messages cleanly without extra newlines.
- **Clear Chat**: Clears visible GUI conversation while retaining `chat_history.txt` and session memory.
- **Resizable Window**: Responsive layout that scales gracefully.

---

## Directory Structure

```text
StudyMate-Chatbot/
├── main.py            # Main application launcher (GUI by default, CLI optional)
├── gui.py             # Tkinter GUI implementation (StudyMateGUI)
├── chatbot.py         # Core rule-based chatbot engine & knowledge base
├── chat_history.txt   # Local persistent conversation log file
└── README.md          # Project documentation
```

---

## Requirements & Installation

- **Python Version**: Python 3.7 or higher
- **Dependencies**: Uses Python built-in standard modules only (`tkinter`, `random`, `datetime`, `sys`, `os`). No external packages required!

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
