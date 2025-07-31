import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configurações de pasta de upload
app.config['UPLOAD_FOLDER'] = 'static/fotos'
app.config['MAX_CONTENT_LENGTH'] = 3 * 1024 * 1024  # 3MB
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Função para verificar extensão da imagem
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Conexão com banco de dados
def get_db():
    conn = sqlite3.connect('dados.db')
    conn.row_factory = sqlite3.Row
    return conn

# Página principal (admin)
@app.route('/admin')
def admin():
    conn = get_db()
    pessoas = conn.execute('SELECT * FROM informacoes').fetchall()
    conn.close()
    return render_template('index.html', pessoas=pessoas)

# Adicionar pessoa
@app.route('/adicionar', methods=['GET', 'POST'])
def adicionar():
    if request.method == 'POST':
        nome = request.form['nome']
        acesso = request.form['acesso']
        cargo = request.form['cargo']
        entrada = request.form['entrada']
        saida = request.form['saida']
        acesso_noturno = 1 if 'acesso_noturno' in request.form else 0

        # Foto
        foto = None
        if 'foto' in request.files:
            foto_file = request.files['foto']
            if foto_file and allowed_file(foto_file.filename):
                foto = secure_filename(foto_file.filename)
                foto_path = os.path.join(app.config['UPLOAD_FOLDER'], foto)
                foto_file.save(foto_path)

        conn = get_db()
        conn.execute(
            'INSERT INTO informacoes (nome, acesso, cargo, entrada, saida, acesso_noturno, foto) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (nome, acesso, cargo, entrada, saida, acesso_noturno, foto)
        )
        conn.commit()
        conn.close()
        return redirect('/admin')
    return render_template('adicionar.html')

# Editar pessoa
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    conn = get_db()
    pessoa = conn.execute('SELECT * FROM informacoes WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        nome = request.form['nome']
        acesso = request.form['acesso']
        cargo = request.form['cargo']
        entrada = request.form['entrada']
        saida = request.form['saida']
        acesso_noturno = 1 if 'acesso_noturno' in request.form else 0

        foto = pessoa['foto']
        if 'foto' in request.files:
            foto_file = request.files['foto']
            if foto_file and allowed_file(foto_file.filename):
                foto = secure_filename(foto_file.filename)
                foto_path = os.path.join(app.config['UPLOAD_FOLDER'], foto)
                foto_file.save(foto_path)

        conn.execute(
            'UPDATE informacoes SET nome=?, acesso=?, cargo=?, entrada=?, saida=?, acesso_noturno=?, foto=? WHERE id=?',
            (nome, acesso, cargo, entrada, saida, acesso_noturno, foto, id)
        )
        conn.commit()
        conn.close()
        return redirect('/admin')

    return render_template('editar.html', pessoa=pessoa)

# Excluir pessoa
@app.route('/excluir/<int:id>')
def excluir(id):
    conn = get_db()
    conn.execute('DELETE FROM informacoes WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return redirect('/admin')

# Página pública por ID
@app.route('/pessoa/<int:id>')
def pessoa(id):
    conn = get_db()
    pessoa = conn.execute('SELECT * FROM informacoes WHERE id=?', (id,)).fetchone()
    conn.close()
    if pessoa:
        return render_template('pessoa.html', pessoa=pessoa)
    return "Pessoa não encontrada", 404

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))  # define a porta dinamicamente para o Render
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(host='0.0.0.0', port=port, debug=True)