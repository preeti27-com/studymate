"""
StudyMate - Automated Unit Test Suite
CodeAlpha Internship Project

Tests core chatbot functionality including:
- Knowledge base query matching (Python, DBMS, HTML, CSS, Git, Programming)
- Safe arithmetic calculator and error handling (division by zero, negative numbers)
- Live date and time retrieval
- Session name memory and recall
- Greetings, small talk, and help system
- Graceful fallback for unrecognized queries
"""

import unittest
from datetime import datetime
import chatbot


class TestStudyMateKnowledgeBase(unittest.TestCase):
    """Tests knowledge base retrieval across core topics."""

    def test_python_topic(self):
        answer = chatbot.search_knowledge_base("what is python")
        self.assertIsNotNone(answer)
        self.assertIn("Python is a high-level", answer)

    def test_dbms_topic(self):
        answer = chatbot.search_knowledge_base("what is dbms")
        self.assertIsNotNone(answer)
        self.assertIn("DBMS (Database Management System)", answer)

    def test_sql_topic(self):
        answer = chatbot.search_knowledge_base("explain sql")
        self.assertIsNotNone(answer)
        self.assertIn("SQL", answer)

    def test_html_topic(self):
        answer = chatbot.search_knowledge_base("what is html")
        self.assertIsNotNone(answer)
        self.assertIn("HyperText Markup Language", answer)

    def test_css_topic(self):
        answer = chatbot.search_knowledge_base("why use css")
        self.assertIsNotNone(answer)
        self.assertIn("CSS is used to separate web content", answer)

    def test_git_github_topics(self):
        git_ans = chatbot.search_knowledge_base("what is git")
        github_ans = chatbot.search_knowledge_base("what is github")
        self.assertIn("distributed version control system", git_ans)
        self.assertIn("cloud-based hosting platform", github_ans)

    def test_algorithm_topic(self):
        answer = chatbot.search_knowledge_base("what is an algorithm")
        self.assertIsNotNone(answer)
        self.assertIn("step-by-step set of instructions", answer)


class TestStudyMateCalculator(unittest.TestCase):
    """Tests safe calculator functions, division by zero, and negative values."""

    def test_addition(self):
        res, ok = chatbot.safe_calculate("25 + 30")
        self.assertTrue(ok)
        self.assertEqual(res, "The result is 55.")

    def test_subtraction(self):
        res, ok = chatbot.safe_calculate("20 - 8")
        self.assertTrue(ok)
        self.assertEqual(res, "The result is 12.")

    def test_multiplication(self):
        res, ok = chatbot.safe_calculate("6 * 7")
        self.assertTrue(ok)
        self.assertEqual(res, "The result is 42.")

    def test_division(self):
        res, ok = chatbot.safe_calculate("20 / 4")
        self.assertTrue(ok)
        self.assertEqual(res, "The result is 5.")

    def test_division_by_zero(self):
        res, ok = chatbot.safe_calculate("10 / 0")
        self.assertFalse(ok)
        self.assertEqual(res, "Sorry, division by zero is not allowed.")

    def test_negative_numbers(self):
        res, ok = chatbot.safe_calculate("-5 - 10")
        self.assertTrue(ok)
        self.assertEqual(res, "The result is -15.")

    def test_calculator_handler(self):
        resp = chatbot.handle_calculator("calculate 15 + 15")
        self.assertIn("The result is 30.", resp)


class TestStudyMateDateTime(unittest.TestCase):
    """Tests date and time handling."""

    def test_date_handler(self):
        resp = chatbot.handle_date("what is today's date")
        self.assertIsNotNone(resp)
        self.assertIn("Today's date is", resp)
        self.assertIn(str(datetime.now().year), resp)

    def test_time_handler(self):
        resp = chatbot.handle_time("what is the time")
        self.assertIsNotNone(resp)
        self.assertIn("The current time is", resp)


class TestStudyMateNameMemory(unittest.TestCase):
    """Tests user name introduction, storage, and recall."""

    def test_unknown_name_query(self):
        resp, name = chatbot.handle_name_memory("what is my name", "what is my name", None)
        self.assertIn("I don't know your name yet", resp)
        self.assertIsNone(name)

    def test_name_introduction(self):
        resp, name = chatbot.handle_name_memory("my name is preeti", "My name is Preeti", None)
        self.assertEqual(name, "Preeti")
        self.assertIn("Nice to meet you, Preeti!", resp)

    def test_remembered_name_query(self):
        resp, name = chatbot.handle_name_memory("what is my name", "what is my name", "Preeti")
        self.assertEqual(name, "Preeti")
        self.assertIn("Your name is Preeti!", resp)

    def test_call_me_pattern(self):
        resp, name = chatbot.handle_name_memory("call me alex", "call me Alex", None)
        self.assertEqual(name, "Alex")
        self.assertIn("I will call you Alex.", resp)


class TestStudyMateConversationFlow(unittest.TestCase):
    """Tests exit commands, help menu, conversational greetings, and fallback."""

    def test_empty_input(self):
        resp, _ = chatbot.get_response("", "", None)
        self.assertIn("Please enter a message or question!", resp)

    def test_exit_command(self):
        resp, _ = chatbot.get_response("bye", "bye", None)
        self.assertIn("Goodbye!", resp)

    def test_help_command(self):
        resp, _ = chatbot.get_response("help", "help", "Preeti")
        self.assertIn("Hello Preeti!", resp)
        self.assertIn("I can help you with", resp)

    def test_greeting(self):
        resp, _ = chatbot.get_response("hello", "hello", "Preeti")
        self.assertIn("Preeti", resp)

    def test_fallback(self):
        resp, _ = chatbot.get_response("random unknown query 123", "random unknown query 123", None)
        self.assertIn("Sorry, I don't have an answer for that topic yet", resp)


if __name__ == "__main__":
    unittest.main()
