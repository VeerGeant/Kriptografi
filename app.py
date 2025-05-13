from flask import Flask, render_template, request, send_file, redirect, url_for, session
import io
import os
from ciphers import (
    affine, autokey_vigenere, extended_vigenere,
    hill, playfair, vigenere
)

app = Flask(__name__)
app.secret_key = 'rahasia'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text_input = request.form.get("text") or ""
        key_input = request.form.get("key") or ""
        cipher = request.form.get("cipher")
        mode = request.form.get("mode")
        group5 = request.form.get("group5") == "on"
        uploaded_file = request.files.get("file")

        if uploaded_file and uploaded_file.filename:
            filename = uploaded_file.filename
            file_ext = os.path.splitext(filename)[1].lower()

            if cipher == 'extended_vigenere' and file_ext != '.txt':
                file_bytes = uploaded_file.read()
                result = extended_vigenere.extended_vigenere(file_bytes, key_input, mode)
                return send_file(
                    io.BytesIO(result),
                    as_attachment=True,
                    download_name=filename + (".enc" if mode == "encrypt" else ".dec"),
                    mimetype="application/octet-stream"
                )
            else:
                text_input = uploaded_file.read().decode("utf-8", errors="ignore")

        text_input = text_input.strip()

        # Proses enkripsi/dekripsi
        if cipher == "vigenere":
            result = vigenere.vigenere_cipher(text_input, key_input, mode)
        elif cipher == "autokey_vigenere":
            result = autokey_vigenere.auto_key_vigenere(text_input, key_input, mode)
        elif cipher == "affine":
            a, b = map(int, key_input.split(','))
            result = affine.affine_cipher(text_input, a, b, mode)
        elif cipher == "playfair":
            result = playfair.playfair_cipher(text_input, key_input, mode)
        elif cipher == "hill":
            result = hill.hill_cipher(text_input, key_input, mode, size=3)
        elif cipher == "extended_vigenere":
            result = extended_vigenere.extended_vigenere(text_input.encode(), key_input, mode).decode(errors='ignore')

        # Kelompokkan 5 huruf
        if group5:
            result = ' '.join(result[i:i+5] for i in range(0, len(result), 5))

        # Simpan ke session
        session['cipher'] = cipher
        session['mode'] = mode
        session['key'] = key_input
        session['text'] = text_input
        session['group5'] = group5
        session['result'] = result
        return redirect(url_for("index"))

    # Ambil hasil dari session
    result = session.pop('result', None)
    cipher = session.pop('cipher', '')
    mode = session.pop('mode', '')
    key = session.pop('key', '')
    text = session.pop('text', '')
    group5 = session.pop('group5', False)

    return render_template("index.html", result=result, cipher=cipher, mode=mode, key=key, text=text, group5=group5)

if __name__ == '__main__':
    app.run(debug=True)
