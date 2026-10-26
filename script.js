/**
 * StudyMate - Handcrafted Web Client
 * Clean, human-friendly interactions with Vercel API and instant offline fallback.
 */

document.addEventListener("DOMContentLoaded", () => {
  const chatForm = document.getElementById("chatForm");
  const userInput = document.getElementById("userInput");
  const messagesContainer = document.getElementById("messagesContainer");
  const chatWindow = document.getElementById("chatWindow");
  const typingIndicator = document.getElementById("typingIndicator");
  const clearChatBtn = document.getElementById("clearChatBtn");
  const quickHelpBtn = document.getElementById("quickHelpBtn");
  const themeToggleBtn = document.getElementById("themeToggleBtn");
  const themeIcon = document.getElementById("themeIcon");
  const topicTags = document.querySelectorAll(".topic-tag");

  let currentUserName = null;

  // ============================================================================
  // Theme Toggle (Defaults to pleasant light mode, remembers user choice)
  // ============================================================================
  const savedTheme = localStorage.getItem("studymate_user_theme") || "light";
  applyTheme(savedTheme);

  function applyTheme(theme) {
    if (theme === "dark") {
      document.body.classList.remove("theme-light");
      document.body.classList.add("theme-dark");
      themeIcon.textContent = "Light";
    } else {
      document.body.classList.remove("theme-dark");
      document.body.classList.add("theme-light");
      themeIcon.textContent = "Dark";
    }
  }

  themeToggleBtn.addEventListener("click", () => {
    const isDark = document.body.classList.contains("theme-dark");
    const newTheme = isDark ? "light" : "dark";
    applyTheme(newTheme);
    localStorage.setItem("studymate_user_theme", newTheme);
  });

  // ============================================================================
  // Time Formatting
  // ============================================================================
  function formatCurrentTime() {
    const now = new Date();
    return now.toLocaleTimeString([], { hour: "numeric", minute: "2-digit" });
  }

  // ============================================================================
  // Message Bubble Rendering (Human Style with Avatars & Copy Option)
  // ============================================================================
  function appendBubble(senderText, messageText, isUser = false) {
    const row = document.createElement("div");
    row.className = `chat-bubble-row ${isUser ? "user-side" : "bot-side"}`;

    const avatar = document.createElement("div");
    avatar.className = "sender-mini-avatar";
    avatar.textContent = isUser ? "👤" : "SM";

    const contentBlock = document.createElement("div");
    contentBlock.className = "bubble-content-block";

    const senderLabel = document.createElement("span");
    senderLabel.className = "bubble-sender-name";
    senderLabel.textContent = isUser ? (currentUserName || "You") : "StudyMate";

    const card = document.createElement("div");
    card.className = "bubble-card";
    card.textContent = messageText;

    const footer = document.createElement("div");
    footer.className = "bubble-footer";

    const time = document.createElement("span");
    time.className = "bubble-time";
    time.textContent = formatCurrentTime();
    footer.appendChild(time);

    // Add Copy button for bot answers
    if (!isUser) {
      const copyBtn = document.createElement("button");
      copyBtn.className = "copy-button";
      copyBtn.textContent = "Copy";
      copyBtn.addEventListener("click", () => {
        navigator.clipboard.writeText(messageText);
        copyBtn.textContent = "Copied! ✓";
        setTimeout(() => {
          copyBtn.textContent = "Copy";
        }, 1500);
      });
      footer.appendChild(copyBtn);
    }

    contentBlock.appendChild(senderLabel);
    contentBlock.appendChild(card);
    contentBlock.appendChild(footer);

    row.appendChild(avatar);
    row.appendChild(contentBlock);

    messagesContainer.appendChild(row);
    scrollToBottom();
  }

  function scrollToBottom() {
    setTimeout(() => {
      chatWindow.scrollTop = chatWindow.scrollHeight;
    }, 40);
  }

  function showTyping() {
    typingIndicator.style.display = "flex";
    scrollToBottom();
  }

  function hideTyping() {
    typingIndicator.style.display = "none";
  }

  // ============================================================================
  // Quick Topics Button & Reset
  // ============================================================================
  if (quickHelpBtn) {
    quickHelpBtn.addEventListener("click", () => {
      processMessage("help");
    });
  }

  clearChatBtn.addEventListener("click", () => {
    messagesContainer.innerHTML = "";
    appendBubble("StudyMate", "Chat reset! Ready whenever you are. What would you like to review?");
  });

  // ============================================================================
  // Topic Tags Click
  // ============================================================================
  topicTags.forEach((tag) => {
    tag.addEventListener("click", () => {
      const query = tag.getAttribute("data-query");
      if (query) {
        processMessage(query);
      }
    });
  });

  // ============================================================================
  // Form Submission
  // ============================================================================
  chatForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const raw = userInput.value.trim();
    if (!raw) return;
    userInput.value = "";
    processMessage(raw);
  });

  async function processMessage(rawText) {
    appendBubble("You", rawText, true);
    showTyping();

    try {
      // POST to Vercel Serverless Function
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: rawText,
          user_name: currentUserName
        })
      });

      if (!res.ok) {
        throw new Error(`API responded with ${res.status}`);
      }

      const data = await res.json();
      hideTyping();

      if (data.user_name) {
        currentUserName = data.user_name;
      }

      appendBubble("StudyMate", data.response || "No response received.");
    } catch (err) {
      // Offline fallback: Use local knowledge base simulation
      setTimeout(() => {
        hideTyping();
        const fallbackText = getOfflineResponse(rawText);
        appendBubble("StudyMate", fallbackText);
      }, 300);
    }
  }

  // ============================================================================
  // Offline Engine (Matching chatbot.py logic)
  // ============================================================================
  function getOfflineResponse(rawText) {
    const text = rawText.trim().toLowerCase().replace(/[?!.]+$/, "");

    if (!text) return "Please enter a question or topic to study!";
    if (["bye", "exit", "quit"].includes(text)) {
      return currentUserName ? `Goodbye ${currentUserName}! Good luck with your studies!` : "Goodbye! Good luck with your studies!";
    }
    if (["help", "menu", "options", "what can you do"].includes(text)) {
      const greet = currentUserName ? `Hello ${currentUserName}! ` : "";
      return `${greet}I can help you review:\n• Python (variables, loops, functions, lists)\n• DBMS & SQL (normalization, primary keys)\n• HTML & CSS (tags, selectors, layouts)\n• Git & GitHub (repositories, pushing)\n• Safe Math calculations (e.g., 25 + 30)\n• Current date & time\n\nFeel free to ask any question!`;
    }

    // Name memory
    if (text.startsWith("my name is ")) {
      currentUserName = rawText.trim().slice(11).replace(/[?!.]+$/, "");
      return `Nice to meet you, ${currentUserName}! I'll remember that.`;
    }
    if (text.startsWith("call me ")) {
      currentUserName = rawText.trim().slice(8).replace(/[?!.]+$/, "");
      return `Got it! I will call you ${currentUserName}.`;
    }
    if (["what is my name", "who am i", "do you know my name"].includes(text)) {
      return currentUserName ? `Your name is ${currentUserName}!` : "I don't know your name yet! You can tell me by typing 'My name is [Name]'.";
    }

    // Date & Time
    if (text.includes("date")) {
      const d = new Date();
      return `Today's date is ${d.toLocaleDateString("en-US", { day: "numeric", month: "long", year: "numeric" })}.`;
    }
    if (text.includes("time")) {
      return `The current time is ${formatCurrentTime()}.`;
    }

    // Safe Math
    const calcMatch = rawText.match(/(-?\d+(?:\.\d+)?)\s*([\+\-\*\/])\s*(-?\d+(?:\.\d+)?)/);
    if (calcMatch) {
      const n1 = parseFloat(calcMatch[1]);
      const op = calcMatch[2];
      const n2 = parseFloat(calcMatch[3]);
      if (op === "/" && n2 === 0) return "Sorry, division by zero is not allowed.";
      const res = op === "+" ? n1 + n2 : op === "-" ? n1 - n2 : op === "*" ? n1 * n2 : n1 / n2;
      return `The result is ${res}.`;
    }

    // Knowledge Base matching
    if (text.includes("python")) return "Python is a high-level, interpreted programming language known for its easy-to-read syntax and versatility.";
    if (text.includes("variable")) return "A variable is a reserved memory location used to store values or data in a program.";
    if (text.includes("function")) return "A function is a reusable block of code designed to perform a specific task when called.";
    if (text.includes("loop")) return "A loop is a control structure used to repeat a block of code multiple times as long as a specified condition is met.";
    if (text.includes("list")) return "A list is an ordered, mutable collection of items in Python enclosed in square brackets [].";
    if (text.includes("dbms")) return "DBMS (Database Management System) is software used to store, manage, retrieve, and organize data efficiently.";
    if (text.includes("sql")) return "SQL (Structured Query Language) is the standard language used to communicate with and manipulate relational databases.";
    if (text.includes("primary key")) return "A primary key is a unique identifier assigned to each record in a database table. It cannot contain null values.";
    if (text.includes("normalization")) return "Normalization is the process of organizing data in a database to reduce data redundancy and improve data integrity.";
    if (text.includes("html")) return "HTML (HyperText Markup Language) is the standard markup language used to structure web pages and their content.";
    if (text.includes("css")) return "CSS (Cascading Style Sheets) is used to separate web content from visual presentation, making websites attractive and responsive.";
    if (text.includes("git") && !text.includes("github")) return "Git is a distributed version control system that tracks changes in source code during software development.";
    if (text.includes("github")) return "GitHub is a cloud-based hosting platform that lets developers store, manage, and collaborate on Git repositories.";
    if (text.includes("algorithm")) return "An algorithm is a step-by-step set of instructions or rules designed to solve a specific problem or complete a task.";

    // Greetings
    if (["hello", "hi", "hey"].includes(text)) return currentUserName ? `Hello ${currentUserName}! Ready to learn something today?` : "Hello! Ready to learn something today?";
    if (text.includes("good morning")) return currentUserName ? `Good morning, ${currentUserName}! Hope you have a productive study session!` : "Good morning! Hope you have a productive study session!";
    if (text.includes("good afternoon")) return "Good afternoon! Hope your learning session is going well!";
    if (text.includes("good evening")) return "Good evening! Welcome back. What can I help you review tonight?";
    if (text.includes("how are you")) return "I'm doing great, thank you! Ready to assist you with your learning.";
    if (text.includes("thank")) return "You're very welcome! Keep up the great work.";

    return "Sorry, I don't have an answer for that topic yet. You can ask me about Python, DBMS, HTML, CSS, Git, GitHub, date, time, or calculator. Type 'help' to see sample questions!";
  }
});
