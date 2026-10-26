"""
StudyMate - Rule-Based Student Chatbot (Part 4: Polished Terminal Chatbot)
CodeAlpha Internship Project

This module extends Parts 1, 2, and 3 by adding:
1. Randomized Conversational Responses: Uses random.choice() for greetings and small talk.
2. Improved General Conversation: Adds support for good morning, good afternoon, good evening, thanks.
3. Expanded Question Variations: Supports more question patterns for Python, DBMS, HTML, CSS, Git, GitHub.
4. Local Chat History: Appends timestamped turns to chat_history.txt without requiring a database.
5. Robust Input Validation: Handles empty input, invalid calculator queries, and division by zero gracefully.
6. Improved Fallback Suggestions: Guides users to supported topics when a question isn't in the knowledge base.
"""

import random
import sys
from datetime import datetime

# Reconfigure stdout for UTF-8 encoding on Windows consoles if supported
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# ==============================================================================
# FEATURE 1: STUDENT KNOWLEDGE BASE (Dictionary-Based Structure)
# ==============================================================================
KNOWLEDGE_BASE = {
    # ------------------ PYTHON ------------------
    "python": {
        "patterns": [
            "what is python", "explain python", "tell me about python",
            "what do you know about python", "python"
        ],
        "answer": "Python is a high-level, interpreted programming language known for its easy-to-read syntax and versatility."
    },
    "variable": {
        "patterns": [
            "what is a variable", "explain variable", "tell me about variable",
            "what is variable", "what are variables", "variable"
        ],
        "answer": "A variable is a reserved memory location used to store values or data in a program."
    },
    "loop": {
        "patterns": [
            "what is a loop", "explain loop", "tell me about loop",
            "what is loop", "what are loops", "loop"
        ],
        "answer": "A loop is a control structure used to repeat a block of code multiple times as long as a specified condition is met."
    },
    "function": {
        "patterns": [
            "what is a function", "explain function", "tell me about function",
            "what is function", "what are functions", "function"
        ],
        "answer": "A function is a reusable block of code designed to perform a specific task when called."
    },
    "list": {
        "patterns": [
            "what is a list", "explain list", "tell me about list",
            "what is list", "what are lists", "list"
        ],
        "answer": "A list is an ordered, mutable collection of items in Python enclosed in square brackets []."
    },

    # ------------------ DBMS ------------------
    "dbms": {
        "patterns": [
            "what is dbms", "explain dbms", "tell me about dbms",
            "what do you know about dbms", "dbms"
        ],
        "answer": "DBMS (Database Management System) is software used to store, manage, retrieve, and organize data efficiently."
    },
    "sql": {
        "patterns": [
            "what is sql", "explain sql", "tell me about sql", "sql"
        ],
        "answer": "SQL (Structured Query Language) is the standard language used to communicate with and manipulate relational databases."
    },
    "database": {
        "patterns": [
            "what is a database", "explain database", "tell me about database",
            "what is database", "database"
        ],
        "answer": "A database is an organized collection of structured data stored electronically for easy access and management."
    },
    "primary_key": {
        "patterns": [
            "what is a primary key", "explain primary key", "tell me about primary key",
            "what is primary key", "primary key"
        ],
        "answer": "A primary key is a unique identifier assigned to each record in a database table. It cannot contain null values."
    },
    "normalization": {
        "patterns": [
            "what is normalization", "explain normalization", "tell me about normalization",
            "normalization"
        ],
        "answer": "Normalization is the process of organizing data in a database to reduce data redundancy and improve data integrity."
    },

    # ------------------ HTML ------------------
    "html": {
        "patterns": [
            "what is html", "explain html", "tell me about html",
            "what do you know about html", "html"
        ],
        "answer": "HTML (HyperText Markup Language) is the standard markup language used to structure web pages and their content."
    },
    "html_tag": {
        "patterns": [
            "what is an html tag", "explain html tag", "what is html tag",
            "tell me about html tag", "what are html tags", "html tag"
        ],
        "answer": "An HTML tag is a piece of markup language used to mark the start and end of an HTML element (e.g., <p>, <h1>)."
    },
    "html_element": {
        "patterns": [
            "what is an html element", "explain html element", "what is html element",
            "tell me about html element", "html element"
        ],
        "answer": "An HTML element consists of a start tag, content, and an end tag (e.g., <p>Hello</p>)."
    },

    # ------------------ CSS ------------------
    "css": {
        "patterns": [
            "what is css", "explain css", "tell me about css",
            "why is css used", "purpose of css", "css"
        ],
        "answer": "CSS (Cascading Style Sheets) is a language used to describe the visual presentation and layout of HTML documents."
    },
    "css_selector": {
        "patterns": [
            "what is a css selector", "explain css selector", "what is css selector",
            "tell me about css selector", "css selector"
        ],
        "answer": "A CSS selector is a pattern used to target and select the HTML elements you want to style (e.g., class, ID, element type)."
    },
    "why_css": {
        "patterns": [
            "why use css", "why css used", "why css"
        ],
        "answer": "CSS is used to separate web content (HTML) from visual presentation, making websites attractive, consistent, and responsive."
    },

    # ------------------ GIT & GITHUB ------------------
    "git": {
        "patterns": [
            "what is git", "explain git", "tell me about git", "git"
        ],
        "answer": "Git is a distributed version control system that tracks changes in source code during software development."
    },
    "github": {
        "patterns": [
            "what is github", "explain github", "tell me about github", "github"
        ],
        "answer": "GitHub is a cloud-based hosting platform that lets developers store, manage, track, and collaborate on Git repositories."
    },
    "repository": {
        "patterns": [
            "what is a repository", "explain repository", "tell me about repository",
            "what is repo", "what is repository", "repository"
        ],
        "answer": "A repository (repo) is a storage location where all the files, folders, and commit history of a project are kept."
    },
    "git_push": {
        "patterns": [
            "what is git push", "explain git push", "tell me about git push",
            "how git push works", "git push"
        ],
        "answer": "Git push is a command used to upload local repository commits to a remote repository like GitHub."
    },

    # ------------------ PROGRAMMING BASICS ------------------
    "programming": {
        "patterns": [
            "what is programming", "explain programming", "tell me about programming",
            "programming"
        ],
        "answer": "Programming is the process of writing instructions (code) for computers to perform specific tasks and solve problems."
    },
    "programming_language": {
        "patterns": [
            "what is a programming language", "explain programming language",
            "what is programming language", "tell me about programming language"
        ],
        "answer": "A programming language is a formal set of instructions and syntax used by developers to communicate with computers."
    },
    "algorithm": {
        "patterns": [
            "what is an algorithm", "explain algorithm", "tell me about algorithm",
            "what is algorithm", "algorithm"
        ],
        "answer": "An algorithm is a step-by-step set of instructions or rules designed to solve a specific problem or complete a task."
    }
}


