# Student Translator MVP

A Flask web application that translates documents between English, French, Arabic, Swahili, and Kinyarwanda using OpenAI's GPT-4o model with high accuracy and language validation.

## Features

- Support for 5 languages: English, French, Arabic, Swahili, and Kinyarwanda
- Source language selection with automatic validation
- Upload PDF or DOCX documents (max 16MB)
- AI-powered language detection and validation
- High-accuracy translation using GPT-4o
- Download translated documents as DOCX files
- Modern, educational-themed UI with social media colors
- Comprehensive error handling and user feedback

## Requirements

- Python 3.8 or higher
- OpenAI API key (get one from [OpenAI Platform](https://platform.openai.com/api-keys))

## Installation

1. **Clone or download this repository**

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables**:
   - Copy `.env.example` to `.env`:
     ```bash
     copy .env.example .env
     ```
   - Edit `.env` and add your OpenAI API key:
     ```
     OPENAI_API_KEY=your_actual_api_key_here
     ```

## Running the Application

1. **Make sure your virtual environment is activated**

2. **Set the OpenAI API key** (if not using .env file):
   - On Windows:
     ```bash
     $env:OPENAI_API_KEY="your_api_key_here"
     ```
   - On macOS/Linux:
     ```bash
     export OPENAI_API_KEY="your_api_key_here"
     ```

3. **Run the Flask application**:
   ```bash
   python app.py
   ```

4. **Open your browser** and navigate to:
   ```
   http://localhost:5000
   ```

## Usage

1. **Select source language**: Choose the language of your document (English, French, Arabic, Swahili, or Kinyarwanda)
2. **Upload document**: Select a PDF or DOCX file (max 16MB) - the system will validate the language matches your selection
3. **Select target language**: Choose the language you want to translate to (must be different from source)
4. **Translate**: Click "Translate Document" and wait for high-accuracy AI processing
5. **Download**: Once complete, download your professionally translated PDF document

## Project Structure

```
Student Translator MVP/
├── app.py                 # Flask application main file
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── README.md             # This file
├── templates/            # HTML templates
│   ├── index.html        # Main upload form
│   └── success.html      # Success page with download link
├── static/               # Static files (CSS, JS)
│   ├── styles.css        # Styling
│   └── script.js         # JavaScript functionality
├── uploads/              # Temporary upload directory (auto-created)
└── translations/          # Translated documents directory (auto-created)
```

## Notes

- **Language Validation**: The system automatically detects document language and validates it matches your selection
- **High Accuracy**: Uses GPT-4o model with specialized prompts for educational and professional documents
- **Supported Languages**: English, French, Arabic, Swahili, and Kinyarwanda (bidirectional translation)
- **File Management**: Uploaded files are automatically deleted after processing for privacy
- **Output**: All translations are provided as PDF files for easy sharing and viewing
- **Limits**: Maximum file size is 16MB, supported formats are PDF and DOCX

## Troubleshooting

- **"OPENAI_API_KEY not set"**: Make sure you've set the environment variable or created a `.env` file
- **"No text could be extracted"**: The document might be empty, corrupted, or contain only images
- **"Document language mismatch"**: The detected language doesn't match your selection - choose the correct source language
- **"Source and target languages cannot be the same"**: Select different languages for translation
- **Translation errors**: Check your OpenAI API key and account credits

## License

This project is provided as-is for educational purposes.

