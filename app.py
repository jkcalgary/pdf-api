from flask import Flask, request, jsonify
import fitz  # PyMuPDF
import werkzeug

app = Flask(__name__)

@app.route('/extract-pdf', methods=['POST'])
def extract_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file: werkzeug.datastructures.FileStorage = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if not file.filename.lower().endswith('.pdf'):
        return jsonify({"error": "Only PDF files are supported"}), 400

    pdf_bytes = file.read()
    if not pdf_bytes:
        return jsonify({"error": "Uploaded file is empty"}), 400

    try:
        text = ""
        with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
            for page in doc:
                page_text = page.get_text("text")
                text += page_text
        return jsonify({"text": text})
    except Exception as e:
        return jsonify({"error": f"Failed to extract PDF text: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
