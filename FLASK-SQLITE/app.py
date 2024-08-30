from flask import Flask, render_template, url_for, request, redirect
import sqlite3

app = Flask(__name__)

def obter_conexao():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = obter_conexao()
    name_user = conn.execute('SELECT * FROM usuarios').fetchall()

    return render_template('pages/index.html', name_user=name_user)

@app.route('/create', methods=['GET','POST'])
def create_user():
    if request.method == 'POST':
        name = request.form['name']
        conn = obter_conexao()
        conn.execute("INSERT INTO usuarios(nome) VALUES(?)", (name,))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('pages/create-user.html')

@app.route('/get_user', methods=['GET', 'POST']) # Visualizar um usuário
def get_user():
    if request.method == 'POST':
        return redirect(url_for('index')) # URL_FOR é para rodar uma FUNÇÃO

    return render_template ('pages/get-user.html')

@app.route('/<usuario>')
def visualizar_usuario(usuario):
    identidade = usuario 
    
    conn = obter_conexao()
    user = conn.execute("SELECT * FROM usuarios WHERE id=?", (identidade,)).fetchone()
    
    return render_template('pages/individual.html', identidade=identidade, user=user)

@app.route('/create_peca', methods=['GET', 'POST'])
def create_peca():
    if request.method == 'POST':
        nome_peca = request.form['peca']
        conn = obter_conexao()
        conn.execute("INSERT INTO pecas(nome_peca) VALUES(?)", (nome_peca,))
        conn.commit()
        conn.close()

    return render_template('/pages/create-peca.html')

@app.route('/ver_peca')
def ver_peca():
    conn = obter_conexao()
    nome_peca = conn.execute('SELECT * FROM pecas').fetchall()

    return render_template('pages/ver-peca.html', nome_peca=nome_peca)

@app.route('/ver_peca/<idpeca>')
def visualizar_peca(idpeca):
    identidade_peca = idpeca

    conn = obter_conexao()
    nome_peca = conn.execute("SELECT * FROM pecas WHERE id=?", (identidade_peca,))
    
    return render_template('pages/ver-peca.html', identidade_peca=identidade_peca, nome_peca=nome_peca)

@app.route('/remover_peca/<idepeca>')
def remover_peca(idepeca):
    identidade_peca = idepeca 

    conn = obter_conexao()
    conn.execute("DELETE FROM pecas WHERE id=?", (identidade_peca,))
    conn.commit()
    conn.close()

    return redirect(url_for('ver_peca'))

@app.route('/create_danca')
def create_danca():
    return render_template('pages/create-danca.html')