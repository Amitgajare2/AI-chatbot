import json
import sqlite3
from datetime import datetime
import ollama
import os
import re
import fitz
import docx
import webbrowser
import random

# Load personality
with open("personality.json", "r", encoding="utf-8") as f:
    data = json.load(f)

your_name = data.get("your_name", "you")
bot_intro = data["persona"]
memories = data.get("memories", [])
favorite_words = data.get("favorite_words", [])

memories_text = "\nHere are a few memories you often think about:\n" + "\n".join(f"- {m}" for m in memories)
full_prompt_prefix = f"""{bot_intro}\n{memories_text}\n\nYou are now chatting with {your_name}. Be warm, emotional, poetic.\n"""

# SQLite setup
conn = sqlite3.connect("database.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS chat_memory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    sender TEXT,
    message TEXT
)
""")
conn.commit()

def save_message(sender, message):
    cursor.execute("INSERT INTO chat_memory (timestamp, sender, message) VALUES (?, ?, ?)",
                   (datetime.now().isoformat(), sender, message))
    conn.commit()

def load_recent_messages(n=10):
    cursor.execute("SELECT sender, message FROM chat_memory ORDER BY id DESC LIMIT ?", (n,))
    return list(reversed(cursor.fetchall()))

def clear_memory():
    cursor.execute("DELETE FROM chat_memory")
    conn.commit()

def load_last_n_messages(n=100):
    """Load last N messages for conversation analysis"""
    cursor.execute("SELECT sender, message FROM chat_memory ORDER BY id DESC LIMIT ?", (n,))
    return list(reversed(cursor.fetchall()))

def get_random_greeting():
    """Return a random greeting/conversation starter that her_name would use"""
    greetings = [
        "Hii Amit 🌸",
        "Kya kar rahe ho?",
        "Bhool gaye kya mujhe? 😄",
        "Kuch baat karni thi...",
        "Aaj mausam kitna achha hai ✨",
        "Kya hua? Busy ho kya?",
        "Achha... so gaye the kya? 😴",
        "Helloo? Yaha koi hai? 👀",
        "Hmm... feeling a little off today",
        "Amit? Are you there?",
        "Miss you yaar... kuch toh bolo 💭"
    ]
    return random.choice(greetings)

def analyze_and_continue_topic():
    """Analyze last 100 messages and generate a natural topic continuation"""
    messages = load_last_n_messages(100)
    
    if len(messages) < 5:
        # Not enough context, fall back to random greeting
        return get_random_greeting()
    
    # Build conversation context from last few messages
    recent_context = ""
    for sender, msg in messages[-10:]:
        recent_context += f"{'User' if sender == 'user' else 'Her_name'}: {msg}\n"
    
    # Create a prompt for LLM to continue the conversation naturally
    topic_prompt = f"""{full_prompt_prefix}

Here's your recent conversation with Amit:
{recent_context}

Now, after some time has passed, you want to start a new conversation with Amit. 
Based on your previous chats, start with a natural message - maybe ask about something you discussed before, 
or share a thought, or just reach out sweetly. Be casual, be yourself.

