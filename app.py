import os
from flask import Flask, render_template, request, redirect, url_for, send_file, flash
from werkzeug.utils import secure_filename
from openai import OpenAI
import PyPDF2
from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

# Flask setup
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['TRANSLATIONS_FOLDER'] = 'translations'

ALLOWED_EXTENSIONS = {'pdf', 'docx'}

LANGUAGES = {
    'english': 'English',
    'french': 'French', 
    'arabic': 'Arabic',
    'swahili': 'Swahili',
    'kinyarwanda': 'Kinyarwanda'
}

# ------------ FIXED OPENAI CLIENT -------------
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
# ---------------------------------------------


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_text_from_pdf(path):
    text = ""
    with open(path, "rb") as f:
        pdf = PyPDF2.PdfReader(f)
        for page in pdf.pages:
            text += (page.extract_text() or "") + "\n"
    return text.strip()


def extract_text_from_docx(path):
    doc = Document(path)
    return "\n".join([p.text for p in doc.paragraphs]).strip()


def detect_language(text):
    prompt = f"""
Detect the language of the following text.
Respond ONLY with one word: English, French, Arabic, Swahili, Kinyarwanda.

Text: {text[:400]}...
"""

    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt
    )

    return response.output_text.strip().lower()


def translate_text(text, source, target):
    prompt = f"""
Translate the following text from {source} to {target}.
Maintain accuracy, structure, and meaning.

TEXT:
{text}
"""

    response = client.responses.create(
        model="gpt-4o",
        input=prompt
    )

    return response.output_text.strip()


def create_pdf_file(text, output_path):
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    for p in text.split("\n"):
        if p.strip():
            story.append(Paragraph(p, styles["Normal"]))
            story.append(Spacer(1, 0.2 * inch))

    doc.build(story)


@app.route('/')
def index():
    return render_template('index.html', languages=LANGUAGES)


@app.route('/translate', methods=['POST'])
def translate():
    if 'file' not in request.files:
        flash('No file uploaded.', 'error')
        return redirect(url_for('index'))

    file = request.files['file']
    source_language = request.form.get('source_language', '').lower()
    target_language = request.form.get('target_language', '').lower()

    if file.filename == '':
        flash('Please select a file.', 'error')
        return redirect(url_for('index'))

    if not allowed_file(file.filename):
        flash('Invalid file type.', 'error')
        return redirect(url_for('index'))

    if source_language == target_language:
        flash('Source and target cannot be the same.', 'error')
        return redirect(url_for('index'))

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['TRANSLATIONS_FOLDER'], exist_ok=True)

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    try:
        ext = filename.rsplit('.', 1)[1].lower()

        if ext == "pdf":
            extracted = extract_text_from_pdf(file_path)
        else:
            extracted = extract_text_from_docx(file_path)

        detected = detect_language(extracted)

        if detected != source_language and not detected.startswith(source_language[:3]):
            raise Exception(f"Language mismatch. Expected {source_language}, got {detected}.")

        translated = translate_text(extracted, LANGUAGES[source_language], LANGUAGES[target_language])

        output_filename = filename.split('.')[0] + "_translated.pdf"
        output_path = os.path.join(app.config['TRANSLATIONS_FOLDER'], output_filename)

        create_pdf_file(translated, output_path)

        os.remove(file_path)

        return redirect(url_for('success', filename=output_filename))

    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        flash(f"Error: {str(e)}", "error")
        return redirect(url_for('index'))


@app.route('/success')
def success():
    filename = request.args.get("filename", "")
    return render_template("success.html", filename=filename)


@app.route('/download/<filename>')
def download(filename):
    path = os.path.join(app.config['TRANSLATIONS_FOLDER'], filename)
    return send_file(path, as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)