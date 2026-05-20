# Gerador de Senha com painel visual

import random
import string
import tkinter as tk
from tkinter import messagebox


def gerar_senha(tamanho=12):
    if tamanho < 8 or tamanho > 25:
        return "Tamanho inválido (8–25)"

    minusculas = random.choice(string.ascii_lowercase)
    maiusculas = random.choice(string.ascii_uppercase)
    numeros = random.choice(string.digits)
    especiais = random.choice(string.punctuation)

    todos = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation

    senha = [minusculas, maiusculas, numeros, especiais]
    senha += random.choices(todos, k=tamanho - 4)

    random.shuffle(senha)
    return ''.join(senha)


def copiar():
    root.clipboard_clear()
    root.clipboard_append(campo_senha.get())
    btn_copiar.config(text="✔ Copiado!")
    root.after(2000, lambda: btn_copiar.config(text="Copiar"))


def nova_senha():
    senha = gerar_senha(12)
    campo_senha.config(state="normal")
    campo_senha.delete(0, tk.END)
    campo_senha.insert(0, senha)
    campo_senha.config(state="readonly")


# Janela principal
root = tk.Tk()
root.title("Gerador de Senha")
root.geometry("380x180")
root.resizable(False, False)
root.configure(bg="#1e1e2e")

# Título
tk.Label(root, text="🔐 Gerador de Senha", font=("Courier", 14, "bold"),
         bg="#1e1e2e", fg="#cdd6f4").pack(pady=(20, 10))

# Campo da senha
campo_senha = tk.Entry(root, font=("Courier", 13), width=28,
                       justify="center", state="readonly",
                       readonlybackground="#313244", fg="#a6e3a1",
                       relief="flat", bd=5)
campo_senha.pack(pady=5)

# Frame dos botões
frame = tk.Frame(root, bg="#1e1e2e")
frame.pack(pady=12)

btn_nova = tk.Button(frame, text="Nova Senha", command=nova_senha,
                     font=("Courier", 10, "bold"), bg="#89b4fa", fg="#1e1e2e",
                     relief="flat", padx=12, pady=6, cursor="hand2")
btn_nova.grid(row=0, column=0, padx=8)

btn_copiar = tk.Button(frame, text="Copiar", command=copiar,
                       font=("Courier", 10, "bold"), bg="#a6e3a1", fg="#1e1e2e",
                       relief="flat", padx=12, pady=6, cursor="hand2")
btn_copiar.grid(row=0, column=1, padx=8)

# Gera senha ao abrir
nova_senha()

root.mainloop()
