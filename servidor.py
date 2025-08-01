import os
import sqlite3
import os
print("Banco de dados salvo em:", os.path.abspath("dados.db"))
from flask import Flask, render_template, request, redirect, send_from_directory, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/fotos'
app.config['MAX_CONTENT_LENGTH'] = 3 * 1024 * 1024  # Máximo 3MB
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Verifica se extensão é permitida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Conecta à base de dados
def get_db():
    conn = sqlite3.connect('dados.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db()
    pessoas = conn.execute('SELECT * FROM informacoes').fetchall()
    conn.close()
    return render_template('index.html', pessoas=pessoas)

@app.route('/pessoa/<int:id>')
def pessoa(id):
    conn = get_db()
    pessoa = conn.execute('SELECT * FROM informacoes WHERE id = ?', (id,)).fetchone()
    conn.close()
    return render_template('pessoa.html', pessoa=pessoa)

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

@app.route('/apagar/<int:id>')
def apagar(id):
    conn = get_db()
    conn.execute('DELETE FROM informacoes WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/static/fotos/<filename>')
def foto(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(host='0.0.0.0', port=port, debug=True)