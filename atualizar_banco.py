import sqlite3

# Conecta ao banco de dados
conn = sqlite3.connect("dados.db")
cursor = conn.cursor()

# Dados que você quer atualizar (exemplo para o ID 6)
id_pessoa = 2
nova_foto = "leonardo2.jpg"
novo_cargo = "Engenheiro Informático"

# Comando SQL para atualizar
cursor.execute("""
    UPDATE informacoes
    SET foto = ?, cargo = ?
    WHERE id = ?
""", (nova_foto, novo_cargo, id_pessoa))

# Salva as alterações
conn.commit()
conn.close()

print(f"✅ Dados atualizados com sucesso para o ID {id_pessoa}")
