"""
StudyMate - Main Application Launcher
CodeAlpha Internship Project

This is the main entry point for StudyMate Chatbot.
Launches the Tkinter Graphical User Interface (GUI) by default.
Can optionally launch Terminal Mode by passing '--cli' or '-c'.
"""

import sys
import gui
import chatbot


def main():
    """
    Main launcher for StudyMate.
    Launches the GUI by default or CLI if requested.
    """
    if len(sys.argv) > 1 and sys.argv[1].lower() in ["--cli", "-c", "cli"]:
        print("Launching StudyMate in Terminal Mode...")
        chatbot.main()
    else:
        print("Launching StudyMate GUI Application...")
        gui.create_gui()


if __name__ == "__main__":
    main()
