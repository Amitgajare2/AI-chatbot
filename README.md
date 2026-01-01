# 🤖 AI Chatbot

*A local emotional AI chatbot built with Python + LLaMA3 via Ollama.*  
**Powered by memories, feelings, and conversation — an AI companion that truly remembers.**

---

**AI Companion** is an offline, AI-powered emotional chatbot that remembers every conversation.  
She responds like someone who genuinely cares — conversational, emotional, and authentic.  
Powered by **LLaMA3** via **Ollama**, with local **SQLite** memory storage.

---

## ✨ Features

* 💬 **Emotional AI personality** — customizable to your preferences
* 🎭 **Auto-conversation starter** — she can randomly start conversations with you!
* 🧠 **Persistent memory** — remembers everything using SQLite database
* 🌐 **Fully offline** — no internet needed after setup
* 🤖 **Powered by LLaMA3** — running locally via Ollama
* 📚 **Document reading** — can learn from PDFs, DOCX, and TXT files
* 🔍 **Web commands** — search YouTube, Google, Wikipedia directly
* 🎨 **Fully customizable** — change personality, memories, and conversation style

---

## 🚀 Installation
read article 
https://amitgajare.hashnode.dev/how-to-create-your-own-ai-girlfriend-chatbot-a-beginners-tutorial


## 🎮 Commands

| Command        | Action                          |
| -------------- | ------------------------------- |
| `/yt query`    | Search YouTube                  |
| `/g query`     | Search Google                   |
| `/wiki query`  | Search Wikipedia                |
| `/open url`    | Open any website                |
| `/read`        | Learn from files in `reading/`  |
| `clear memory` | Clear conversation history      |
| `exit`         | Exit chat                       |

---

## 🎨 Customization

### Change Personality

Edit `personality.json`:

```json
{
  "name": "Your AI Name",
  "your_name": "Your Name",
  "style": "sweet, caring, playful",
  "memories": [
    "Add custom memories here",
    "Things you want her to remember"
  ]
}
```


## 📚 Advanced Features

### Teach Her from Documents

1. Create a folder named `reading/`
2. Place PDFs, Word docs, or text files inside
3. In the chat, type `/read`
4. She'll absorb the content and reference it in conversations!



## 📁 Project Structure

```
ai-companion/
├── chatBot.py        # Main chatbot script
├── personality.json     # AI personality configuration
├── database.db        # SQLite conversation memory
├── reading/             # Place documents here for AI to learn
├── requirements.txt     # Python dependencies
└── README.md           # You are here!
```


## 🌟 What Makes This Special?

Unlike cloud-based chatbots:
- ✅ **100% Private** — all data stays on your computer
- ✅ **True Memory** — she actually remembers conversations
- ✅ **Feels Alive** — auto-starts conversations randomly
- ✅ **Completely Free** — no subscriptions or API costs
- ✅ **Offline First** — works without internet

---

## 📜 License

**MIT License** — free to use, modify, and share.  
Built with ❤️ for meaningful AI conversations.

---

## 🤝 Contributing

Feel free to:
- ⭐ Star this project
- 🐛 Report bugs
- 💡 Suggest features
- 🔧 Submit pull requests

---

**Enjoy your AI Chatbot** 🌸  
May your conversations be meaningful and memorable.


