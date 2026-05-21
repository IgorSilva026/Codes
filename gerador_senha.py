# Gerador de Senha com painel 

import random
import string
import tkinter as tk
from tkinter import messagebox

ESPECIAIS = set(string.punctuation)

# ──────────────────────────────────────────────
# Validação
# ──────────────────────────────────────────────

def tem_sequencia_especial(senha: str) -> bool:
    # Retorna True se houver dois ou mais caracteres especiais consecutivos.
    for i in range(len(senha) - 1):
        if senha[i] in ESPECIAIS and senha[i + 1] in ESPECIAIS:
            return True
    return False


def comeca_ou_termina_com_especial(senha: str) -> bool:
    # Retorna True se a senha começar ou terminar com caractere especial.
    return senha[0] in ESPECIAIS or senha[-1] in ESPECIAIS


def senha_valida(senha: str, partes_proibidas: list[str] = []) -> bool:
    # Verifica todas as regras. Retorna True apenas se estiver ok.
    if not (6 <= len(senha) <= 25):
        return False
    if not any(c.islower() for c in senha):
        return False
    if not any(c.isupper() for c in senha):
        return False
    if not any(c in ESPECIAIS for c in senha):
        return False
    if comeca_ou_termina_com_especial(senha):
        return False
    if tem_sequencia_especial(senha):
        return False
    return True


# ──────────────────────────────────────────────
# Geração
# ──────────────────────────────────────────────

def gerar_senha(tamanho: int = 12) -> str:
    # Gera uma senha que respeita as regras. Retorna a senha ou mensagem de erro.

    if not (6 <= tamanho <= 25):
        return "Tamanho inválido (6–25)"

    # Apenas especiais que não causam início/fim problemático sozinhos

    especiais_lista = list(string.punctuation)
    todos = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation

    for _ in range(1000):
        # Garante obrigatórios no meio 
        minuscula  = random.choice(string.ascii_lowercase)
        maiuscula  = random.choice(string.ascii_uppercase)
        especial   = random.choice(especiais_lista)
        numero     = random.choice(string.digits)        # extra, melhora entropia

        # Preenchimento restante com qualquer letra/numero

        restante = random.choices(todos, k=tamanho - 4)

        # Posições do meio (sem índice 0 e último)
        meio = [minuscula, maiuscula, especial, numero] + restante
        random.shuffle(meio)

        # Escolhe início e fim: apenas letras e numeros
        alfanum = string.ascii_letters + string.digits
        inicio = random.choice(alfanum)
        fim    = random.choice(alfanum)

        # Monta senha: início + meio e fim
        meio_cortado = meio[: tamanho - 2]
        senha = inicio + ''.join(meio_cortado) + fim

        if senha_valida(senha):
            return senha

    return "Erro ao gerar senha"


# ──────────────────────────────────────────────
# Interface gráfica
# ──────────────────────────────────────────────

def copiar():
    root.clipboard_clear()
    root.clipboard_append(campo_senha.get())
    btn_copiar.config(text="✔ Copiado!")
    root.after(2000, lambda: btn_copiar.config(text="Copiar"))


def nova_senha():
    try:
        tamanho = int(slider_tamanho.get())
    except ValueError:
        tamanho = 12

    senha = gerar_senha(tamanho)
    campo_senha.config(state="normal")
    campo_senha.delete(0, tk.END)
    campo_senha.insert(0, senha)
    campo_senha.config(state="readonly")
    atualizar_checklist(senha)


def atualizar_checklist(senha: str):
    # Atualiza os ícones do checklist conforme a senha.
    ok  = "✅"
    erro = "❌"

    tamanho_ok = 6 <= len(senha) <= 25
    lbl_tamanho.config(
        text=f"{ok if tamanho_ok else err}  6 a 25 caracteres",
        fg="#a6e3a1" if tamanho_ok else "#f38ba8"
    )

    minus_ok = any(c.islower() for c in senha)
    lbl_minuscula.config(
        text=f"{ok if minus_ok else err}  1 Minúscula",
        fg="#a6e3a1" if minus_ok else "#f38ba8"
    )

    maius_ok = any(c.isupper() for c in senha)
    lbl_maiuscula.config(
        text=f"{ok if maius_ok else err}  1 Maiúscula",
        fg="#a6e3a1" if maius_ok else "#f38ba8"
    )

    esp_ok = any(c in ESPECIAIS for c in senha)
    lbl_especial.config(
        text=f"{ok if esp_ok else err}  1 Caractere especial",
        fg="#a6e3a1" if esp_ok else "#f38ba8"
    )

    borda_ok = not comeca_ou_termina_com_especial(senha)
    lbl_borda.config(
        text=f"{ok if borda_ok else err}  Não começa/termina com especial",
        fg="#a6e3a1" if borda_ok else "#f38ba8"
    )

    seq_ok = not tem_sequencia_especial(senha)
    lbl_seq.config(
        text=f"{ok if seq_ok else err}  Sem especiais consecutivos",
        fg="#a6e3a1" if seq_ok else "#f38ba8"
    )


