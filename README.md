# PDF Summarizer

A web application that allows users to upload PDF documents and get AI-generated summaries.

## Features

- 📄 Upload PDF files via drag-and-drop or file browser
- 🤖 Automatic text extraction from PDFs
- ✨ AI-powered summarization
- 🎨 Clean, modern UI
- 📱 Responsive design

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Start the Flask backend:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

## Usage

1. Click "Browse Files" or drag and drop a PDF file onto the upload area
2. Wait for the PDF to be processed
3. View the generated summary
4. Click "Upload Another PDF" to process a new file

## Technology Stack

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python Flask
- **PDF Processing**: PyPDF2
- **Summarization**: Extractive summarization algorithm

## How It Works

1. User uploads a PDF file through the web interface
2. Backend extracts text from the PDF using PyPDF2
3. Text is processed and summarized using an extractive summarization algorithm
4. Summary is displayed on the web UI

## Notes

- Maximum file size: 16MB
- Supported formats: PDF only
- The summarization uses an extractive approach that selects the most important sentences from the document

## Future Enhancements

- Integration with advanced AI models (OpenAI, Anthropic, etc.)
- Support for multiple languages
- Adjustable summary length
- Export summary as text file
- Document comparison feature