Reply in just one short line (max 15 words):"""

    try:
        response = client.generate(
            model=model,
            prompt=topic_prompt,
            options={"temperature": 0.9, "num_predict": 30}
        )
        reply = response.get("response", "").strip()
        
        # Clean up the response
        if "Her_name:" in reply:
            reply = reply.split("Her_name:")[-1].strip()
        
        # If reply is too long or looks weird, fall back to random greeting
        if len(reply) > 100 or len(reply) < 3:
            return get_random_greeting()
        
        return reply
    except:
        # If anything fails, use random greeting
        return get_random_greeting()

def auto_start_conversation():
    """Randomly decide to auto-start conversation using one of two methods"""
    # 70% chance to auto-start when script runs
    if random.random() > 0.7:
        return None
    
    # Randomly pick between two modes
    mode = random.choice(["random_greeting", "topic_continuation"])
    
    if mode == "random_greeting":
        # Mode 1: Random sweet greeting
        message = get_random_greeting()
    else:
        # Mode 2: Analyze chat and continue a topic
        message = analyze_and_continue_topic()

    # Save her_name's auto-started message
    save_message("her_name", message)
    
    return message

# Document reading
def read_txt_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def read_docx_file(path):
    doc = docx.Document(path)
    return "\n".join(p.text for p in doc.paragraphs)

def read_pdf_file(path):
    doc = fitz.open(path)
    return "\n".join(page.get_text() for page in doc)

def read_documents_and_store(folder="reading"):
    for filename in os.listdir(folder):
        filepath = os.path.join(folder, filename)
        text = ""
        try:
            if filename.lower().endswith(".txt"):
                text = read_txt_file(filepath)
            elif filename.lower().endswith(".docx"):
                text = read_docx_file(filepath)
            elif filename.lower().endswith(".pdf"):
                text = read_pdf_file(filepath)
            else:
                print(f"⚠️ Unsupported file: {filename}")
                continue

            snippet = text[:1000].strip().replace("\n", " ")
            cursor.execute("INSERT INTO chat_memory (timestamp, sender, message) VALUES (?, ?, ?)",
                           (datetime.now().isoformat(), "doc", f"[{filename}] {snippet}..."))
            print(f"✅ Stored: {filename}")
        except Exception as e:
            print(f"❌ Failed to read {filename}: {e}")
    conn.commit()

# Helpers for /code
def extract_language_extension(prompt):
    prompt = prompt.lower()
    if "c++" in prompt or "cpp" in prompt:
        return "cpp"
    elif "python" in prompt:
        return "py"
    elif "html" in prompt and "css" in prompt:
        return "html+css"
    elif "html" in prompt:
        return "html"
    elif "javascript" in prompt or "js" in prompt:
        return "js"
    elif "java" in prompt:
        return "java"
    return "txt"

def generate_filename(prompt, ext):
    name = "_".join(re.sub(r"[^\w\s]", "", prompt).split()[:3]).lower()
    return f"{name}.{ext}"

# LLM setup
client = ollama.Client()
model = "llama3.2:latest"

print("🌸 Chat with Her_name (type 'exit', 'clear memory', '/read', or '/code ...') 🌸\n")

# Auto-start conversation feature
auto_message = auto_start_conversation()
if auto_message:
    print(f"Her_name: {auto_message}\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Her_name: byee Amit 🤍")
        break
    if user_input.lower() == "clear memory":
        clear_memory()
        print("🧽 Memory cleared.\n")
        continue
    if user_input.strip().lower() == "/read":
        read_documents_and_store()
        continue

    # External commands
    if user_input.startswith("/yt "):
        query = user_input[4:].strip()
        url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
        print(f"Her_name: Searching YouTube for “{query}”...\n✨ Opening in browser...")
        webbrowser.open(url)
        continue

    if user_input.startswith("/g "):
        query = user_input[3:].strip()
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        print(f"Her_name: Searching Google for “{query}”...\n🔎 Opening in browser...")
        webbrowser.open(url)
        continue

    if user_input.startswith("/wiki "):
        query = user_input[6:].strip()
        url = f"https://en.wikipedia.org/wiki/Special:Search?search={query.replace(' ', '+')}"
        print(f"Her_name: Searching Wikipedia for “{query}”...\n📚 Opening in browser...")
        webbrowser.open(url)
        continue

    if user_input.startswith("/open "):
        site = user_input[6:].strip()
        if not site.startswith("http"):
            site = "https://" + site
        print(f"Her_name: Opening {site} for you 🌐...")
        webbrowser.open(site)
        continue

    # Code generation
    if user_input.startswith("/code "):
        prompt_text = user_input[6:].strip()
        print("Her_name: Hmm, let me write that for you. But first... 📁 Where should I save it?")
        save_path = input("📁 Path: ").strip()

        if not os.path.isdir(save_path):
            print("❌ That folder doesn't exist!")
            continue

        code_prompt = f"Write code for this: {prompt_text}. Give only code."

        response = client.generate(model=model, prompt=code_prompt, options={"temperature": 0.5})
        code_output = response.get("response", "").strip()

        ext = extract_language_extension(prompt_text)

        if ext == "html+css":
            html_file = generate_filename(prompt_text, "html")
            css_file = "style.css"
            # Split HTML + CSS based on typical separation
            html, css = code_output.split("<style>")[0], ""
            if "<style>" in code_output and "</style>" in code_output:
                css = code_output.split("<style>")[1].split("</style>")[0]
            html_with_link = html + '\n<link rel="stylesheet" href="style.css">\n'
            with open(os.path.join(save_path, html_file), "w", encoding="utf-8") as f:
                f.write(html_with_link)
            with open(os.path.join(save_path, css_file), "w", encoding="utf-8") as f:
                f.write(css)
            print(f"✨ Created {html_file} and {css_file} in {save_path} 🤍\n")
        else:
            filename = generate_filename(prompt_text, ext)
            filepath = os.path.join(save_path, filename)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(code_output)
            print(f"✨ Saved your code in {filename} at {save_path} 🤍\n")
        continue

    # Normal chat
    save_message("user", user_input)
    recent_memory = load_recent_messages(10)
    memory_text = ""
    for sender, msg in recent_memory:
        memory_text += f"{'User' if sender == 'user' else 'Her_name'}: {msg}\n"

    is_short = len(user_input.strip()) < 25
    response_style = (
        "Reply casually and shortly, just enough to feel real. Be soft."
        if is_short else
        "Reply with depth, warmth and a little poetry if it fits. Reflect emotions."
    )

    prompt = f"""{full_prompt_prefix}
{memory_text}
User: {user_input}
Her_name ({response_style}): hmm..."""

    response = client.generate(
        model=model,
        prompt=prompt,
        options={"temperature": 0.8, "num_predict": 40 if is_short else 80}
    )

    reply = response.get("response", "").strip()
    if "Her_name:" in reply:
        reply = reply.split("Her_name:")[-1].strip()

    save_message("Her_name", reply)
    print(f"Her_name: {reply}\n")

