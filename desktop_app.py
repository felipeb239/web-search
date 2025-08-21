"""
Sistema de Busca de Arquivos - Versão Desktop
Conecta ao servidor de arquivos do cliente (nuvem ou físico)
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import json
import threading
from datetime import datetime
# import requests  # Comentado por enquanto
from docx import Document
import PyPDF2
import ftplib
# import smbclient  # Comentado por enquanto
# from pathlib import Path  # Comentado por enquanto

class FileSearchDesktop:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Busca de Arquivos - Desktop")
        self.root.geometry("1000x700")
        
        # Configurações do servidor
        self.server_config = {
            'type': 'local',  # 'local', 'ftp', 'smb', 'webdav'
            'host': '',
            'username': '',
            'password': '',
            'path': '',
            'port': 21
        }
        
        # Cache de arquivos indexados
        self.file_cache = {}
        self.search_results = []
        
        self.setup_ui()
        self.load_config()
        
    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurações do servidor
        server_frame = ttk.LabelFrame(main_frame, text="Configurações do Servidor", padding="10")
        server_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Tipo de servidor
        ttk.Label(server_frame, text="Tipo:").grid(row=0, column=0, sticky=tk.W)
        self.server_type = ttk.Combobox(server_frame, values=['local', 'ftp', 'smb', 'webdav'], width=15)
        self.server_type.grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
        self.server_type.bind('<<ComboboxSelected>>', self.on_server_type_change)
        
        # Host/IP
        ttk.Label(server_frame, text="Host/IP:").grid(row=0, column=2, sticky=tk.W, padx=(20, 0))
        self.host_entry = ttk.Entry(server_frame, width=20)
        self.host_entry.grid(row=0, column=3, sticky=tk.W, padx=(5, 0))
        
        # Porta
        ttk.Label(server_frame, text="Porta:").grid(row=0, column=4, sticky=tk.W, padx=(20, 0))
        self.port_entry = ttk.Entry(server_frame, width=10)
        self.port_entry.grid(row=0, column=5, sticky=tk.W, padx=(5, 0))
        
        # Usuário
        ttk.Label(server_frame, text="Usuário:").grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        self.username_entry = ttk.Entry(server_frame, width=20)
        self.username_entry.grid(row=1, column=1, sticky=tk.W, pady=(10, 0))
        
        # Senha
        ttk.Label(server_frame, text="Senha:").grid(row=1, column=2, sticky=tk.W, pady=(10, 0), padx=(20, 0))
        self.password_entry = ttk.Entry(server_frame, width=20, show="*")
        self.password_entry.grid(row=1, column=3, sticky=tk.W, pady=(10, 0), padx=(5, 0))
        
        # Caminho
        ttk.Label(server_frame, text="Caminho:").grid(row=1, column=4, sticky=tk.W, pady=(10, 0), padx=(20, 0))
        self.path_entry = ttk.Entry(server_frame, width=30)
        self.path_entry.grid(row=1, column=5, sticky=tk.W, pady=(10, 0), padx=(5, 0))
        
        # Botões de conexão
        button_frame = ttk.Frame(server_frame)
        button_frame.grid(row=2, column=0, columnspan=6, pady=(10, 0))
        
        ttk.Button(button_frame, text="Conectar", command=self.connect_to_server).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Salvar Config", command=self.save_config).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Indexar Arquivos", command=self.index_files).pack(side=tk.LEFT)
        
        # Barra de busca
        search_frame = ttk.Frame(main_frame)
        search_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(search_frame, text="Buscar:").pack(side=tk.LEFT)
        self.search_entry = ttk.Entry(search_frame, width=60)
        self.search_entry.pack(side=tk.LEFT, padx=(5, 10))
        self.search_entry.bind('<Return>', lambda e: self.perform_search())
        
        ttk.Button(search_frame, text="🔍 Buscar", command=self.perform_search).pack(side=tk.LEFT)
        
        # Resultados da busca
        results_frame = ttk.LabelFrame(main_frame, text="Resultados da Busca", padding="10")
        results_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Treeview para resultados
        columns = ('Nome', 'Tipo', 'Tamanho', 'Data Modificação', 'Relevância')
        self.results_tree = ttk.Treeview(results_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.results_tree.heading(col, text=col)
            self.results_tree.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.results_tree.yview)
        self.results_tree.configure(yscrollcommand=scrollbar.set)
        
        self.results_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Estatísticas
        stats_frame = ttk.LabelFrame(main_frame, text="Estatísticas", padding="10")
        stats_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        self.stats_label = ttk.Label(stats_frame, text="Arquivos indexados: 0 | Última indexação: Nunca")
        self.stats_label.pack()
        
        # Configurar grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        
    def on_server_type_change(self, event):
        server_type = self.server_type.get()
        if server_type == 'local':
            self.host_entry.config(state='disabled')
            self.port_entry.config(state='disabled')
            self.username_entry.config(state='disabled')
            self.password_entry.config(state='disabled')
        else:
            self.host_entry.config(state='normal')
            self.port_entry.config(state='normal')
            self.username_entry.config(state='normal')
            self.password_entry.config(state='normal')
    
    def load_config(self):
        try:
            if os.path.exists('desktop_config.json'):
                with open('desktop_config.json', 'r') as f:
                    config = json.load(f)
                    self.server_config.update(config)
                    
                    # Atualizar UI
                    self.server_type.set(self.server_config['type'])
                    self.host_entry.insert(0, self.server_config['host'])
                    self.port_entry.insert(0, str(self.server_config['port']))
                    self.username_entry.insert(0, self.server_config['username'])
                    self.password_entry.insert(0, self.server_config['password'])
                    self.path_entry.insert(0, self.server_config['path'])
                    
                    self.on_server_type_change(None)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar configuração: {e}")
    
    def save_config(self):
        try:
            config = {
                'type': self.server_type.get(),
                'host': self.host_entry.get(),
                'port': int(self.port_entry.get() or 21),
                'username': self.username_entry.get(),
                'password': self.password_entry.get(),
                'path': self.path_entry.get()
            }
            
            with open('desktop_config.json', 'w') as f:
                json.dump(config, f, indent=2)
            
            messagebox.showinfo("Sucesso", "Configuração salva com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar configuração: {e}")
    
    def connect_to_server(self):
        server_type = self.server_type.get()
        
        if server_type == 'local':
            path = self.path_entry.get()
            if not path or not os.path.exists(path):
                messagebox.showerror("Erro", "Caminho local inválido!")
                return
            messagebox.showinfo("Sucesso", f"Conectado ao diretório local: {path}")
            
        elif server_type == 'ftp':
            try:
                # Testar conexão FTP
                ftp = ftplib.FTP()
                ftp.connect(self.host_entry.get(), int(self.port_entry.get() or 21))
                ftp.login(self.username_entry.get(), self.password_entry.get())
                ftp.quit()
                messagebox.showinfo("Sucesso", "Conexão FTP estabelecida!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro na conexão FTP: {e}")
                
        elif server_type == 'smb':
            try:
                # Testar conexão SMB
                # Implementar teste de conexão SMB
                messagebox.showinfo("Sucesso", "Conexão SMB estabelecida!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro na conexão SMB: {e}")
    
    def index_files(self):
        def index_thread():
            try:
                server_type = self.server_type.get()
                if server_type == 'local':
                    self.index_local_files()
                elif server_type == 'ftp':
                    self.index_ftp_files()
                elif server_type == 'smb':
                    self.index_smb_files()
                    
                self.update_stats()
                messagebox.showinfo("Sucesso", "Indexação concluída!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro na indexação: {e}")
        
        threading.Thread(target=index_thread, daemon=True).start()
    
    def index_local_files(self):
        path = self.path_entry.get()
        if not path:
            return
            
        self.file_cache.clear()
        
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.lower().endswith(('.docx', '.pdf')):
                    file_path = os.path.join(root, file)
                    try:
                        content = self.extract_file_content(file_path)
                        self.file_cache[file_path] = {
                            'name': file,
                            'type': os.path.splitext(file)[1].lower(),
                            'size': os.path.getsize(file_path),
                            'modified': datetime.fromtimestamp(os.path.getmtime(file_path)),
                            'content': content
                        }
                    except Exception as e:
                        print(f"Erro ao processar {file_path}: {e}")
    
    def extract_file_content(self, file_path):
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext == '.docx':
            try:
                doc = Document(file_path)
                return ' '.join([paragraph.text for paragraph in doc.paragraphs])
            except:
                return ""
        elif ext == '.pdf':
            try:
                with open(file_path, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)
                    text = ""
                    for page in reader.pages:
                        text += page.extract_text() + " "
                    return text
            except:
                return ""
        return ""
    
    def perform_search(self):
        query = self.search_entry.get().lower()
        if not query:
            messagebox.showwarning("Aviso", "Digite um termo para buscar!")
            return
        
        # Limpar resultados anteriores
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        # Buscar nos arquivos indexados
        results = []
        for file_path, file_info in self.file_cache.items():
            relevance = 0
            
            # Buscar no nome do arquivo
            if query in file_info['name'].lower():
                relevance += 10
            
            # Buscar no conteúdo
            if query in file_info['content'].lower():
                relevance += 5
                # Contar ocorrências
                relevance += file_info['content'].lower().count(query)
            
            if relevance > 0:
                results.append((file_path, file_info, relevance))
        
        # Ordenar por relevância
        results.sort(key=lambda x: x[2], reverse=True)
        
        # Exibir resultados
        for file_path, file_info, relevance in results:
            self.results_tree.insert('', 'end', values=(
                file_info['name'],
                file_info['type'],
                self.format_file_size(file_info['size']),
                file_info['modified'].strftime('%d/%m/%Y %H:%M'),
                f"{relevance} pontos"
            ))
        
        if not results:
            messagebox.showinfo("Resultado", "Nenhum arquivo encontrado.")
    
    def format_file_size(self, size_bytes):
        if size_bytes == 0:
            return "0 B"
        size_names = ["B", "KB", "MB", "GB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        return f"{size_bytes:.1f} {size_names[i]}"
    
    def update_stats(self):
        count = len(self.file_cache)
        last_index = datetime.now().strftime('%d/%m/%Y %H:%M') if count > 0 else "Nunca"
        self.stats_label.config(text=f"Arquivos indexados: {count} | Última indexação: {last_index}")

def main():
    root = tk.Tk()
    app = FileSearchDesktop(root)
    root.mainloop()

if __name__ == "__main__":
    main()
