import sqlite3
import qrcode
import os

# URL base do Render
URL_BASE = "https://projetosoclima-6.onrender.com/pessoa/"

# Gera só para o ID 4
id_pessoa = 4

# Conecta ao banco
conn = sqlite3.connect("dados.db")
cursor = conn.cursor()

cursor.execute("SELECT nome FROM informacoes WHERE id = ?", (id_pessoa,))
resultado = cursor.fetchone()
conn.close()

if resultado:
    nome = resultado[0]
    url = f"{URL_BASE}{id_pessoa}"
    qr = qrcode.make(url)

    os.makedirs("static/qrcodes", exist_ok=True)
    caminho = f"static/qrcodes/{id_pessoa}.png"
    qr.save(caminho)
    print(f"✅ QR Code gerado para {nome} (ID: {id_pessoa}) → {caminho}")
else:
    print(f"❌ Nenhuma pessoa com ID {id_pessoa} encontrada.")
