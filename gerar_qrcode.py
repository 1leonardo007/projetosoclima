import sqlite3
import qrcode

# URL da aplicação no Render
URL_BASE = "https://projetosoclima.onrender-6.com"

# Conecta ao banco de dados
conn = sqlite3.connect("dados.db")
cursor = conn.cursor()

# Busca apenas o ID 4
cursor.execute("SELECT id, nome FROM informacoes WHERE id = 4")
dados = cursor.fetchall()

# Loop pelos dados (apenas 1 neste caso)
for id_pessoa, nome in dados:
    url = f"{URL_BASE}{id_pessoa}"
    qr = qrcode.make(url)

    # Caminho do arquivo PNG do QR Code
    caminho = f"static/qrcodes/{id_pessoa}.png"
    qr.save(caminho)

    print(f"✅ QR Code gerado para {nome} (ID: {id_pessoa}) → {caminho}")

conn.close()