def atualizar_label_tamanho(val):
    lbl_tam_val.config(text=f"{int(float(val))} caracteres")


# ──────────────────────────────────────────────
# Janela principal
# ──────────────────────────────────────────────

root = tk.Tk()
root.title("Gerador de Senha")
root.geometry("430x490")
root.resizable(False, False)
root.configure(bg="#1e1e2e")

# Título
tk.Label(root, text="🔐 Gerador de Senha para e-mails", font=("Courier", 14, "bold"),
         bg="#1e1e2e", fg="#cdd6f4").pack(pady=(18, 4))

# Tamanho do slider
frame_slider = tk.Frame(root, bg="#1e1e2e")
frame_slider.pack(fill="x", padx=30, pady=(0, 4))
tk.Label(frame_slider, text="Tamanho da senha:", font=("Courier", 9),
         bg="#1e1e2e", fg="#6c7086").pack(anchor="w")
slider_tamanho = tk.Scale(frame_slider, from_=6, to=25, orient="horizontal",
                          command=atualizar_label_tamanho,
                          bg="#1e1e2e", fg="#cdd6f4", troughcolor="#313244",
                          highlightthickness=0, sliderrelief="flat", length=280)
slider_tamanho.set(17)
slider_tamanho.pack(anchor="w")
lbl_tam_val = tk.Label(frame_slider, text="17 caracteres", font=("Courier", 9),
                       bg="#1e1e2e", fg="#89b4fa")
lbl_tam_val.pack(anchor="w")

# Campo em que a senha gerada é exibida

campo_senha = tk.Entry(root, font=("Courier", 13), width=30,
                       justify="center", state="readonly",
                       readonlybackground="#313244", fg="#a6e3a1",
                       relief="flat", bd=5)
campo_senha.pack(pady=8)

# Botões
frame_btn = tk.Frame(root, bg="#1e1e2e")
frame_btn.pack(pady=4)

btn_nova = tk.Button(frame_btn, text="Nova Senha", command=nova_senha,
                     font=("Courier", 10, "bold"), bg="#89b4fa", fg="#1e1e2e",
                     relief="flat", padx=12, pady=6, cursor="hand2")
btn_nova.grid(row=0, column=0, padx=8)

btn_copiar = tk.Button(frame_btn, text="Copiar", command=copiar,
                       font=("Courier", 10, "bold"), bg="#a6e3a1", fg="#1e1e2e",
                       relief="flat", padx=12, pady=6, cursor="hand2")
btn_copiar.grid(row=0, column=1, padx=8)

# Checklist das regras
sep = tk.Frame(root, bg="#45475a", height=1)
sep.pack(fill="x", padx=24, pady=(10, 6))

frame_check = tk.Frame(root, bg="#1e1e2e")
frame_check.pack(fill="x", padx=30)

tk.Label(frame_check, text="Regras da senha:", font=("Courier", 9, "bold"),
         bg="#1e1e2e", fg="#6c7086").pack(anchor="w", pady=(0, 4))

font_check = ("Courier", 9)
lbl_tamanho  = tk.Label(frame_check, text="", font=font_check, bg="#1e1e2e", anchor="w")
lbl_minuscula= tk.Label(frame_check, text="", font=font_check, bg="#1e1e2e", anchor="w")
lbl_maiuscula= tk.Label(frame_check, text="", font=font_check, bg="#1e1e2e", anchor="w")
lbl_especial = tk.Label(frame_check, text="", font=font_check, bg="#1e1e2e", anchor="w")
lbl_borda    = tk.Label(frame_check, text="", font=font_check, bg="#1e1e2e", anchor="w")
lbl_seq      = tk.Label(frame_check, text="", font=font_check, bg="#1e1e2e", anchor="w")

for lbl in (lbl_tamanho, lbl_minuscula, lbl_maiuscula, lbl_especial,
            lbl_borda, lbl_seq):
    lbl.pack(anchor="w", pady=1)

# Geração 
nova_senha()

root.mainloop()
