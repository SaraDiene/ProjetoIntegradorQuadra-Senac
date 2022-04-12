

from flask import Flask, redirect, render_template, request, url_for,session
from bancodados import Usuario, Agendamento
import os
from enviar_email import recebe_parametros




app = Flask(__name__)
app.secret_key = os.urandom(16)
grupo_logado = None

@app.route('/')
def abre_pagina_principal():
    if 'username' in session:
        return render_template('agendamento.html',grupo_user = grupo_logado)
    return redirect(url_for('abre_login'))

@app.route('/login')
def abre_login():
    return render_template('login.html', titulo = "Login")

@app.route('/fotos')
def abre_fotos():
    return render_template('espaco.html', titulo = "Galeria")

@app.route('/login', methods = ['POST'])
def realiza_login():
    login = request.form['email']
    senha = request.form['senha']
    usuario_logado = Usuario(None,None,None,login,senha)
    resultado = usuario_logado.verifica_email()
    
    if resultado == True:  
        session['username'] = usuario_logado.email
        global grupo_logado
        grupo_logado = usuario_logado.grupo
        return redirect(url_for('abre_agenda'))  
    else:
        return render_template('login.html', mensagem = 'Usuário ou senha inválido')

@app.route('/logout')
def realiza_logout():
    session.pop('username', None)
    return redirect(url_for('abre_login'))


@app.route('/contato')
def abre_contato():
    return render_template('contato.html', titulo = "Contato")

@app.route('/contato',methods=['POST'])
def envia_email_dados():
    nome_cliente = request.form['nome']
    email_cliente = request.form['email']
    telefone_cliente = request.form['telefone']
    assunto_mensagem = request.form['assunto']
    mensagem_cliente = request.form['mensagem']

    recebe_parametros(assunto_mensagem,nome_cliente,email_cliente,telefone_cliente,mensagem_cliente)
    return render_template('contato.html',mensagem_email = 'Mensagem enviada com sucesso!')

@app.route('/funcionamento')
def abre_funcionamento():
    return render_template('funcionamento.html',titulo = "Funcionamento")


@app.route('/cadastro')
def abre_cadastro():
    return render_template('cadastro.html', titulo = "Cadastro")


@app.route('/cadastro', methods=['POST'])
def salva_cadastro():
    nome_usuario = request.form['nome_cadastro']
    cpf_usuario = request.form['cpf_cadastro']
    telefone_usuario = request.form['tel_cadastro']
    email_usuario = request.form['email_cadastro']
    senha_usuario = request.form['senha_cadastro']
    
    objeto_usuario = Usuario(nome=nome_usuario, cpf=cpf_usuario, telefone=telefone_usuario, email=email_usuario,
                             senha=senha_usuario)
                            
    objeto_usuario.insere_usuario()
    return redirect(url_for('abre_agenda'))

@app.route('/administrador')
def abre_administrador():
    if 'username' in session:
        usuario = Usuario()
        return render_template('administrador.html', lista_usuario = usuario.select_todos_usuarios(),titulo = "Administrador")
    return redirect(url_for('abre_login')) 
    
@app.route('/excluir_usuario', methods = ['POST'])
def exclui_usuario():
    if 'username' in session:
        excluir_usuario = request.form['exclui_usuario']
        objeto_usuario = Usuario()
        objeto_usuario.exclui_usuario(excluir_usuario)
        return redirect(url_for('abre_administrador'))
    return redirect(url_for('abre_login'))    

@app.route('/agenda')
def abre_agenda():
    if 'username' in session:
        return render_template('agendamento.html', titulo = "Agendamento")
    return redirect(url_for('abre_login'))

@app.route('/historico')
def mostra_historico():
    if 'username' in session:
        agenda = Agendamento(None,None, None, None)
        return render_template('historico.html',lista_agenda=agenda.mostra_historico(session['username']), titulo = 'Reservas')
    return redirect(url_for('abre_login'))




@app.route('/excluir_agendamento',methods=['POST'])
def exclui_agendamento():
    if 'username' in session:
        agendamento_excluido = request.form['exclui_agendamento']
        objeto_agendamento = Agendamento()
        objeto_agendamento.exclui_agendamento(agendamento_excluido)
        return redirect(url_for('mostra_historico'))
    return redirect(url_for('abre_login'))


@app.route('/agenda', methods=['POST'])
def salva_agendamento():
    tipo_quadra = request.form['quadra']
    data = request.form['calendario']
    lista_horario = request.form.getlist('horario')

    # verificar se o agendamento ja existe
    invalido = None
    for x in lista_horario:
        objeto_agenda = Agendamento(quadra=tipo_quadra, data=data, hora=x, email = session['username'])
        resultado = objeto_agenda.verifica_agendamento()
        if resultado == False:
            invalido = False
            break
        objeto_agenda.insere_agendamento()
    if invalido == False:
        return render_template('agendamento.html', mensagem = "Horário indisponível, favor selecionar outro horário ou data.")
    return redirect(url_for('finaliza_pagamento'))

@app.route('/pagamento')
def abre_pagamento():
    if 'username' in session:
        objeto_agendamento = Agendamento()
        return render_template('pagamento.html', valor = objeto_agendamento.mostra_valor(session['username']), titulo = "Pagamento")
    return redirect(url_for('abre_login'))


@app.route('/pagamento', methods=["POST"])
def finaliza_pagamento():
    objeto_agendamento = Agendamento()
    objeto_agendamento.finaliza_pagamento(session['username'])
    return redirect(url_for('abre_agenda'))

app.run(debug=True)
