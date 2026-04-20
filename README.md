# LexiRead

> **Disability? Nah, this is ability.**  
> A dyslexia-friendly reading assistant with OCR, text-to-speech, and customizable reading tools.

---

## What is LexiRead?

LexiRead is a web app built to help people with dyslexia read and understand text more easily. It combines a clean, accessible frontend with a Python backend that uses 
AI to extract text from images.

### Features

- **Dyslexic Font Toggle** - Switch to the Lexend font, designed specifically for readers with dyslexia
- **Font Size & Line Spacing Controls** - Adjust text size and spacing on the fly for maximum comfort
- **Text to Speech** - Paste any text and have it read aloud in 10+ languages using your browser's speech engine
- **Image OCR** - Upload a photo of any text (a book page, sign, handwritten note) and extract the text using Gemini AI, with EasyOCR as a fallback
- **Friendly Format** - Paste any text and reformat it with dyslexia-friendly typography (Lexend font, wider spacing, increased line height)
- **Know More** - FAQ section explaining dyslexia, its causes, and the strengths of dyslexic thinkers

---

## Project Structure

```
LexiRead/
├── index.html      # Frontend, all UI, styling, and browser-side logic
├── backend.py      # Python server, handles OCR using Gemini AI + EasyOCR
├── .gitignore
└── README.md
```

---

## How It Works

### Frontend (`index.html`)
A single-page HTML/CSS/JS app, open it in a browser. It communicates with the backend via `fetch()` to send images for OCR.

### Backend (`backend.py`)
A Flask REST API with one main endpoint:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/ocr` | POST | Accepts an image, returns extracted text |
| `/health` | GET | Checks if the server is running and if the Gemini key is set |

**OCR priority:**
1. Tries **Gemini 1.5 Flash** (Google AI) first, fast and accurate
2. Falls back to **EasyOCR** if Gemini fails or no API key is provided

---

##  How to Run

### Prerequisites

- Python 3.8+
- A free Gemini API key from [aistudio.google.com](https://aistudio.google.com) *(optional but recommended)*

### 1. Install dependencies

```bash
pip install flask flask-cors google-generativeai easyocr pillow
```

### 2. Set your Gemini API key

**Windows (PowerShell):**
```powershell
$env:GEMINI_API_KEY = "your-key-here"
```

**Mac/Linux:**
```bash
export GEMINI_API_KEY="your-key-here"
```

> If you skip this step, LexiRead will still work using EasyOCR for text extraction, it just won't use Gemini.

### 3. Start the backend

```bash
python backend.py
```

You should see:
```
==================================================
  LexiRead OCR Backend
==================================================
  ✓ Gemini API key found — will try Gemini first
  Listening on http://localhost:5000
==================================================
```

### 4. Serve the frontend

Open a **second terminal** in the LexiRead folder and run:

```bash
python -m http.server 8080
```

> Do NOT open `index.html` by double-clicking it. It must be served over HTTP or the browser will block requests to the backend.

### 5. Open the app

Go to **[http://localhost:8080](http://localhost:8080)** in your browser.

---

## API Key Safety

- Never hardcode your API key directly in `backend.py`
- Never commit a real API key to GitHub
- Always use environment variables (as shown above)

---

## Contact

Built by **Vansh Sharma** - vanshsharma.73804@gmail.com

---
