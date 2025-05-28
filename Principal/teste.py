import tkinter as tk
import re

def validar_email(event):
    email = entrada_email.get()

    # Expressão regular simples para validar e-mail
    padrao = r'^[\w\.-]+@[\w\.-]+\.\w{3,}$'

    if re.match(padrao, email):
        label_status.config(text="✅ E-mail válido", fg="green")
    else:
        label_status.config(text="❌ E-mail inválido", fg="red")

# Criar janela
janela = tk.Tk()
janela.title("Validação de E-mail")

# Campo de entrada de e-mail
entrada_email = tk.Entry(janela, font=("Arial", 14), width=30)
entrada_email.pack(pady=10)
entrada_email.bind("<KeyRelease>", validar_email)

# Label para mostrar resultado da validação
label_status = tk.Label(janela, text="", font=("Arial", 12))
label_status.pack()

janela.mainloop()
