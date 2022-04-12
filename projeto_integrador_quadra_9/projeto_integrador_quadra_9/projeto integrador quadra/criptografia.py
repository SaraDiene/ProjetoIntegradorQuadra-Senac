import bcrypt 

def criptografia_senha(senha):
    senha = senha.encode('utf_8')
    senha_crypt = bcrypt.hashpw(senha,bcrypt.gensalt())

    return senha_crypt

def valida_senha(senha, hash_senha):
    senha = senha.encode('utf-8')
    hash_senha = hash_senha.encode('utf-8')
    resultado = bcrypt.checkpw(senha,hash_senha)
    return(resultado)