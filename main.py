import tkinter as tk
from tkinter import ttk, font, messagebox

# Criar a janela principal
janela = tk.Tk()
janela.title("Meu App de Tarefas")
janela.configure(bg="#F0F0F0")
janela.geometry("500x600")

# Variável para armazenar o frame da tarefa que está sendo editada
frame_em_edicao = None

def adicionar_tarefa():
    global frame_em_edicao
    tarefa = entrada_tarefa.get().strip()
    if tarefa and tarefa != "Escreva sua tarefa aqui":
        if frame_em_edicao is not None:
            atualizar_tarefa(tarefa)
            frame_em_edicao = None
        else:
            adicionar_item_tarefa(tarefa)
        entrada_tarefa.delete(0, tk.END)
    else:
        messagebox.showwarning("Entrada Inválida", "Por favor, insira uma tarefa válida.")

def adicionar_item_tarefa(tarefa):
    frame_tarefa = tk.Frame(canvas_interior, bg="white", bd=1, relief=tk.SOLID)

    label_tarefa = tk.Label(frame_tarefa, text=tarefa, font=("Garamond", 16), bg="white", width=25, height=2, anchor="w")
    label_tarefa.pack(side=tk.LEFT, fill=tk.X, padx=10, pady=5)

    botao_editar = tk.Button(frame_tarefa, image=icon_editar, command=lambda f=frame_tarefa, l=label_tarefa: preparar_edicao(f, l), bg="white", relief=tk.FLAT)
    botao_editar.pack(side=tk.RIGHT, padx=5)

    botao_deletar = tk.Button(frame_tarefa, image=icon_deletar, command=lambda f=frame_tarefa: deletar_tarefa(f), bg="white", relief=tk.FLAT)
    botao_deletar.pack(side=tk.RIGHT, padx=5)

    frame_tarefa.pack(fill=tk.X, padx=5, pady=5)

    checkbutton = ttk.Checkbutton(frame_tarefa, command=lambda label=label_tarefa: alternar_sublinhado(label))
    checkbutton.pack(side=tk.RIGHT, padx=5)

    canvas_interior.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

def preparar_edicao(frame_tarefa, label_tarefa):
    global frame_em_edicao
    frame_em_edicao = frame_tarefa
    entrada_tarefa.delete(0, tk.END)
    entrada_tarefa.insert(0, label_tarefa.cget("text"))

def atualizar_tarefa(nova_tarefa):
    global frame_em_edicao
    for widget in frame_em_edicao.winfo_children():
        if isinstance(widget, tk.Label):
            widget.config(text=nova_tarefa)

def deletar_tarefa(frame_tarefa):
    frame_tarefa.destroy()
    canvas_interior.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

def alternar_sublinhado(label):
    fonte_atual = label.cget("font")
    if "underline" in fonte_atual:
        nova_fonte = fonte_atual.replace(" underline", "")
    else:
        nova_fonte = fonte_atual + " underline"
    label.config(font=nova_fonte)

def ao_clicar_entrada(event):
    if entrada_tarefa.get() == "Escreva sua tarefa aqui":
        entrada_tarefa.delete(0, tk.END)
        entrada_tarefa.configure(fg="black")

def ao_sair_foco(event):
    if not entrada_tarefa.get().strip():
        entrada_tarefa.delete(0, tk.END)
        entrada_tarefa.insert(0, "Escreva sua tarefa aqui")
        entrada_tarefa.configure(fg="grey")

def redimensionar_imagem(caminho_arquivo, tamanho=(24, 24)):
    """Redimensiona a imagem usando PhotoImage e retorna o PhotoImage redimensionado"""
    try:
        img = tk.PhotoImage(file=caminho_arquivo)
        img = img.subsample(int(img.width() / tamanho[0]), int(img.height() / tamanho[1]))
        return img
    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível redimensionar o ícone {caminho_arquivo}: {e}")
        return None

# Carregar ícones com redimensionamento
icon_editar = redimensionar_imagem(r"C:\Users\Menezes\OneDrive\Desktop\PROJETOS GERAIS DE PROGRAMAÇÃO\PROJETO 1 - PYTHON\imagens\edit.png")
icon_deletar = redimensionar_imagem(r"C:\Users\Menezes\OneDrive\Desktop\PROJETOS GERAIS DE PROGRAMAÇÃO\PROJETO 1 - PYTHON\imagens\delete.png")

if not icon_editar or not icon_deletar:
    messagebox.showerror("Erro", "Um ou mais ícones não puderam ser carregados. O aplicativo pode não funcionar corretamente.")

# Criar uma fonte para o cabeçalho
fonte_cabecalho = font.Font(family="Garamond", size=24, weight="bold")

# Criar um rótulo de cabeçalho
rotulo_cabecalho = tk.Label(janela, text="Meu App de Tarefas", font=fonte_cabecalho, bg="#F0F0F0", fg="#333")
rotulo_cabecalho.pack(pady=20)

# Frame para a entrada da tarefa e o botão de adicionar
frame = tk.Frame(janela, bg="#F0F0F0")
frame.pack(pady=10)

entrada_tarefa = tk.Entry(frame, font=("Garamond", 14), relief=tk.FLAT, bg="white", fg="grey", width=30)
entrada_tarefa.insert(0, "Escreva sua tarefa aqui")
entrada_tarefa.bind("<FocusIn>", ao_clicar_entrada)
entrada_tarefa.bind("<FocusOut>", ao_sair_foco)
entrada_tarefa.pack(side=tk.LEFT, padx=10)

botao_adicionar = tk.Button(frame, text="Adicionar Tarefa", command=adicionar_tarefa, bg="#4CAF50", fg="white", height=1, width=15, font=("Roboto", 11), relief=tk.FLAT)
botao_adicionar.pack(side=tk.LEFT, padx=10)

# Criar um frame para a lista de tarefas com barra de rolagem
frame_lista_tarefas = tk.Frame(janela, bg="white")
frame_lista_tarefas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
canvas = tk.Canvas(frame_lista_tarefas, bg="white")
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar = ttk.Scrollbar(frame_lista_tarefas, orient="vertical", command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

canvas.configure(yscrollcommand=scrollbar.set)
canvas_interior = tk.Frame(canvas, bg="white")
canvas.create_window((0, 0), window=canvas_interior, anchor="nw")
canvas_interior.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

janela.mainloop()
