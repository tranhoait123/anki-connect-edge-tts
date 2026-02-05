# 🎧 Anki Connect Edge TTS - The Ultimate Batch Audio Solution for Anki

Welcome to the most powerful, user-friendly, and optimized tool for elevating your Anki experience. This isn't just a simple TTS generator; it's a meticulously designed system to help you "learn faster and remember longer" through the power of high-quality AI speech.

> **Made with ❤️ by PonZ**
>
> [Tiếng Việt (README.md)](./README.md)

---

## 📖 Project Vision

Staring at text-heavy flashcards can be monotonous and often leads to mispronunciation or poor retention, especially with complex Medical terminology or new languages. This project was created to:

1. **Save Time**: Instead of manually creating audio files, you can batch-process thousands of cards in minutes.
2. **Enhance Memory**: The dual-coding effect (visual + auditory) stimulates deeper neural encoding.
3. **Optimize Workflow**: Professionally manage your decks, filling in missing audio without disrupting your existing data.

**Inspiration:** Inherited and developed from the original concept by [msjsc001/Anki-TTS-Edge](https://github.com/msjsc001/Anki-TTS-Edge), I have completely rebuilt the interface and logic to be more intuitive for modern users and specialized academic communities.

---

## ✨ Feature Breakdown (Everything You Need)

### 1. 🚀 Intelligent Deck Management

- **🔍 Scan Status**: Do you have thousands of cards and don't know which ones are missing audio? With one click, the App reports:
  - Total card count.
  - Cards with existing audio.
  - "Silent" cards (missing audio).
- **⚡ Smart Fill**: The App is smart enough to detect cards with existing audio and skip them, focusing only on the gaps. This is extremely useful when adding new cards to a massive deck.
- **🗑️ Clear Audio**: Want to refresh the voice for your entire deck? The Clear button wipes the audio field, making it ready for a fresh generation batch.

### 2. 🩺 Medical & Language Specific Optimization

- **📝 Abbreviation Expansion**: A "Golden Feature" for students.
  - Example: Set `PT=Patient`, and the voice will read "Patient" whenever it encounters `PT`.
  - Supports an unlimited custom abbreviation list directly in the UI.
- **🧹 Text Cleaning Pro**:
  - Removes icons, emojis, and miscellaneous symbols.
  - Deletes citation numbers (e.g., `[1]`, `[2,3]`) that disrupt the flow of speech.
  - Cleans up stray HTML tags so the engine doesn't read them out loud.

### 3. 🎙️ High-End Audio Technology (Edge TTS)

- **🎭 Advanced SSML**: Configurable multi-voice setup. Have a Male voice read the Question and a Female voice read the Answer (or vice-versa) to create a distinct mental separation. Includes a built-in 1-second pause for better processing time.
- **🛡️ Simple Mode**: If the engine ever starts reading out the XML source code (e.g., "speak version 1.0"), switch to this mode. It sends pure plain text, guaranteeing 100% stability.
- **🐢 Speed Control**: Customize from slow (to hear every phoneme) to fast (for quick reviews). **0.9x** is recommended for complex academic content.

---

## 🛠️ Step-by-Step "Hands-On" Installation

### Step 1: Environment Setup (One-Time)

1. Download and install **Python** from [python.org](https://www.python.org/downloads/). (Make sure to check **"Add Python to PATH"** during installation).
2. Download this source code and extract the ZIP file.

### Step 2: Configure Anki & AnkiConnect

The project needs "permission" to talk to your Anki database.

1. Open Anki on your computer.
2. Go to **Tools** -> **Add-ons** -> **Get Add-ons**.
3. Enter code: `2055492159` to install **AnkiConnect**.
4. After installation, select AnkiConnect -> **Config** and paste this block:

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

5. **Critical**: Close and restart Anki.

### Step 3: Install Core Libraries

1. Open the folder containing the downloaded code.
2. Right-click in the folder and select **Open in Terminal** (or Command Prompt).
3. Run the command to create a clean environment:

    ```bash
    python -m venv .venv
    ```

4. Activate it:
    - **Windows**: `.venv\Scripts\activate`
    - **Mac/Linux**: `source .venv/bin/activate`
5. Install required packages:

    ```bash
    pip install -r requirements.txt
    ```

---

## 🚀 Practical Usage Guide

1. **Launch**: In your Terminal, type `streamlit run streamlit_app.py`. A browser window will open automatically.
2. **Connection**: The App should show a green "Connected to Anki" status on the left sidebar. If it's red, make sure Anki is actually running.
3. **Filtration**:
    - Select your **Deck**.
    - Enter a **Tag** if you only want to process a specific subset of cards.
4. **Field Configuration**:
    - **Source Fields**: The names of the fields containing text (e.g., `Front, Back`).
    - **Target Field**: The name of the field where the audio tag will be stored (e.g., `Audio`).
5. **Voice Selection**: Choose your target Language and select a voice (e.g., `en-US-GuyNeural` for a standard American accent).
6. **Execute**: Click **Start Batch Generation** and watch the progress bar.

---

## 🔍 Frequently Asked Questions (FAQ) & Troubleshooting

- **Q: Why does the App say it cannot connect to Anki?**
  - *A*: Ensure Anki is open and AnkiConnect is correctly configured as per Step 2.
- **Q: The voice is reading weird tags like "speak version 1.0"?**
  - *A*: This is an occasional SSML parsing error with Microsoft servers. Check the **Simple Mode** box in the App; this will resolve it immediately.
- **Q: I want to regenerate the audio with a different speed?**
  - *A*: Change the speed slider, check **"Force overwrite existing audio"**, and run the generation again.

---

## 📝 License & Copyright

This project is released under the **LGPL-3.0** license.

- All audio assets generated belong to you.
- Please retain the **Made by PonZ** credits if you share or fork this project.

**Copyright (c) 2026 PonZ.**

---
*I hope this tool makes your learning journey smoother and more enjoyable! Happy studying!* 🎧📚