def search_knowledge_base(user_input):
    """
    Searches the KNOWLEDGE_BASE dictionary for a matching question or topic pattern.
    
    Parameters:
        user_input (str): Cleaned user input.
        
    Returns:
        str or None: The answer if a match is found, otherwise None.
    """
    clean_input = user_input.strip().rstrip("?.!")

    # Direct exact pattern match
    for topic, item in KNOWLEDGE_BASE.items():
        if clean_input in item["patterns"]:
            return item["answer"]

    # Substring pattern match (longest pattern first)
    all_patterns = []
    for topic, item in KNOWLEDGE_BASE.items():
        for pattern in item["patterns"]:
            all_patterns.append((pattern, item["answer"]))

    all_patterns.sort(key=lambda x: len(x[0]), reverse=True)

    for pattern, answer in all_patterns:
        if pattern in clean_input:
            return answer

    return None


# ==============================================================================
# FEATURE 2: NAME MEMORY HANDLING
# ==============================================================================
def handle_name_memory(user_input, raw_input, user_name):
    """
    Detects if the user is introducing themselves or asking for their remembered name.
    """
    clean_input = user_input.strip().rstrip("?.!")

    if clean_input in ["what is my name", "do you know my name", "who am i", "what's my name"]:
        if user_name:
            return f"StudyMate: Your name is {user_name}!", user_name
        else:
            return "StudyMate: I don't know your name yet! You can tell me by typing 'My name is [Your Name]'.", user_name

    if clean_input.startswith("my name is "):
        extracted = raw_input.strip()[11:].strip().rstrip("?.!").title()
        if extracted:
            user_name = extracted
            return f"StudyMate: Nice to meet you, {user_name}!", user_name

    elif clean_input.startswith("call me "):
        extracted = raw_input.strip()[8:].strip().rstrip("?.!").title()
        if extracted:
            user_name = extracted
            return f"StudyMate: Got it! I will call you {user_name}.", user_name

    elif clean_input.startswith("i am "):
        ignored_words = ["good", "fine", "ok", "okay", "happy", "sad", "busy", "student", "ready", "learning"]
        if not any(word in clean_input for word in ignored_words):
            extracted = raw_input.strip()[5:].strip().rstrip("?.!").title()
            if extracted and len(extracted.split()) <= 2:
                user_name = extracted
                return f"StudyMate: Nice to meet you, {user_name}!", user_name

    return None, user_name


