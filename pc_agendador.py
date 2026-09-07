import tkinter as tk
from tkinter import messagebox
import json
import os
import subprocess
from datetime import datetime
import threading

# Configuracao de pastas e arquivo de dados
PASTA_DADOS = "dados"
ARQUIVO_DADOS = os.path.join(PASTA_DADOS, "tasks.json")

os.makedirs(PASTA_DADOS, exist_ok=True)

if not os.path.exists(ARQUIVO_DADOS):
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
        json.dump([], f)

def carregar_tarefas():
    try:
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def salvar_tarefas(tarefas):
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
        json.dump(tarefas, f, indent=4)
    # Roda o sync em uma thread separada para nao travar a interface
    threading.Thread(target=sincronizar_github).start()

def sincronizar_github():
    try:
        status_var.set("Sincronizando com GitHub...")
        root.update_idletasks()
        
        # Puxa alteracoes do celular/nuvem primeiro
        subprocess.run(["git", "pull", "--rebase"], check=False, creationflags=subprocess.CREATE_NO_WINDOW)
        
        # Envia alteracoes locais
        subprocess.run(["git", "add", ARQUIVO_DADOS], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
        mensagem = f"Auto-sync via PC: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        subprocess.run(["git", "commit", "-m", mensagem], check=False, creationflags=subprocess.CREATE_NO_WINDOW)
        subprocess.run(["git", "push"], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
        
        status_var.set("Sincronizado!")
        atualizar_lista()
    except Exception as e:
        status_var.set("Erro no sync. Verifique o Git.")

def adicionar_tarefa():
    titulo = entry_titulo.get()
    if titulo:
        tarefas = carregar_tarefas()
        tarefas.append({"titulo": titulo, "concluida": False, "timestamp": datetime.now().isoformat()})
        salvar_tarefas(tarefas)
        entry_titulo.delete(0, tk.END)
        atualizar_lista()

def atualizar_lista():
    listbox.delete(0, tk.END)
    for t in carregar_tarefas():
        status = "[X]" if t.get("concluida") else "[ ]"
        listbox.insert(tk.END, f"{status} {t['titulo']}")

# Interface Grafica (Tkinter)
root = tk.Tk()
root.title("Agendador PC - Sync GitHub")
root.geometry("400x450")
root.configure(padx=20, pady=20)

tk.Label(root, text="Nova Tarefa:", font=("Arial", 10, "bold")).pack(anchor="w")
entry_titulo = tk.Entry(root, width=40, font=("Arial", 12))
entry_titulo.pack(pady=5, fill="x")

tk.Button(root, text="Adicionar e Sincronizar", command=adicionar_tarefa, bg="#2563eb", fg="white", font=("Arial", 10, "bold")).pack(pady=10, fill="x")

listbox = tk.Listbox(root, font=("Arial", 11), height=12)
listbox.pack(fill="both", expand=True)

status_var = tk.StringVar()
status_var.set("Aguardando...")
tk.Label(root, textvariable=status_var, fg="gray").pack(pady=5)

tk.Button(root, text="Forçar Atualização (Pull/Push)", command=lambda: threading.Thread(target=sincronizar_github).start()).pack(fill="x")

atualizar_lista()
root.mainloop()
