import mysql.connector as bd
import criptografia as cp


class BancoDados:
    def __init__(self):
        self.conexao = None

    def get_conexao(self):
        self.conexao = bd.connect(host='localhost',
                                  user="root",
                                  password="Admin@22",
                                  database="db_quadra")
        return self.conexao


class Usuario:
    def __init__(self, nome=None, cpf=None, telefone=None, email=None, senha=None,grupo=0):
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone
        self.email = email
        self.senha = senha
        self.grupo = grupo

    def insere_usuario(self):
        banco = BancoDados()
        conexao = banco.get_conexao()

        COMANDO_INSERT = 'insert into usuarios(nome,cpf,telefone,email,senha,grupo) values (%s,%s,%s,%s,%s,%s)'
        hash_senha = cp.criptografia_senha(self.senha)
        valores = (self.nome, self.cpf, self.telefone, self.email, hash_senha,self.grupo)
        manipulador_sql = conexao.cursor()
        manipulador_sql.execute(COMANDO_INSERT, valores)
        conexao.commit()
        return 'Seu Cadastro foi Realizado com Sucesso'


    def verifica_email(self):
        banco = BancoDados()
        conexao = banco.get_conexao()   

        COMANDO_SELECT = 'select senha from usuarios where email like binary %s '
        valor = (self.email,)
        manipulador_sql = conexao.cursor()
        manipulador_sql.execute(COMANDO_SELECT,valor)
        senha_banco_dados = manipulador_sql.fetchone()
        if senha_banco_dados != None:
            resultado = cp.valida_senha(self.senha,senha_banco_dados[0])
            return resultado
        return False

    def verificacao_email(self):

        banco = BancoDados()
        conexao = banco.get_conexao()   

        COMANDO_SELECT = 'select email from usuarios where email = email;'
        valor = (self.email,)
        manipulador_sql = conexao.cursor()
        manipulador_sql.execute(COMANDO_SELECT,valor)
        email_banco_dados = manipulador_sql.fetchone()
        if email_banco_dados != None:
            resultado = (self.email,email_banco_dados[0])
            return resultado
        return False
        

    
    def select_todos_usuarios(self):

        banco = BancoDados()
        conexao = banco.get_conexao()

        COMANDO_SELECT = " select id,nome,telefone,email,grupo from usuarios "
        manipulador_sql = conexao.cursor()
        manipulador_sql.execute(COMANDO_SELECT)
        resultado = manipulador_sql.fetchall()
        lista = []

        for usuario in resultado:
            objeto_usuarios = Usuario(nome=usuario[1],cpf=None,telefone=usuario[2],email=usuario[3],senha=None,grupo=None)
            lista.append(objeto_usuarios)
        return lista
        '''
    def filtra_contatos_agenda(self,nome):
        banco = BancoDados()
        conexao = banco.get_conexao()
        COMANDO_SELECT = 'select * from usuarios where nome like %s'
        valor = (nome,)
        manipulador = conexao.cursor()
        manipulador.execute(COMANDO_SELECT,valor)
        return manipulador.fetchall()
        '''


    def exclui_usuario(self,email):

        obj_banco = BancoDados()    
        conexao = obj_banco.get_conexao()
        
        COMANDO_DELETE = 'delete from usuarios where email = %s'
        valor = (email,)
        manipulador_sql = conexao.cursor()
        manipulador_sql.execute(COMANDO_DELETE,valor)
        conexao.commit()

        return 'Deletado com Sucesso'

