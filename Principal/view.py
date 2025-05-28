# Importando SQlite
import sqlite3 as lite

# criando conexão
con  = lite.connect('Principal/dados.db')

# INSERT
def insert(i):
    with con:
        cur = con.cursor()
        query = "INSERT INTO formulario (nome, cpf, email, telefone, lgpd, senha) VALUES (?, ?, ?, ?, ?, ?)"
        cur.execute(query, i)

# READ
def read_table():
    lista = []
    with con:
        cur = con.cursor()
        query = "SELECT * FROM formulario"
        cur.execute(query)
        dados = cur.fetchall()

        for i in dados:
            lista.append(i)
    return lista
               
# UPDATE
def update(i) :
    with con:
        cur = con.cursor()
        query = "UPDATE formulario SET nome = ?, cpf = ?, email = ?, telefone = ?,lgpd = ?, senha = ? WHERE id = ?"
        cur.execute(query,i)

# DELETE
def delete(i):
    with con:
        cur = con.cursor()
        query = "DELETE FROM formulario WHERE id = ?"
        cur.execute(query,i)