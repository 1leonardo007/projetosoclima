from flask import Flask, render_template
import sqlite3
import os

app = Flask(__name__)

@app.route("/")
def home():
    return 'Use /pessoa/<id> para ver dados ou /gerar_qrcode/<id> para gerar QR.'

@app.route("/pessoa/<int:id>")
def exibir_pessoa(id):
    conn = sqlite3.connect("dados.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, acesso, entrada, saida, acesso_noturno, foto FROM informacoes WHERE id = ?", (id,))
    pessoa = cursor.fetchone()
    conn.close()

    if pessoa:
        return render_template("pessoas.html", pessoa=pessoa)
    else:
        return "Pessoa não encontrada", 404

@app.route("/gerar_qrcode/<int:id>")
def gerar_qrcode(id):
    import qrcode
    url = f"https://projetosoclima.onrender.com/pessoa/{id}"
    img = qrcode.make(url)
    caminho = os.path.join("static/qrcodes", f"{id}.png")
    img.save(caminho)
    return f"QR Code gerado: <br><img src='/{caminho}' width='200'>"

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=10000)
