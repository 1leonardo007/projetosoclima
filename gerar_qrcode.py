import qrcode
import os

# URL do Render para o ID 4
url = "https://projetosoclima-6.onrender.com/pessoa/4"

# Caminho onde o QR Code será salvo
output_dir = "static/qrcodes"
os.makedirs(output_dir, exist_ok=True)

# Criar o QR Code
qr = qrcode.make(url)

# Salvar imagem
caminho_arquivo = os.path.join(output_dir, "4.png")
qr.save(caminho_arquivo)

print(f"✅ QR Code gerado com sucesso: {caminho_arquivo}")
