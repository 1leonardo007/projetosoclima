from flask import Flask, render_template
import sqlite3
import os
import qrcode

app = Flask(__name__)

DB_PATH = 'dados.db'
QRCODE_PATH = 'static/qrcodes'

@app.route('/')
def home():
    return 'Use /pessoa/<id> para ver dados ou /gerar_qrcode/<id> para gerar QR.'

@app.route('/pessoa/<int:id>')
def pessoa(id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM informacoes WHERE id = ?", (id,))
    dados = cursor.fetchone()
    conn.close()

    if dados:
        return render_template("pessoas.html", pessoa=dados)
    else:
        return "Pessoa não encontrada."

@app.route('/gerar_qrcode/<int:id>')
def gerar_qrcode(id):
    url = f"https://projetosoclima.onrender.com/pessoa/{id}"
    img = qrcode.make(url)
    caminho = os.path.join(QRCODE_PATH, f'qrcode_id{id}.png')
    img.save(caminho)
    return f"QR gerado: <br><img src='/{caminho}' width='200'>"

if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=10000)
