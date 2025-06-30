from flask import Flask, render_template, send_file
import sqlite3
import os
import qrcode

app = Flask(__name__)
DB_PATH = 'dados.db'

@app.route('/')
def home():
    return '✅ Use /pessoa/<id> para ver dados ou /gerar_qrcode/<id> para gerar QR.'

@app.route('/pessoa/<int:id>')
def exibir_pessoa(id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, acesso, entrada, saida, acesso_noturno, foto FROM informacoes WHERE id = ?", (id,))
    pessoa = cursor.fetchone()
    conn.close()

    if pessoa:
        return render_template("pessoa.html", pessoa=pessoa)
    else:
        return "❌ Pessoa não encontrada", 404

@app.route('/gerar_qrcode/<int:id>')
def gerar_qrcode(id):
    url = f"https://projetosoclima-6.onrender.com/pessoa/{id}"
    img = qrcode.make(url)

    # Criar a pasta se não existir
    pasta = "static/qrcodes"
    os.makedirs(pasta, exist_ok=True)

    caminho = os.path.join(pasta, f"{id}.png")
    img.save(caminho)

    return f'''
        ✅ QR Code gerado com sucesso para o ID {id}!<br><br>
        <img src="/static/qrcodes/{id}.png" width="200"><br><br>
        <a href="{url}" target="_blank">Ver dados da pessoa {id}</a>
    '''

if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=10000)
