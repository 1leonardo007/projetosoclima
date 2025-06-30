import sqlite3

# Conecta à base de dados
conn = sqlite3.connect("dados.db")
cursor = conn.cursor()

# Adiciona a coluna 'cargo' se ela ainda não existir
try:
    cursor.execute("ALTER TABLE informacoes ADD COLUMN cargo TEXT;")
    print("✅ Coluna 'cargo' adicionada.")
except sqlite3.OperationalError:
    print("⚠️ A coluna 'cargo' já existe.")

# Atualiza os cargos para os IDs desejados
cargos = {
    2: "Gerente",
    3: "Administrador",
    4: "Engenheiro Informática"
}

for id_pessoa, cargo in cargos.items():
    cursor.execute("UPDATE informacoes SET cargo = ? WHERE id = ?", (cargo, id_pessoa))
    print(f"🔁 Cargo '{cargo}' adicionado ao ID {id_pessoa}")

conn.commit()
conn.close()
print("✅ Banco de dados atualizado com sucesso.")
