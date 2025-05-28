# imprntnado SQlite
import sqlite3 as lite

# criando conexão com o banco de dados
con = lite.connect('Principal/dados.db')


# create table
with con:
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS formulario (" \
    "id INTEGER PRIMARY KEY AUTOINCREMENT, " \
    "nome TEXT, " \
    "cpf TEXT, " \
    "email TEXT, " \
    "telefone TEXT, " \
    "lgpd TEXT, " \
    "senha TEXT)"
    )