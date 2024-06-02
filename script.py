import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import zipfile

def search_files(directory, filename, progress_var, progress_bar, total_dirs):
    result = []
    count = 0
    for root, dirs, files in os.walk(directory):
        if filename in files:
            result.append(os.path.join(root, filename))
        
        count += 1
        progress_var.set(count / total_dirs * 100)
        progress_bar.update()

    return result

def extract_zip(zip_file, extract_to):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

def on_search():
    directory = directory_entry.get()
    filename = filename_entry.get()
    
    if not os.path.isdir(directory):
        messagebox.showerror("Erro", "Diretório inválido")
        return
    
    total_dirs = sum(len(dirs) for _, dirs, _ in os.walk(directory))
    progress_var.set(0)
    progress_bar.update()
    
    results = search_files(directory, filename, progress_var, progress_bar, total_dirs)
    if results:
        result_listbox.delete(0, tk.END)  # Limpa a lista anterior
        for result in results:
            result_listbox.insert(tk.END, result)
        result_listbox.pack(pady=10)  # Exibe a Listbox
        open_button.config(state=tk.NORMAL)
    else:
        result_text.set("Arquivo não encontrado")
        result_listbox.pack_forget()  # Esconde a Listbox
        open_button.config(state=tk.DISABLED)

def select_directory():
    directory = filedialog.askdirectory()
    if directory:
        directory_entry.delete(0, tk.END)
        directory_entry.insert(0, directory)

def open_file():
    selected_index = result_listbox.curselection()
    if selected_index:
        filepath = result_listbox.get(selected_index)
        if filepath.endswith('.zip'):
            try:
                extract_to = os.path.join(os.path.dirname(filepath), 'extracted')
                extract_zip(filepath, extract_to)
                messagebox.showinfo("Sucesso", f"Arquivo ZIP extraído para: {extract_to}")
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível extrair o arquivo ZIP: {e}")
        else:
            try:
                if os.name == 'nt':
                    os.startfile(filepath)
                elif os.name == 'posix':
                    # Tentar diferentes comandos para abrir o arquivo no Linux
                    try:
                        subprocess.call(('xdg-open', filepath))
                    except FileNotFoundError:
                        try:
                            subprocess.call(('gio', 'open', filepath))
                        except FileNotFoundError:
                            try:
                                subprocess.call(('gnome-open', filepath))
                            except FileNotFoundError:
                                try:
                                    subprocess.call(('kde-open', filepath))
                                except FileNotFoundError:
                                    messagebox.showerror("Erro", "Não foi possível abrir o arquivo com xdg-open, gio, gnome-open ou kde-open")
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível abrir o arquivo: {e}")
    else:
        messagebox.showwarning("Aviso", "Nenhum arquivo selecionado")

app = tk.Tk()
app.title("Busca de Arquivos")

# Frame para diretório
directory_frame = tk.Frame(app)
directory_frame.pack(pady=10)
tk.Label(directory_frame, text="Diretório:").pack(side=tk.LEFT)
directory_entry = tk.Entry(directory_frame, width=50)
directory_entry.pack(side=tk.LEFT)
tk.Button(directory_frame, text="Selecionar", command=select_directory).pack(side=tk.LEFT)

# Frame para nome do arquivo
filename_frame = tk.Frame(app)
filename_frame.pack(pady=10)
tk.Label(filename_frame, text="Nome do Arquivo:").pack(side=tk.LEFT)
filename_entry = tk.Entry(filename_frame, width=50)
filename_entry.pack(side=tk.LEFT)

# Botão de busca
search_button = tk.Button(app, text="Buscar", command=on_search)
search_button.pack(pady=10)

# Barra de progresso
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(app, variable=progress_var, maximum=100)
progress_bar.pack(pady=10, fill=tk.X)

# Listbox para mostrar os resultados
result_listbox = tk.Listbox(app, selectmode=tk.SINGLE, width=80, height=10)
result_listbox.pack_forget()  # Inicialmente escondido

# Botão para abrir o arquivo
open_button = tk.Button(app, text="Abrir Arquivo", command=open_file, state=tk.DISABLED)
open_button.pack(pady=10)

# Área de resultados
result_text = tk.StringVar()
result_label = tk.Label(app, textvariable=result_text, justify=tk.LEFT)
result_label.pack(pady=10)

app.mainloop()