# ==============================================================================
# FEATURE 3: DATE HANDLING
# ==============================================================================
def handle_date(user_input):
    """
    Returns the current system date formatted nicely (e.g., 4 October 2026).
    """
    date_queries = [
        "what is today's date", "what is the date", "today's date",
        "tell me today's date", "date", "today date", "what's today's date",
        "what is todays date", "todays date"
    ]
    clean_input = user_input.strip().rstrip("?.!")
    if any(query in clean_input for query in date_queries):
        now = datetime.now()
        formatted_date = f"{now.day} {now.strftime('%B %Y')}"
        return f"StudyMate: Today's date is {formatted_date}."
    return None


# ==============================================================================
# FEATURE 4: TIME HANDLING
# ==============================================================================
def handle_time(user_input):
    """
    Returns the current system time formatted in 12-hour format with AM/PM (e.g., 10:30 PM).
    """
    time_queries = [
        "what is the time", "what time is it", "current time",
        "tell me the time", "time", "what's the time"
    ]
    clean_input = user_input.strip().rstrip("?.!")
    if any(query in clean_input for query in time_queries):
        now = datetime.now()
        formatted_time = now.strftime("%I:%M %p").lstrip('0')
        return f"StudyMate: The current time is {formatted_time}."
    return None


# ==============================================================================
# FEATURE 5: SAFE BASIC CALCULATOR
# ==============================================================================
def safe_calculate(expression):
    """
    Safely calculates simple mathematical expressions (+, -, *, /) without unrestricted eval().
    
    Returns:
        tuple: (result_string, is_success)
    """
    expr = expression.strip()
    
    # Identify the operator (skip leading sign if present)
    operator = None
    op_index = -1
    start_index = 1 if (expr.startswith("-") or expr.startswith("+")) else 0

    for i in range(start_index, len(expr)):
        if expr[i] in ["+", "-", "*", "/"]:
            operator = expr[i]
            op_index = i
            break
            
    if not operator or op_index == -1:
        return "Invalid expression for calculator. Please use format like 'calculate 25 + 30'.", False

    # Split operands around operator
    part1 = expr[:op_index].strip()
    part2 = expr[op_index + 1:].strip()

    try:
        num1 = float(part1)
        num2 = float(part2)
    except ValueError:
        return "Invalid expression for calculator. Please use format like 'calculate 25 + 30'.", False

    if operator == "+":
        res = num1 + num2
    elif operator == "-":
        res = num1 - num2
    elif operator == "*":
        res = num1 * num2
    elif operator == "/":
        if num2 == 0:
            return "Sorry, division by zero is not allowed.", False
        res = num1 / num2
    else:
        return "Invalid expression for calculator. Please use format like 'calculate 25 + 30'.", False

    # Format result as int if whole number, else float
    if res.is_integer():
        res_str = str(int(res))
    else:
        res_str = str(round(res, 4))

    return f"The result is {res_str}.", True


def handle_calculator(user_input):
    """
    Detects calculator requests and passes the math expression to safe_calculate.
    """
    clean_text = user_input.strip().rstrip("?.!")

    # Triggered by 'calculate ...' or 'calc ...'
    if clean_text.startswith("calculate") or clean_text.startswith("calc"):
        if clean_text in ["calculate", "calc"]:
            return "StudyMate: Please specify an expression to calculate (e.g., 'calculate 25 + 30')."
        prefix_len = 10 if clean_text.startswith("calculate ") else (5 if clean_text.startswith("calc ") else 0)
        if prefix_len > 0:
            expr = clean_text[prefix_len:].strip()
            result_msg, _ = safe_calculate(expr)
            return f"StudyMate: {result_msg}"

    # Handle direct arithmetic expressions like '25 + 30', '20 / 4', '6 * 7', '20 - 8'
    if any(op in clean_text for op in ["+", "-", "*", "/"]) and any(char.isdigit() for char in clean_text):
        words = clean_text.split()
        if len(words) <= 5 and not any(w in clean_text for w in ["what", "how", "who", "why", "tell", "explain", "date", "time"]):
            result_msg, is_success = safe_calculate(clean_text)
            if is_success or "division by zero" in result_msg or "Invalid expression" in result_msg:
                return f"StudyMate: {result_msg}"

    return None


