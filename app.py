from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import PyPDF2
import os
from werkzeug.utils import secure_filename
import re

app = Flask(__name__, static_folder='static')
CORS(app)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF file"""
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            num_pages = len(pdf_reader.pages)
            
            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {str(e)}")
    
    return text

def simple_summarize(text, max_sentences=5):
    """Create a simple extractive summary"""
    # Clean the text
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Split into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    # Filter out very short sentences
    sentences = [s for s in sentences if len(s.split()) > 5]
    
    if not sentences:
        return "Unable to generate summary from the PDF content."
    
    # Simple scoring: prioritize sentences with more words (up to a limit)
    # and those appearing near the beginning
    scored_sentences = []
    for i, sentence in enumerate(sentences[:50]):  # Consider first 50 sentences
        position_score = 1 - (i / 50)  # Earlier sentences score higher
        length_score = min(len(sentence.split()) / 30, 1)  # Prefer moderate length
        score = position_score * 0.6 + length_score * 0.4
        scored_sentences.append((score, sentence))
    
    # Sort by score and take top sentences
    scored_sentences.sort(reverse=True, key=lambda x: x[0])
    summary_sentences = [s[1] for s in scored_sentences[:max_sentences]]
    
    # Sort by original order for coherence
    summary = ' '.join(summary_sentences)
    
    return summary

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Extract text from PDF
            text = extract_text_from_pdf(filepath)
            
            # Generate summary
            summary = simple_summarize(text)
            
            # Clean up uploaded file
            os.remove(filepath)
            
            return jsonify({
                'success': True,
                'summary': summary,
                'text_length': len(text)
            })
        except Exception as e:
            # Clean up on error
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'Invalid file type. Please upload a PDF file.'}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