class Agendamento:
    def __init__(self,id_agendamento=None,quadra=None, data=None, hora=None, valor=0, email = None):
        self.id = id_agendamento
        self.tipo_quadra = quadra
        self.data = data
        self.horario = hora
        self.valor = valor
        self.email = email

    def verifica_agendamento(self):
        banco = BancoDados()
        conexao = banco.get_conexao()
        COMANDO_SELECT = 'select tipo_quadra from agenda where tipo_quadra like %s and horario like %s and data = %s'
        valores = (self.tipo_quadra, self.horario, self.data)
        manipulador_sql = conexao.cursor()
        manipulador_sql.execute(COMANDO_SELECT, valores)
 
        dados = manipulador_sql.fetchone()
        print(dados)
        if dados != None:
            return False
        return True


    def insere_agendamento(self):

        banco = BancoDados()
        conexao = banco.get_conexao()

        COMANDO_INSERT = 'insert into agenda(tipo_quadra,data,horario,valor,email) values (%s,%s,%s,%s,%s)'
        valores = (self.tipo_quadra, self.data, self.horario, self.verifica_valor(), self.email)

        manipulador_sql = conexao.cursor()
        manipulador_sql.execute(COMANDO_INSERT, valores)
        conexao.commit()

        return 'Seu Agendamento foi Realizado com Sucesso'

    
    def exclui_agendamento(self,id):
       
        obj_banco = BancoDados()    
        conexao = obj_banco.get_conexao()
        
        COMANDO_DELETE = 'delete from agenda where id = %s'
        valor = (id,)
        manipulador_sql = conexao.cursor()
        manipulador_sql.execute(COMANDO_DELETE,valor)
        conexao.commit()

        return 'Agendamento Deletado com Sucesso'
    

    def verifica_valor(self):

        if self.tipo_quadra == 'Society':
            self.valor = 280.00

        elif self.tipo_quadra == 'Areia':
            self.valor = 170.00

        elif self.tipo_quadra == 'Salão':
            self.valor = 200.00

        elif self.tipo_quadra == 'Vôlei/Peteca':
            self.valor = 150.00

        return self.valor

    def mostra_valor(self,email):
        banco = BancoDados()
        conexao = banco.get_conexao()

        COMANDO_SELECT = "select sum(valor) from agenda where email like %s and pagamento = false"
        valores = (email,)
        manipulador_sql = conexao.cursor()
        manipulador_sql.execute(COMANDO_SELECT,valores)
        valor = manipulador_sql.fetchone()    
        return valor[0]

    def mostra_todos_agendamentos(self):

        banco = BancoDados()
        conexao = banco.get_conexao()

        COMANDO_SELECT = "select id,tipo_quadra,data,horario,format(valor,2,'de_DE'),email from agenda order by data"
        manipulador_sql = conexao.cursor()
        manipulador_sql.execute(COMANDO_SELECT)
        lista_agenda = manipulador_sql.fetchall()
        lista = []
        for agenda in lista_agenda:
            obj_agenda = Agendamento(agenda[0], agenda[1], agenda[2], agenda[3], agenda[4],agenda[5])
            lista.append(obj_agenda)

        return lista

    

    def mostra_historico(self,username):

        banco = BancoDados()
        conexao = banco.get_conexao()
        manipulador_sql = conexao.cursor()

        if username == 'admin@admin.com':
            COMANDO_SELECT = "select id,tipo_quadra,data,horario,format(valor,2,'de_DE'),email from agenda order by data"
            manipulador_sql.execute(COMANDO_SELECT)
        else:
            COMANDO_SELECT = "select id,tipo_quadra,data,horario,format(valor,2,'de_DE'),email from agenda where email like %s order by data"
            valor = (username,)
            manipulador_sql.execute(COMANDO_SELECT,valor)

        lista_agenda = manipulador_sql.fetchall()
        lista = []
        for agenda in lista_agenda:
            obj_agenda = Agendamento(agenda[0], agenda[1], agenda[2], agenda[3], agenda[4],agenda[5])
            lista.append(obj_agenda)

        return lista

    def finaliza_pagamento(self,email):
        banco = BancoDados()
        conexao = banco.get_conexao()
        COMANDO_UPDATE = 'update agenda set pagamento = true where email like %s'
        valor = (email,)
        manipulador_sql = conexao.cursor()
        manipulador_sql.execute(COMANDO_UPDATE,valor)
        conexao.commit()
        return "Finalizado com sucesso"




