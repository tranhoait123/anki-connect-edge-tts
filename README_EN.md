# 🎧 Anki Connect Edge TTS - Auto Audio Generator for Anki

A powerful, simple, and optimized application for batch generating Text-to-Speech (TTS) for Anki cards using Microsoft Edge TTS technology. Specifically designed for Medical students and language learners.

> **Made with ❤️ by PonZ**
>
> [Tiếng Việt (README.md)](./README.md)

---

## 🌟 Concept & Inspiration

This project was born from the practical need to master the vast amount of knowledge in Medical school. Listening to audio helps memory retention significantly, but existing tools were often complex or sounded robotic.

**Inspiration:** This project is inspired by and inherits ideas from [msjsc001/Anki-TTS-Edge](https://github.com/msjsc001/Anki-TTS-Edge). I rebuilt it with a modern Streamlit interface, added smart filters specifically for medical terminology, and created a more intuitive deck management system.

---

## ✨ Key Features

- **🚀 Smart Scanning & Management**:
  - **Scan Status**: Instantly see which Deck/Tag is missing audio. Generates a report with total cards, cards with audio, and cards without.
  - **Smart Fill**: Generate audio only for empty cards (saves time, avoids duplicates).
  - **Clear Audio**: Wipe the data field clean in one click to restart.
- **🩺 Medical & Language Optimization**:
  - **Abbreviation Expansion**: Automatically decodes abbreviations (e.g., `PT` -> `Patient`, `HTN` -> `Hypertension`). You can customize your own abbreviation list directly in the UI.
  - **Text Cleaning**: Automatically removes clutter: Emojis, citation numbers like `[1]`, hidden characters that break audio, HTML tags, etc.
- **🗣️ Advanced Audio Technology**:
  - **SSML Advanced**: Uses a Male voice for questions and a Female voice for answers, with a professional 1-second pause between fields.
  - **Simple Mode (Tag-Free)**: Sends plain text to Microsoft servers. Guaranteed 100% stability, never accidentally reads XML source code.
  - **Speed Control**: Adjust reading speed from 0.5x to 1.5x (default 0.9x for better comprehension of complex content).
- **🎨 Streamlit UI**: Operates directly in your browser, intuitive, and supports auto-saving all settings for future use.

---

## 🛠️ Installation Guide

### 1. System Requirements

- **Python 3.9** or higher installed on your computer.
- **Anki** must be open while using the application.

### 2. Install AnkiConnect (Required)

This app communicates with Anki via the **AnkiConnect** plugin.

1. Open Anki -> **Tools** -> **Add-ons**.
2. Click **Get Add-ons**, enter code: `2055492159`.
3. After installation, select AnkiConnect in the list -> click **Config**.
4. Paste the following configuration exactly to allow access:

   ```json
   {
       "apiKey": null,
       "apiLogPath": null,
       "ignoreOriginList": [],
       "webBindAddress": "127.0.0.1",
       "webBindPort": 8765,
       "webCorsOriginList": ["*"]
   }
   ```

5. **Restart Anki** to apply changes.

### 3. Install the App

1. Download the source code to your computer.
2. Open Terminal (Command Prompt) in the project folder and run:

   ```bash
   # Create a virtual environment (Recommended)
   python -m venv .venv

   # Activate virtual environment
   # On Windows:
   .venv\Scripts\activate
   # On Mac/Linux:
   source .venv/bin/activate

   # Install required dependencies
   pip install -r requirements.txt
   ```

---

## 🚀 How to Use

1. **Launch the App:** In your Terminal with the virtual environment active, type:

    ```bash
    streamlit run streamlit_app.py
    ```

2. **Configure UI:**
    - **Deck/Tag**: Select the group of cards you want to add audio to.
    - **Fields**: Enter the source field names (e.g., `Front, Back`) and the target field for Audio (e.g., `Audio`). Note: Field names must match Anki fields exactly (case-sensitive).
    - **Voice**: Select a language and voice.
3. **Preview:** Always click **Preview Random Note** to check the speed and quality before batch processing.
4. **Execute:** Click **Start Batch Generation**. The app will display real-time progress and the content currently being processed.

---

## 🔍 Technical Details & Troubleshooting

### SSML vs Simple Mode

- **SSML (Advanced)**: Uses XML tags to control speech characteristics (pauses, multiple voices). Better quality but more complex.
- **Simple Mode**: Safety mode that sends only plain text. Switch to this if you hear the voice reading "speak version 1.0" or other tags.

### Common Issues

1. **"Could not connect to Anki"**: Check if Anki is open and if AnkiConnect is configured correctly (see Step 2).
2. **"Field not found"**: Double-check your field names in Anki. `front` is different from `Front`.
3. **Voice reading XML tags**: Enable **Simple Mode** in the app UI.

---

## 📝 License & Contributions

This project is released under the **LGPL-3.0** license.

- The Edge-TTS core belongs to the original authors (Christopher Down & Rany).
- The UI logic, Medical text filtering, and Anki management were developed by **PonZ**.

**Copyright (c) 2026 PonZ.**

---
*Happy studying! May your flashcards always have the right vibe. 🎧📖*
