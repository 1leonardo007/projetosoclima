from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
DATABASE = 'soclima.db'

# Função para conectar ao banco de dados
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Página principal - lista os dados
@app.route('/')
def index():
    conn = get_db()
    pessoas = conn.execute('SELECT * FROM informacoes').fetchall()
    conn.close()
    return render_template('index.html', pessoas=pessoas)

# Página para adicionar novo registro
@app.route('/adicionar', methods=['GET', 'POST'])
def adicionar():
    if request.method == 'POST':
        nome = request.form['nome']
        acesso = request.form['acesso']
        entrada = request.form['entrada']
        saida = request.form['saida']

        conn = get_db()
        conn.execute('INSERT INTO informacoes (nome, acesso, entrada, saida) VALUES (?, ?, ?, ?)',
                     (nome, acesso, entrada, saida))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('adicionar.html')

# Editar registro existente
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    conn = get_db()
    pessoa = conn.execute('SELECT * FROM informacoes WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        nome = request.form['nome']
        acesso = request.form['acesso']
        entrada = request.form['entrada']
        saida = request.form['saida']

        conn.execute('UPDATE informacoes SET nome=?, acesso=?, entrada=?, saida=? WHERE id=?',
                     (nome, acesso, entrada, saida, id))
        conn.commit()
        conn.close()
        return redirect('/')
    conn.close()
    return render_template('editar.html', pessoa=pessoa)

# Excluir registro (função que estava faltando)
@app.route('/excluir/<int:id>')
def excluir(id):
    conn = get_db()
    conn.execute('DELETE FROM informacoes WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')

# Iniciar servidor
if __name__ == '__main__':
    if not os.path.exists(DATABASE):
        # Cria o banco e a tabela caso não existam
        conn = get_db()
        conn.execute('''
            CREATE TABLE informacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                acesso TEXT NOT NULL,
                entrada TEXT NOT NULL,
                saida TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()
        print('Banco de dados criado com sucesso.')

    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)