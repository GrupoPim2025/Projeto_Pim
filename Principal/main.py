from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import bcrypt
import re


# IMPORT CONEXOES
from view import *


################# cores ###############

co0 = "#f0f3f5"   # Preta
co1 = "#feffff"   # branca
co2 = "#4fa882"   # verde
co3 = "#38576b"   # valor
co4 = "#403d3d"   # letra
co5 = "#e06636"   # - profit
co6 = "#038cfc"   # azul
co7 = "#ef5350"   # vermelha
co8 = "#263238"   # + verde
co9 = "#e9edf5"   # sky blue


# CREATE WINDOW

janela = Tk()
janela.title("GESTÃO DE USUÁRIOS")
janela.geometry("1080x560")
janela.configure(background=co9)
janela.resizable(width=FALSE, height=FALSE)


# GRID FRAMES

frame_Title = Frame(janela, width=330, height=60, bg=co2, relief='flat')
frame_Title.grid(row=0, column=0)

frame_Forms = Frame(janela, width=330, height=510, bg=co1, relief='flat')
frame_Forms.grid(row=1, column=0, sticky=NSEW, padx=0, pady=1)

frame_Results = Frame(janela, width=750, height=560, bg=co1, relief='flat')
frame_Results.grid(row=0, column=1, rowspan=2, padx=1, pady=0, sticky=NSEW)

########################## CONFIG FRAME TITLE ##########################

app_title = Label(frame_Title, text='Formulário de dados',justify='center', font=('Arial 16 bold'), fg= co1, bg=co2, relief='flat')
app_title.place(x=60,y=20)

########################## CONFIG FRAME FOMRS ##########################

# VAR TREE GLOBAL
global tree

# FUNÇÃO DE INSERÇÃO DE DADOS
def inserir():
    nome = e_name.get()
    cpf = e_cpf.get()
    telefone = e_telefone.get()
    email = e_email.get()
    senha = e_passwords.get()
    senhaConfirm = e_passwordsConfirm.get()
    lgpd = ''
    senha_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt())
    lista = [nome, cpf, email, telefone, lgpd, senha_hash]

    if not nome or not cpf or not telefone or not email or not senha or not senhaConfirm:
        messagebox.showerror("Erro", "Preencha todos os campos!") 
    elif senha != senhaConfirm:
        messagebox.showwarning('Erro', 'AS SENHAS NÃO CORRESPONDEM')
    else: 
        # PERGUNTA PARA ACEITAR OS TERMOS DE LGPD
        resposta = messagebox.askyesno("Confirmação", "Você concorda com o compartilhamento de dados?")
        if resposta:

            # ADICIONANDO A RESPOSTA NO DADO LGPD
            lista[4] = 'sim'
            insert(lista)
          
            e_name.delete(0,'end')
            e_cpf.delete(0,'end')
            e_telefone.delete(0,'end')
            e_email.delete(0,'end')
            e_passwords.delete(0,'end')
            e_passwordsConfirm.delete(0,'end')
        else:
            messagebox.OK('CANCELAMENTO DE OPERAÇÃO', 'Sua operação foi cancelada')
            e_name.delete(0,'end')
            e_cpf.delete(0,'end')
            e_telefone.delete(0,'end')
            e_email.delete(0,'end')
            e_passwords.delete(0,'end')
            e_passwordsConfirm.delete(0,'end')
        
        for widget in frame_Results.winfo_children():
            widget.destroy()
        
        label_status.place_forget()
        show_tables()

