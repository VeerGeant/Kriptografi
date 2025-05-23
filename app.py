from flask import Flask, render_template, request, send_file, redirect, url_for, session
import os
from ciphers import (
    affine, autokey_vigenere, extended_vigenere,
    hill, playfair, vigenere
)

app = Flask(__name__)
app.secret_key = 'rahasia'  # butuh secret key buat session
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    matrix_preview = None  # Inisialisasi matrix_preview di awal
    
    if request.method == 'POST':
        text_input = request.form.get("text") or ""
        key_input = request.form.get("key") or ""
        cipher = request.form.get("cipher")
        mode = request.form.get("mode")
        group5 = request.form.get("group5") == "on"
        uploaded_file = request.files.get("file")
        
        if uploaded_file and uploaded_file.filename:
            filepath = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
            uploaded_file.save(filepath)
            if cipher == 'extended_vigenere':
                with open(filepath, "rb") as f:
                    file_bytes = f.read()
                result = extended_vigenere.extended_vigenere(file_bytes, key_input, mode)
                output_path = filepath + ".enc" if mode == "encrypt" else filepath + ".dec"
                with open(output_path, "wb") as f:
                    f.write(result)
                return send_file(output_path, as_attachment=True)

        else:
            text_input = text_input.strip()

            if cipher == "vigenere":
                result = vigenere.vigenere_cipher(text_input, key_input, mode)
            elif cipher == "autokey_vigenere":
                result = autokey_vigenere.auto_key_vigenere(text_input, key_input, mode)
            elif cipher == "affine":
                a, b = map(int, key_input.split(','))
                result = affine.affine_cipher(text_input, a, b, mode)
            elif cipher == "playfair":
                result, matrix_preview = playfair.playfair_cipher(text_input, key_input, mode)
            elif cipher == "hill":
                result = hill.hill_cipher(text_input, key_input, mode, size=3)
            elif cipher == "extended_vigenere":
                result = extended_vigenere.extended_vigenere(text_input.encode(), key_input, mode).decode(errors='ignore')

            if group5:
                result = ' '.join(result[i:i+5] for i in range(0, len(result), 5))

            session['result'] = result  # simpan ke session
            session['matrix_preview'] = matrix_preview  # simpan matrix preview jika Playfair dipilih

        return redirect(url_for("index"))  # redirect ke GET setelah POST

    result = session.pop('result', None)  # ambil result dari session
    matrix_preview = session.pop('matrix_preview', None)  # ambil matrix preview dari session hanya jika Playfair dipilih
    return render_template("index.html", result=result, matrix_preview=matrix_preview)

if __name__ == '__main__':
    app.run(debug=True)
