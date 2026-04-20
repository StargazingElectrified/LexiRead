import os
import io
import base64
import traceback
from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image

app = Flask(__name__)
CORS(app)  

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")


def ocr_with_gemini(image_bytes: bytes) -> str:
    import google.generativeai as genai
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY environment variable is not set.")

    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")

    image = Image.open(io.BytesIO(image_bytes))
    prompt = (
        "Extract all the text from this image exactly as it appears. "
        "Preserve line breaks and formatting. "
        "Return only the extracted text, nothing else."
    )
    response = model.generate_content([prompt, image])
    return response.text.strip()


_easyocr_reader = None 

def get_easyocr_reader():
    global _easyocr_reader
    if _easyocr_reader is None:
        import easyocr
        _easyocr_reader = easyocr.Reader(["en"], gpu=False)
    return _easyocr_reader


def ocr_with_easyocr(image_bytes: bytes) -> str:
    """Extract text from image bytes using EasyOCR."""
    import numpy as np

    reader = get_easyocr_reader()
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img_array = np.array(image)
    results = reader.readtext(img_array, detail=0, paragraph=True)
    return "\n".join(results).strip()



@app.route("/ocr", methods=["POST"])
def ocr():

    image_bytes = None

    if request.content_type and "multipart/form-data" in request.content_type:
        file = request.files.get("image")
        if not file:
            return jsonify({"text": "", "method": None, "error": "No image file provided."}), 400
        image_bytes = file.read()

    elif request.is_json:
        data = request.get_json()
        b64 = data.get("image", "")
        if not b64:
            return jsonify({"text": "", "method": None, "error": "No image data provided."}), 400
        if "," in b64:
            b64 = b64.split(",", 1)[1]
        image_bytes = base64.b64decode(b64)

    else:
        return jsonify({"text": "", "method": None, "error": "Unsupported content type."}), 415

    if not image_bytes:
        return jsonify({"text": "", "method": None, "error": "Empty image data."}), 400

    gemini_error = None
    if GEMINI_API_KEY:
        try:
            text = ocr_with_gemini(image_bytes)
            return jsonify({"text": text, "method": "gemini", "error": None})
        except Exception as e:
            gemini_error = str(e)
            print(f"[Gemini OCR failed] {gemini_error}")
            traceback.print_exc()

    try:
        text = ocr_with_easyocr(image_bytes)
        return jsonify({
            "text": text,
            "method": "easyocr",
            "error": None,
            "gemini_error": gemini_error  
        })
    except Exception as e:
        easyocr_error = str(e)
        print(f"[EasyOCR failed] {easyocr_error}")
        traceback.print_exc()
        return jsonify({
            "text": "",
            "method": None,
            "error": f"Both OCR methods failed. Gemini: {gemini_error}. EasyOCR: {easyocr_error}"
        }), 500


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "gemini_key_set": bool(GEMINI_API_KEY)})


if __name__ == "__main__":
    print("=" * 50)
    print("  LexiRead OCR Backend")
    print("=" * 50)
    if GEMINI_API_KEY:
        print("  ✓ Gemini API key found — will try Gemini first")
    else:
        print("  ✗ No GEMINI_API_KEY — will use EasyOCR only")
    print("  Listening on http://localhost:5000")
    print("=" * 50)
    app.run(debug=True, port=5000, host='0.0.0.0')
