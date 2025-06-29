from flask import Flask, render_template, url_for
import sqlite3
import qrcode
import os

app = Flask(__name__)

DB_PATH = 'dados.db'
QRCODE_PATH = 'static/qrcodes'

# Página inicial
@app.route('/')
def home():
    return 'Use /pessoa/<id> para ver dados ou /gerar_qrcode/<id> para gerar QR.'

# Rota para exibir dados da pessoa
@app.route('/pessoa/<int:id>')
def exibir_pessoa(id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, acesso, entrada, saida, acesso_noturno, foto FROM informacoes WHERE id = 4", (id,))
    pessoa = cursor.fetchone()
    conn.close()

    if pessoa:
        return render_template("pessoa.html", pessoa=pessoa)
    else:
        return "Pessoa não encontrada", 404

# Rota para gerar o QR Code de uma pessoa
@app.route('/gerar_qrcode/<int:id>')
def gerar_qrcode(id):
    url = f"https://projetosoclima.onrender.com/pessoa/{id}"
    qr = qrcode.make(url)

    # Certifique-se de que o diretório existe
    if not os.path.exists(QRCODE_PATH):
        os.makedirs(QRCODE_PATH)

    caminho = os.path.join(QRCODE_PATH, f'{id}.png')
    qr.save(caminho)
    return f"✅ QR Code gerado! <br><img src='/{caminho}' width='200'>"

# Iniciar com waitress para o Render
if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=10000)
