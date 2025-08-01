import os
import sqlite3
from flask import Flask, render_template, request, redirect, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configurações de upload
app.config['UPLOAD_FOLDER'] = 'static/fotos'
app.config['MAX_CONTENT_LENGTH'] = 3 * 1024 * 1024  # Máx. 3MB por imagem
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Verifica se a extensão do arquivo é permitida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Conexão com o banco de dados SQLite
def get_db():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(base_dir, 'dados.db')  # Banco na mesma pasta do projeto
    print("🗄️ Banco de dados usado:", db_path)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

# Página principal: lista de pessoas
@app.route('/')
def index():
    conn = get_db()
    pessoas = conn.execute('SELECT * FROM informacoes').fetchall()
    conn.close()
    return render_template('index.html', pessoas=pessoas)

# Página com detalhes de uma pessoa
@app.route('/pessoa/<int:id>')
def pessoa(id):
    conn = get_db()
    pessoa = conn.execute('SELECT * FROM informacoes WHERE id = ?', (id,)).fetchone()
    conn.close()
    return render_template('pessoa.html', pessoa=pessoa)

# Adicionar nova pessoa
@app.route('/adicionar', methods=['GET', 'POST'])
def adicionar():
    if request.method == 'POST':
        nome = request.form['nome']
        acesso = request.form['acesso']
        cargo = request.form['cargo']
        entrada = request.form['entrada']
        saida = request.form['saida']
        acesso_noturno = 1 if 'acesso_noturno' in request.form else 0

        foto = None
        if 'foto' in request.files:
            file = request.files['foto']
            if file and allowed_file(file.filename):
                foto = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], foto))

        conn = get_db()
        conn.execute('''
            INSERT INTO informacoes (nome, acesso, cargo, entrada, saida, acesso_noturno, foto)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (nome, acesso, cargo, entrada, saida, acesso_noturno, foto))
        conn.commit()
        conn.close()

        return redirect('/')
    return render_template('adicionar.html')

# Editar dados de uma pessoa
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
            file = request.files['foto']
            if file and allowed_file(file.filename):
                foto = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], foto))

        conn.execute('''
            UPDATE informacoes
            SET nome=?, acesso=?, cargo=?, entrada=?, saida=?, acesso_noturno=?, foto=?
            WHERE id=?
        ''', (nome, acesso, cargo, entrada, saida, acesso_noturno, foto, id))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('editar.html', pessoa=pessoa)

# Apagar uma pessoa
@app.route('/apagar/<int:id>')
def apagar(id):
    conn = get_db()
    conn.execute('DELETE FROM informacoes WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')

# Servir imagens das fotos
@app.route('/static/fotos/<filename>')
def foto(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Inicialização
if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    print("✔️ Aplicação iniciada!")
    print("📍 Banco de dados em:", os.path.abspath(os.path.join(os.path.dirname(__file__), 'dados.db')))
    app.run(host='0.0.0.0', port=5000, debug=True)