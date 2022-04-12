import smtplib
from email.message import EmailMessage



EMAIL_LOGIN = 'quadrasoccerbrasil@gmail.com'
EMAIL_SENHA = '******'

def recebe_parametros(assunto,nome,email,telefone,informacoes):
    criar_email = f'Nome: {nome}\nEmail: {email}\nTelefone: {telefone}\n{informacoes}'

    mensagem = EmailMessage()
    mensagem['Subject'] = assunto
    mensagem['To'] = 'quadrasoccerbrasil@gmail.com'
    mensagem['From'] = nome
    mensagem.set_content(criar_email)

    with smtplib.SMTP_SSL('smtp.gmail.com',465) as servidor:
        servidor.login(EMAIL_LOGIN, EMAIL_SENHA)
        servidor.send_message(mensagem)
