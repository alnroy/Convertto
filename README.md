# ✍️ Handwriting to Text Converter with Smart Text Editor

An advanced web-based application that converts handwritten notes or images into editable text using **Google Vision API**, **Python**, and **JavaScript**.  
It features an intelligent **inbuilt text editor** that allows users to **translate** and **transliterate** text in real-time across multiple languages.

---

## 🌟 Features

- 🖋️ **Handwriting Recognition** — Extract text from handwritten images using Google Vision API  
- 🧠 **Python Backend Processing** — For OCR integration, text cleanup, and NLP utilities  
- 🪶 **Inbuilt Smart Text Editor** — Edit, format, and manage recognized text instantly  
- 🌐 **Translation & Transliteration** — Convert words or entire paragraphs between languages  
- ⚡ **Real-time JavaScript UI** — Smooth, responsive experience powered by modern JS libraries  
- 📁 **File Upload Support** — Upload handwritten images or drag-and-drop directly into the editor  

---

## 🏗️ Tech Stack

| Layer | Technologies Used |
|-------|--------------------|
| **Frontend** | HTML5, CSS3, JavaScript (ES6+), Quill.js / TinyMCE (Editor) |
| **Backend** | Python (Django / RestAPI) |
| **APIs** | Google Vision API, Google Translate API |
| **Libraries** | `requests`, `google-cloud-vision`, `googletrans`, `gTTS` |
| **Utilities** | JSON, AJAX, Fetch API, FileReader |
| **Deployment** | GitHub Pages / Django Server |

---

## 🚀 Getting Started

1️⃣ Clone the Repository
git clone https://github.com/alnroy/handwriting-to-text.git
cd handwriting-to-text

2️⃣ Create and Activate Virtual Environment
python -m venv venv
venv\Scripts\activate   # Windows
# OR
source venv/bin/activate   # macOS/Linux

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Set Up Google Cloud Credentials

Create a Google Cloud Project

Enable Vision API and Translate API

Download the service account JSON key and set the environment variable:

set GOOGLE_APPLICATION_CREDENTIALS="path\to\service-account.json"

🧩 How It Works

🖼️ Image Upload – The user uploads a handwritten note or image

🤖 OCR Processing – Python backend sends it to Google Vision API for text extraction

🧹 Text Cleaning – Extracted text is processed, formatted, and displayed in the editor

🌍 Translate / Transliterate – User can convert the recognized text to any chosen language

💾 Save or Export – The final document can be downloaded or copied for further use

🧠 Example Workflow
1. Upload: "notes.jpg"
2. Vision API → "Hello this is my handwriting"
3. Text Editor → Edit text, change style or font
4. Translate → "Hola esto es mi escritura"
5. Save → Export as .txt or .docx

🧰 Requirements

Ensure the following are installed:

Python 3.8+

pip (Python Package Manager)

Google Cloud SDK (for authentication)

Modern browser with JavaScript enabled


⚙️ Core Libraries Used
🧩 Python
pip install google-cloud-vision googletrans==4.0.0-rc1 Flask requests gTTS

💻 JavaScript

Quill.js / TinyMCE – Rich text editor

Google Translate API (via fetch calls)

FileReader API – For previewing uploaded images

💡 Future Enhancements

🗣️ Add speech-to-text and text-to-speech integration

📱 Create a mobile-friendly PWA version

☁️ Save documents to Google Drive or Firebase

🧾 Add auto-language detection


✨ “Turning handwriting into meaning — bridging humans and machines through language.” 🌍

git clone https://github.com/alnroy/handwriting-to-text.git
cd handwriting-to-text