# ==============================================================================
# FEATURE 6: HELP COMMAND
# ==============================================================================
def handle_help(user_input, user_name):
    """
    Displays chatbot capabilities and sample questions. Personalized if user_name is set.
    """
    clean_input = user_input.strip().rstrip("?.!")
    if clean_input in ["help", "what can you do", "help me", "options", "menu"]:
        greeting = f"Hello {user_name}! " if user_name else ""
        return (
            f"StudyMate: {greeting}I can help you with:\n\n"
            "1. Python\n"
            "2. DBMS\n"
            "3. HTML\n"
            "4. CSS\n"
            "5. Git and GitHub\n"
            "6. Programming basics\n"
            "7. Date and time\n"
            "8. Calculator\n"
            "9. General conversation\n\n"
            "Example questions:\n"
            "- What is Python?\n"
            "- What is DBMS?\n"
            "- What is GitHub?\n"
            "- What is the time?\n"
            "- What is today's date?\n"
            "- Calculate 25 + 30"
        )
    return None


# ==============================================================================
# PART 4 FEATURE 1 & 2: RANDOMIZED CONVERSATIONAL RESPONSES
# ==============================================================================
def handle_conversational_responses(user_input, user_name):
    """
    Uses Python's random module to return varied responses for greetings and small talk.
    """
    clean_input = user_input.strip().rstrip("?.!")

    # Hello / Hi / Hey
    if clean_input in ["hello", "hi", "hey"]:
        options = [
            f"Hello {user_name}! How can I help you today?" if user_name else "Hello! How can I help you today?",
            f"Hi {user_name}! Nice to see you!" if user_name else "Hi! Nice to see you!",
            f"Hey {user_name}! What would you like to learn today?" if user_name else "Hey! What would you like to learn today?"
        ]
        return f"StudyMate: {random.choice(options)}"

    # Good morning
    if clean_input in ["good morning", "morning"]:
        options = [
            f"Good morning, {user_name}! Hope you have a great day ahead!" if user_name else "Good morning! Hope you have a great and productive day of learning ahead!",
            f"Good morning, {user_name}! Ready to learn something new today?" if user_name else "Good morning! Ready to tackle some questions today?",
            f"Good morning, {user_name}! How can I assist your study session today?" if user_name else "Good morning! How can I assist your study session today?"
        ]
        return f"StudyMate: {random.choice(options)}"

    # Good afternoon
    if clean_input in ["good afternoon", "afternoon"]:
        options = [
            f"Good afternoon, {user_name}! Hope your learning session is going well!" if user_name else "Good afternoon! Hope your learning session is going well!",
            f"Good afternoon, {user_name}! How can I assist you with your studies right now?" if user_name else "Good afternoon! How can I assist you with your studies today?",
            f"Good afternoon, {user_name}! Ready to continue studying?" if user_name else "Good afternoon! Ready to continue studying?"
        ]
        return f"StudyMate: {random.choice(options)}"

    # Good evening
    if clean_input in ["good evening", "evening"]:
        options = [
            f"Good evening, {user_name}! Welcome back. What can I help you with tonight?" if user_name else "Good evening! Welcome back. What can I help you with tonight?",
            f"Good evening, {user_name}! Hope you had a fruitful day! Ready to review?" if user_name else "Good evening! Hope you had a fruitful day! Ready to study?",
            f"Good evening, {user_name}! How can I assist your learning tonight?" if user_name else "Good evening! How can I assist your learning tonight?"
        ]
        return f"StudyMate: {random.choice(options)}"

    # How are you
    if clean_input in ["how are you", "how are you doing", "how's it going"]:
        options = [
            f"I'm doing great, {user_name}! Ready to assist you with your learning." if user_name else "I'm doing great, thank you! Ready to assist you with your learning.",
            f"I'm functioning perfectly and ready for your questions, {user_name}!" if user_name else "I'm functioning perfectly and ready to answer your questions!",
            f"Doing fantastic, {user_name}! How are your studies coming along?" if user_name else "Doing fantastic! How are your studies coming along?"
        ]
        return f"StudyMate: {random.choice(options)}"

    # Thank you / Thanks
    if clean_input in ["thank you", "thanks", "thank you so much", "thanks a lot"]:
        options = [
            f"You're very welcome, {user_name}! Let me know if you need anything else." if user_name else "You're very welcome! Let me know if you need anything else.",
            f"Happy to help, {user_name}! Keep up the great work!" if user_name else "Happy to help! Keep up the great work!",
            f"Anytime, {user_name}! Feel free to ask more questions whenever you like." if user_name else "Anytime! Feel free to ask more questions whenever you like."
        ]
        return f"StudyMate: {random.choice(options)}"

    # What is your name
    if clean_input in ["what is your name", "what's your name", "who are you"]:
        if user_name:
            return f"StudyMate: My name is StudyMate! I'm glad to assist you, {user_name}."
        return "StudyMate: My name is StudyMate, your student chatbot assistant!"

    return None