# FUNÇÃO DE ATUALIZAÇÃO DE DADOS
def atualizar():
    try:
        treev_dados = tree.focus()
        treev_dicionario = tree.item(treev_dados)
        tree_lista = treev_dicionario['values']

        valor_id = tree_lista[0]

        e_name.delete(0,'end')
        e_cpf.delete(0,'end')
        e_email.delete(0,'end')
        e_telefone.delete(0,'end')
        e_passwords.delete(0,'end')
        e_passwordsConfirm.delete(0,'end')

        e_name.insert(0,tree_lista[1])
        e_cpf.insert(0,tree_lista[2])
        e_email.insert(0,tree_lista[3])
        e_telefone.insert(0,tree_lista[4])
        e_passwords.insert(0,tree_lista[6])
        e_passwordsConfirm.insert(0,tree_lista[6])

        def atualizando():

            nome = e_name.get()
            cpf = e_cpf.get()
            email = e_email.get()
            telefone = e_telefone.get()
            senha = e_passwords.get()
            senhaConfirm = e_passwordsConfirm.get()
            lgpd = ''
            senha_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt())
            lista = [nome, cpf, email, telefone, lgpd, senha_hash, valor_id]


            if not nome or not cpf or not telefone or not email or not senha or not senhaConfirm:
                messagebox.showerror("Erro", "Preencha todos os campos!")
            
            elif senha != senhaConfirm:
                messagebox.showwarning('Erro', 'AS SENHAS NÃO CORRESPONDEM')
            else:       
                # PERGUNTA PARA ACEITAR OS TERMOS DE LGPD
                resposta = messagebox.askyesno("Confirmação", "Você concorda com o compartilhamento de dados?")
                if resposta:

                    # ADICIONANDO A RESPOSTA NO DADO LGPD
                    lista[4] = 'sim'
                    update(lista)
                
                    e_name.delete(0,'end')
                    e_cpf.delete(0,'end')
                    e_email.delete(0,'end')
                    e_telefone.delete(0,'end')
                    e_passwords.delete(0,'end')
                    e_passwordsConfirm.delete(0,'end')
                    
                    btn_comfirmar.place_forget()     

                else:
                    messagebox.OK('CANCELAMENTO DE OPERAÇÃO', 'Sua operação foi cancelada')
                    e_name.delete(0,'end')
                    e_cpf.delete(0,'end')
                    e_email.delete(0,'end')
                    e_telefone.delete(0,'end')
                    e_passwords.delete(0,'end')
                    e_passwordsConfirm.delete(0,'end')
                
                for widget in frame_Results.winfo_children():
                    widget.destroy()
                
                label_status.place_forget()
                show_tables()   

        # Botão Atualizar
        btn_comfirmar = Button(frame_Forms,command=atualizando, text='Confirmar',width=10, justify='center',font=('Arial 8 bold'), fg= co1, bg=co3, relief='raised', overrelief='ridge')
        btn_comfirmar.place(x=120,y=440)


    except IndexError:
        messagebox.showerror("Erro", "Selecione um dos dados na tabela")

# FUNÇÃO DELETE
def deletar():
    try:
        treev_dados = tree.focus()
        treev_dicionario = tree.item(treev_dados)
        tree_lista = treev_dicionario['values']

        valor_id = [tree_lista[0]]
        
        resposta = messagebox.askyesno('Cuidado', 'Deseja realmente deletar esses dados?')
        if resposta == True:
            #deleta no banco de dados
            delete(valor_id)
            messagebox.showinfo('Sucesso', 'Os dados foram deletado com sucesso')

            e_name.delete(0,'end')
            e_cpf.delete(0,'end')
            e_email.delete(0,'end')
            e_telefone.delete(0,'end')
            e_passwords.delete(0,'end')
            e_passwordsConfirm.delete(0,'end')
            
            for widget in frame_Results.winfo_children():
                widget.destroy()
            
            label_status.place_forget()
            show_tables()

        else:
            messagebox.showinfo('Cancelamento', 'Operação cancelada')     

    except IndexError:
        messagebox.showerror("Erro", "Dados não deletados")

# FORMATAÇÃO DO CAMPO CPF
def formatar_cpf(event):

    texto = e_cpf.get().replace(".", "").replace("-", "")

    
    if not texto.isdigit():
        texto = ''.join(filter(str.isdigit, texto))  # remove letras e símbolos

    novo_texto = ''
    if len(texto) > 0:
        novo_texto += texto[:3]
    if len(texto) >= 4:
        novo_texto += '.' + texto[3:6]
    if len(texto) >= 7:
        novo_texto += '.' + texto[6:9]
    if len(texto) >= 10:
        novo_texto += '-' + texto[9:11]
    
    e_cpf.delete(0, 'end')
    e_cpf.insert(0,novo_texto)

# VALIDAR E-MAIL
def validar_email(event):
    email = e_email.get()

    # Expressão regular simples para validar e-mail
    padrao = r'^[\w\.-]+@[\w\.-]+\.\w{3,}$'

    if re.match(padrao, email):
        label_status.config(text="✅ E-mail válido", fg="green")
    else:
        label_status.config(text="❌ E-mail inválido", fg="red")

    label_status.pack_forget()
    
# FORMATAÇÃO DO CAMPO TELEFONE
def formatar_telefone(event):
    texto = e_telefone.get()
    texto = ''.join(filter(str.isdigit, texto))  # remove tudo que não for número

    novo_texto = ''
    if len(texto) >= 1:
        novo_texto += '(' + texto[:2]  # DDD
    if len(texto) >= 3:
        novo_texto += ') ' + texto[2:7]  # Primeira parte do número
    if len(texto) >= 8:
        novo_texto += '-' + texto[7:11]  # Últimos 4 dígitos

    e_telefone.delete(0, 'end')
    e_telefone.insert(0, novo_texto)

# NOME
l_name = Label(frame_Forms, text='Nome:', anchor=NW, font=('Arial 13 bold'), fg= co4, bg=co1, relief='flat')
l_name.place(x=10,y=10)
e_name = Entry(frame_Forms, width=49, justify='left', relief='solid')
e_name.place(x=10,y=40)

# CPF
l_cpf = Label(frame_Forms, text='CPF', anchor=NW, font=('Arial 13 bold'), fg= co4, bg=co1, relief='flat')
l_cpf.place(x=10,y=70)
l_cpf = Label(frame_Forms, text='(sem digítos ou pontos):', anchor=NW, font=('Arial 10'), fg= co4, bg=co1, relief='flat')
l_cpf.place(x=50,y=70)
e_cpf = Entry(frame_Forms, width=49, justify='left', relief='solid')
e_cpf.place(x=10,y=100)
# Formatar a cada tecla pressionada
e_cpf.bind("<KeyRelease>", formatar_cpf)

# EMAIL
l_email = Label(frame_Forms, text='E-mail:', anchor=NW, font=('Arial 13 bold'), fg= co4, bg=co1, relief='flat')
l_email.place(x=10,y=130)
# Label para mostrar resultado da validação
label_status = Label(frame_Forms, text="", font=("Arial", 8), fg= co4, bg=co1, relief='flat')
label_status.place(x=70,y=134)
# CONT EMAIL
e_email = Entry(frame_Forms, width=49, justify='left', relief='solid')
e_email.place(x=10,y=160)
# VALIDAÇÃO E-MAIL
e_email.bind("<FocusOut>",validar_email)

# TELEFONE
l_telefone = Label(frame_Forms, text='Telefone', anchor=NW, font=('Arial 13 bold'), fg= co4, bg=co1, relief='flat')
l_telefone.place(x=10,y=190) #190
l_telefone = Label(frame_Forms, text='(sem digítos ou pontos):', anchor=NW, font=('Arial 10'), fg= co4, bg=co1, relief='flat')
l_telefone.place(x=85,y=190)
e_telefone = Entry(frame_Forms, width=49, justify='left', relief='solid')
e_telefone.place(x=10,y=220) #220
# Formatar a cada tecla pressionada
e_telefone.bind("<KeyRelease>", formatar_telefone)

# Senha
l_passwords = Label(frame_Forms, text='Senha:', anchor=NW, font=('Arial 13 bold'), fg= co4, bg=co1, relief='flat')
l_passwords.place(x=10,y=250)
e_passwords = Entry(frame_Forms, width=49, justify='left', relief='solid', show='*') 
e_passwords.place(x=10,y=280)

# Confirma Senha
l_passwordsConfirm = Label(frame_Forms, text='Confirmar a senha:', anchor=NW, font=('Arial 13 bold'), fg= co4, bg=co1, relief='flat')
l_passwordsConfirm.place(x=10,y=310)
e_passwordsConfirm = Entry(frame_Forms, width=49, justify='left', relief='solid', show='*')
e_passwordsConfirm.place(x=10,y=340)

# Botão Inserir
btn_insert = Button(frame_Forms, command=inserir , text='INSERIR',width=10, justify='center',font=('Arial 9 bold'), fg= co1, bg=co6, relief='raised', overrelief='ridge')
btn_insert.place(x=10,y=400)

# Botão Atualizar
btn_update = Button(frame_Forms,command=atualizar, text='ATUALIZAR',width=10, justify='center',font=('Arial 9 bold'), fg= co1, bg=co3, relief='raised', overrelief='ridge')
btn_update.place(x=120,y=400)

# Botão Deletar
btn_delete = Button(frame_Forms,command=deletar, text='DELETAR',width=10, justify='center',font=('Arial 9 bold'), fg= co1, bg=co7, relief='raised', overrelief='ridge')
btn_delete.place(x=230,y=400)

########################## CONFIGURAÇÃO DAS TABELAS ##########################

# MOSTRAR A TABLEA
def show_tables():
    global tree

    # LISTA BASICA PARA INCREMENTAR
    lista = read_table()

    # LISTA PARA FAZER O CABEÇALHO
    tabela_head = ['ID','Nome','CPF','E-mail',"Telefone","LGPD","Senha"]

    #df_list = lista

    # CRIANDO A TABELA
    tree = ttk.Treeview(frame_Results, selectmode='extended', columns=tabela_head, show='headings')

    # Scroll vertical
    vsb = ttk.Scrollbar(frame_Results, orient="vertical", command=tree.yview)

    # Scroll horizontal
    hsb = ttk.Scrollbar(frame_Results, orient="horizontal", command=tree.yview)

    # CONFIGURAÇÃO DAS COLINAS
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    tree.grid(column=0, row=0, sticky='nsew')
    vsb.grid(column=1, row=0, sticky='ns')
    hsb.grid(column=0, row=1, sticky='ew')

    frame_Results.grid_rowconfigure(0, weight=12)


    hd=["nw","nw","nw","nw","nw","center","center"]
    h=[30,170,100,170,95,55,100]
    n=0

    for col in tabela_head:
        tree.heading(col, text=col.title(), anchor=CENTER)
        # adjust the column's width to the header string
        tree.column(col, width=h[n],anchor=hd[n])
        
        n+=1

    for item in lista:
        tree.insert('', 'end', values=item)

show_tables()
janela.mainloop()