# ==============================================================================
# PART 4 FEATURE 6: IMPROVED FALLBACK RESPONSE
# ==============================================================================
def handle_fallback(user_name):
    """
    Returns an informative, helpful fallback response when user input is unrecognized.
    """
    name_str = f" {user_name}" if user_name else ""
    return (
        f"StudyMate: Sorry{name_str}, I don't have an answer for that topic yet. "
        "You can ask me about Python, DBMS, HTML, CSS, Git, GitHub, programming basics, "
        "date, time, or calculator. Type 'help' to see sample questions!"
    )


# ==============================================================================
# PART 4 FEATURE 4: LOCAL CHAT HISTORY LOGGING
# ==============================================================================
def save_chat_history(user_msg, bot_resp, filename="chat_history.txt"):
    """
    Appends the conversation turn (timestamp, user message, bot response) to a text file.
    Handles file errors gracefully.
    """
    try:
        timestamp = datetime.now().strftime("[%I:%M:%S %p]")
        with open(filename, "a", encoding="utf-8") as f:
            f.write(f"{timestamp}\nYou: {user_msg}\n{bot_resp}\n\n")
    except Exception as e:
        print(f"[Warning: Could not save chat history to {filename}: {e}]")


# ==============================================================================
# MAIN RESPONSE HANDLER (Combining Parts 1, 2, 3 & 4)
# ==============================================================================
def get_response(user_input, raw_input, user_name):
    """
    Processes normalized user input through exit checks, help, name memory, date, time,
    calculator, randomized conversational responses, knowledge base lookup, and fallback.
    
    Returns:
        tuple: (response_str, updated_user_name)
    """
    clean_input = user_input.strip().rstrip("?.!")

    # 1. Input Validation: Handle empty or whitespace input
    if not clean_input:
        return "StudyMate: Please enter a message or question!", user_name

    # 2. Exit Commands (Part 1)
    if clean_input in ["bye", "exit", "quit"]:
        if user_name:
            return f"StudyMate: Goodbye {user_name}! Good luck with your studies!", user_name
        return "StudyMate: Goodbye! Good luck with your studies!", user_name

    # 3. Help Command (Part 3)
    help_response = handle_help(user_input, user_name)
    if help_response:
        return help_response, user_name

    # 4. Name Memory Handler (Part 2)
    name_response, user_name = handle_name_memory(user_input, raw_input, user_name)
    if name_response:
        return name_response, user_name

    # 5. Date Feature Handler (Part 3)
    date_response = handle_date(user_input)
    if date_response:
        return date_response, user_name

    # 6. Time Feature Handler (Part 3)
    time_response = handle_time(user_input)
    if time_response:
        return time_response, user_name

    # 7. Calculator Feature Handler (Part 3)
    calc_response = handle_calculator(user_input)
    if calc_response:
        return calc_response, user_name

    # 8. Conversational & Greeting Responses (Part 4 Randomized)
    conv_response = handle_conversational_responses(user_input, user_name)
    if conv_response:
        return conv_response, user_name

    # 9. Student Knowledge Base Lookup (Part 2 & 4 Expanded)
    kb_answer = search_knowledge_base(user_input)
    if kb_answer:
        return f"StudyMate: {kb_answer}", user_name

    # 10. Improved Fallback Response for unrecognized input (Part 4)
    fallback_resp = handle_fallback(user_name)
    return fallback_resp, user_name


def main():
    """
    Main loop to execute the rule-based chatbot program.
    """
    user_name = None

    print("==================================================")
    print("      Welcome to StudyMate Student Chatbot!       ")
    print("==================================================")
    print("Ask me basic educational concepts (Python, DBMS, HTML, CSS, Git, Programming)!")
    print("Try asking for 'date', 'time', 'calculate 25 + 30', or type 'help'!")
    print("Type 'bye', 'exit', or 'quit' to end the conversation.\n")

    while True:
        try:
            raw_input = input("You: ")
        except (KeyboardInterrupt, EOFError):
            print("\nStudyMate: Goodbye! Good luck with your studies!")
            break

        user_input = raw_input.strip().lower()

        # Input Validation for empty/whitespace input
        if not user_input:
            resp = "StudyMate: Please enter a message or question!"
            print(resp)
            save_chat_history(raw_input if raw_input else "[empty]", resp)
            continue

        response, user_name = get_response(user_input, raw_input, user_name)
        print(response)

        # Save to local chat history file
        save_chat_history(raw_input, response)

        if user_input.rstrip("?.!") in ["bye", "exit", "quit"]:
            break


# Script Entry Point
if __name__ == "__main__":
    main()
