"""
Sistema de Busca de Arquivos Desktop - ULTRA ROBUSTO
Versão com visualizador de arquivos e botão STOP
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import json
import threading
from datetime import datetime, timedelta
import traceback
from docx import Document
import PyPDF2
import re

class AdvancedFileSearchDesktop:
    def __init__(self, root):
        self.root = root
        self.root.title("🔍 Sistema de Busca de Arquivos - ULTRA ROBUSTO")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 800)
        
        # Variáveis de controle
        self.is_indexing = False
        self.cache_file = "file_cache.json"
        self.indexing_progress = 0
        self.total_files_to_process = 0
        self.processed_files = 0
        
        # Cache de arquivos
        self.file_cache = {}
        self.load_file_cache()
        
        # Configurações
        self.config_file = "advanced_config.json"
        self.load_config()
        
        # Configurar interface
        self.setup_ui()
        self.setup_styles()
        
        # Iniciar timer de atualização da UI
        self.update_ui_timer()
        
        # Verificar configuração inicial
        self.check_initial_config()

    def setup_styles(self):
        """Configura estilos da interface"""
        style = ttk.Style()
        
        # Estilos para labels
        style.configure('Title.TLabel', font=('Segoe UI', 16, 'bold'))
        style.configure('Header.TLabel', font=('Segoe UI', 12, 'bold'))
        style.configure('Info.TLabel', font=('Segoe UI', 9))
        
        # Estilos para botões
        style.configure('Search.TButton', font=('Segoe UI', 10, 'bold'), padding=10)
        style.configure('Action.TButton', font=('Segoe UI', 9), padding=5)
        style.configure('Stop.TButton', font=('Segoe UI', 9, 'bold'), padding=5, foreground='red')
        
        # Estilos para frames
        style.configure('TLabelframe', font=('Segoe UI', 10, 'bold'))
        
    def setup_ui(self):
        """Configura a interface principal"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame superior - Busca e ações
        top_frame = ttk.Frame(main_frame)
        top_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Campo de busca
        search_frame = ttk.Frame(top_frame)
        search_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Label(search_frame, text="Buscar:", style='Header.TLabel').pack(side=tk.LEFT)
        self.search_entry = ttk.Entry(search_frame, width=50, font=('Segoe UI', 10))
        self.search_entry.pack(side=tk.LEFT, padx=(10, 10))
        self.search_entry.bind('<Return>', lambda e: self.perform_search())
        
        ttk.Button(search_frame, text="🔍 Buscar", command=self.perform_search, 
                  style='Search.TButton').pack(side=tk.LEFT)
        
        # Botões de ação
        action_frame = ttk.Frame(top_frame)
        action_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        ttk.Button(action_frame, text="🛑 Parar", command=self.stop_indexing, 
                  style='Stop.TButton').pack(side=tk.TOP, pady=(0, 5))
        ttk.Button(action_frame, text="🧹 Limpar Cache", command=self.clear_cache, 
                  style='Action.TButton').pack(side=tk.TOP, pady=(0, 5))
        ttk.Button(action_frame, text="⚙️ Configurar", command=self.show_config_dialog, 
                  style='Action.TButton').pack(side=tk.TOP, pady=(0, 5))
        ttk.Button(action_frame, text="🔄 Atualizar", command=self.refresh_files, 
                  style='Action.TButton').pack(side=tk.TOP, pady=(0, 5))
        
        # Frame de conteúdo principal
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Painel esquerdo - Filtros e estatísticas
        left_frame = ttk.Frame(content_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Filtros de busca
        filters_frame = ttk.LabelFrame(left_frame, text="🔍 Refinar Busca", padding="10")
        filters_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Filtro por data
        date_frame = ttk.Frame(filters_frame)
        date_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(date_frame, text="📅 Data:", style='Header.TLabel').pack(anchor=tk.W)
        self.date_filter = tk.StringVar(value="all")
        
        ttk.Radiobutton(date_frame, text="Todas as datas", variable=self.date_filter, 
                       value="all", command=self.apply_filters).pack(anchor=tk.W)
        ttk.Radiobutton(date_frame, text="Últimos 7 dias", variable=self.date_filter, 
                       value="7days", command=self.apply_filters).pack(anchor=tk.W)
        ttk.Radiobutton(date_frame, text="Últimos 30 dias", variable=self.date_filter, 
                       value="30days", command=self.apply_filters).pack(anchor=tk.W)
        ttk.Radiobutton(date_frame, text="Último ano", variable=self.date_filter, 
                       value="1year", command=self.apply_filters).pack(anchor=tk.W)
        
        # Filtro por tipo
        type_frame = ttk.Frame(filters_frame)
        type_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(type_frame, text="📄 Tipo de Arquivo:", style='Header.TLabel').pack(anchor=tk.W)
        self.type_filter = tk.StringVar(value="all")
        
        ttk.Radiobutton(type_frame, text="Todos os tipos", variable=self.type_filter, 
                       value="all", command=self.apply_filters).pack(anchor=tk.W)
        ttk.Radiobutton(type_frame, text="Documentos (.docx, .pdf)", variable=self.type_filter, 
                       value="documents", command=self.apply_filters).pack(anchor=tk.W)
        ttk.Radiobutton(type_frame, text="Imagens (.jpg, .png)", variable=self.type_filter, 
                       value="images", command=self.apply_filters).pack(anchor=tk.W)
        ttk.Radiobutton(type_frame, text="Arquivos compactados", variable=self.type_filter, 
                       value="archives", command=self.apply_filters).pack(anchor=tk.W)
        
        # Filtro por pasta
        folder_frame = ttk.Frame(filters_frame)
        folder_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(folder_frame, text="📁 Pasta do Sistema:", style='Header.TLabel').pack(anchor=tk.W)
        self.folder_filter = tk.StringVar(value="all")
        
        ttk.Radiobutton(folder_frame, text="Todas as pastas", variable=self.folder_filter, 
                       value="all", command=self.apply_filters).pack(anchor=tk.W)
        ttk.Radiobutton(folder_frame, text="Documentos", variable=self.folder_filter, 
                       value="documents", command=self.apply_filters).pack(anchor=tk.W)
        ttk.Radiobutton(folder_frame, text="Downloads", variable=self.folder_filter, 
                       value="downloads", command=self.apply_filters).pack(anchor=tk.W)
        ttk.Radiobutton(folder_frame, text="Imagens", variable=self.folder_filter, 
                       value="images", command=self.apply_filters).pack(anchor=tk.W)
        
        # Estatísticas
        stats_frame = ttk.LabelFrame(left_frame, text="📊 Estatísticas", padding="10")
        stats_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.stats_label = ttk.Label(stats_frame, text="Arquivos indexados: 0", style='Info.TLabel')
        self.stats_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.last_index_label = ttk.Label(stats_frame, text="Última indexação: Nunca", style='Info.TLabel')
        self.last_index_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.cache_size_label = ttk.Label(stats_frame, text="Tamanho do cache: 0.0 KB", style='Info.TLabel')
        self.cache_size_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.status_label = ttk.Label(stats_frame, text="Status: ⚠️ Sem arquivos", style='Info.TLabel')
        self.status_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Barra de progresso
        self.progress_bar = ttk.Progressbar(stats_frame, mode='determinate', length=200)
        self.progress_bar.pack(fill=tk.X, pady=(0, 5))
        
        self.progress_label = ttk.Label(stats_frame, text="Progresso: 0%", style='Info.TLabel')
        self.progress_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.progress_text = ttk.Label(stats_frame, text="0 / 0 arquivos processados", style='Info.TLabel')
        self.progress_text.pack(anchor=tk.W)
        
        # Painel direito - Resultados e Visualizador
        right_frame = ttk.Frame(content_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Frame superior - Busca e resultados
        results_frame = ttk.LabelFrame(right_frame, text="🔍 Resultados da Busca", padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        # Contador de resultados
        self.results_count_label = ttk.Label(results_frame, text="Nenhum resultado", style='Info.TLabel')
        self.results_count_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Barra de ferramentas
        toolbar_frame = ttk.Frame(results_frame)
        toolbar_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(toolbar_frame, text="📁 Tempo Real", command=self.show_realtime_files, 
                  style='Action.TButton').pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(toolbar_frame, text="📄 Documentos", command=lambda: self.filter_by_type('documents'), 
                  style='Action.TButton').pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(toolbar_frame, text="🖼️ Imagens", command=lambda: self.filter_by_type('images'), 
                  style='Action.TButton').pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(toolbar_frame, text="📁 Pastas", command=lambda: self.filter_by_type('folders'), 
                  style='Action.TButton').pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(toolbar_frame, text="☆ Favoritos", command=self.show_favorites, 
                  style='Action.TButton').pack(side=tk.LEFT, padx=(0, 5))
        
        # Tabela de resultados
        columns = ('Nome do Arquivo', 'Data de Modificação', 'Tipo de Arquivo', 'Tamanho', 'Localização')
        self.results_tree = ttk.Treeview(results_frame, columns=columns, show='headings', height=15)
        
        # Configurar colunas
        for col in columns:
            self.results_tree.heading(col, text=col)
            self.results_tree.column(col, width=150)
        
        # Scrollbar para resultados
        results_scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.results_tree.yview)
        self.results_tree.configure(yscrollcommand=results_scrollbar.set)
        
        # Empacotar tabela e scrollbar
        self.results_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        results_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Frame inferior - Visualizador de arquivos
        viewer_frame = ttk.LabelFrame(right_frame, text="📖 Visualizador de Arquivos", padding="10")
        viewer_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Controles do visualizador
        viewer_controls = ttk.Frame(viewer_frame)
        viewer_controls.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(viewer_controls, text="Arquivo selecionado:", style='Info.TLabel').pack(side=tk.LEFT)
        self.selected_file_label = ttk.Label(viewer_controls, text="Nenhum arquivo selecionado", style='Info.TLabel')
        self.selected_file_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # Área de visualização
        self.viewer_text = tk.Text(viewer_frame, wrap=tk.WORD, height=10, state=tk.DISABLED)
        viewer_scrollbar = ttk.Scrollbar(viewer_frame, orient=tk.VERTICAL, command=self.viewer_text.yview)
        self.viewer_text.configure(yscrollcommand=viewer_scrollbar.set)
        
        self.viewer_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        viewer_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind duplo clique para visualizar arquivo
        self.results_tree.bind('<Double-1>', self.on_file_double_click)

    def perform_search(self):
        """Executa a busca - ULTRA ROBUSTA"""
        query = self.search_entry.get().strip()
        if not query:
            messagebox.showwarning("Aviso", "Digite um termo para buscar!")
            return
            
        print(f"🔍 Executando busca por: '{query}'")
        print(f"📁 Arquivos disponíveis no cache: {len(self.file_cache)}")
        
        # Verificar se há arquivos indexados
        if not self.file_cache:
            messagebox.showwarning("Aviso", "Nenhum arquivo indexado!\n\nClique em '🔄 Atualizar' para indexar arquivos primeiro.")
            return
            
        # Limpar resultados anteriores de forma ROBUSTA
        self.clear_search_results()
        
        # Criar cópia segura do cache para evitar erro durante indexação
        try:
            # Fazer cópia do cache atual para busca segura
            search_cache = dict(self.file_cache)
            print(f"🔒 Cache copiado com segurança: {len(search_cache)} arquivos")
        except Exception as e:
            print(f"❌ Erro ao copiar cache: {e}")
            messagebox.showerror("Erro", "Erro ao preparar busca. Tente novamente.")
            return
        
        # Buscar nos arquivos indexados
        results = []
        query_lower = query.lower()
        
        print(f"🔍 Iniciando busca em {len(search_cache)} arquivos...")
        
        for file_path, file_info in search_cache.items():
            try:
                # Verificar se o arquivo ainda existe
                if not os.path.exists(file_path):
                    continue
                    
                # Buscar no nome do arquivo
                if query_lower in file_info['name'].lower():
                    results.append((file_path, file_info))
                    continue
                    
                # Buscar no caminho
                if query_lower in file_path.lower():
                    results.append((file_path, file_info))
                    continue
                    
                # Buscar por extensão
                if query_lower.startswith('.') and file_info['name'].lower().endswith(query_lower):
                    results.append((file_path, file_info))
                    continue
                    
            except Exception as e:
                print(f"⚠️ Erro ao processar arquivo {file_path}: {e}")
                continue
        
        print(f"✅ Busca concluída: {len(results)} resultados encontrados")
        
        # Aplicar filtros
        filtered_results = self.apply_filters_to_results(results)
        
        # Exibir resultados
        self.display_search_results(filtered_results)
        
        # Atualizar estatísticas
        self.update_stats()
        
    def clear_search_results(self):
        """Limpa resultados de busca de forma ROBUSTA"""
        try:
            for item in self.results_tree.get_children():
                self.results_tree.delete(item)
            print("🧹 Resultados anteriores limpos com sucesso")
        except Exception as e:
            print(f"⚠️ Erro ao limpar resultados: {e}")
            
    def display_search_results(self, results):
        """Exibe resultados de busca de forma ROBUSTA"""
        try:
            # Limpar resultados anteriores
            for item in self.results_tree.get_children():
                self.results_tree.delete(item)
            
            if not results:
                self.results_count_label.config(text="Nenhum resultado encontrado")
                return
            
            # Exibir resultados
            for file_path, file_info in results:
                try:
                    if os.path.exists(file_path):
                        self.results_tree.insert('', 'end', values=(
                            file_info['name'],
                            file_info['modified'].strftime('%d/%m/%Y %H:%M'),
                            file_info['type'],
                            self.format_file_size(file_info['size']),
                            file_info['path']
                        ), tags=(file_path,))
                except Exception as e:
                    print(f"⚠️ Erro ao exibir arquivo {file_path}: {e}")
                    continue
            
            # Atualizar contador
            self.results_count_label.config(text=f"{len(results)} documentos encontrados")
            
        except Exception as e:
            print(f"❌ Erro ao exibir resultados: {e}")
            messagebox.showerror("Erro", f"Erro ao exibir resultados: {e}")
            
    def apply_filters_to_results(self, results):
        """Aplica filtros aos resultados de busca"""
        if not results:
            return results
            
        filtered_results = []
        
        for file_path, file_info in results:
            try:
                # Verificar se arquivo ainda existe
                if not os.path.exists(file_path):
                    continue
                    
                # Aplicar filtros
                if self.passes_date_filter(file_info['modified']) and \
                   self.passes_type_filter(file_info['type']) and \
                   self.passes_folder_filter(file_info['path']):
                    filtered_results.append((file_path, file_info))
                    
            except Exception as e:
                print(f"⚠️ Erro ao filtrar arquivo {file_path}: {e}")
                continue
        
        return filtered_results
        
    def on_file_double_click(self, event):
        """Abre o arquivo selecionado no visualizador"""
        selection = self.results_tree.selection()
        if not selection:
            return
            
        item = self.results_tree.item(selection[0])
        file_path = item['values'][4]
        
        try:
            if os.path.exists(file_path):
                self.selected_file_label.config(text=f"Arquivo selecionado: {os.path.basename(file_path)}")
                self.viewer_text.config(state=tk.NORMAL)
                self.viewer_text.delete(1.0, tk.END)
                
                if file_path.lower().endswith('.docx'):
                    doc = Document(file_path)
                    content = ""
                    for para in doc.paragraphs:
                        if para.text.strip():
                            content += para.text + "\n"
                    self.viewer_text.insert(tk.END, content[:5000] + "..." if len(content) > 5000 else content)
                    self.viewer_text.config(state=tk.DISABLED)
                elif file_path.lower().endswith('.pdf'):
                    with open(file_path, 'rb') as f:
                        pdf_reader = PyPDF2.PdfReader(f)
                        content = ""
                        for page in pdf_reader.pages[:3]:  # Primeiras 3 páginas
                            content += page.extract_text() + "\n"
                        self.viewer_text.insert(tk.END, content[:5000] + "..." if len(content) > 5000 else content)
                    self.viewer_text.config(state=tk.DISABLED)
                elif file_path.lower().endswith(('.txt', '.log', '.csv', '.json')):
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        self.viewer_text.insert(tk.END, content[:5000] + "..." if len(content) > 5000 else content)
                    self.viewer_text.config(state=tk.DISABLED)
                else:
                    self.viewer_text.insert(tk.END, f"Visualização não suportada para este tipo de arquivo: {os.path.splitext(file_path)[1]}")
                    self.viewer_text.config(state=tk.DISABLED)
            else:
                self.selected_file_label.config(text="Arquivo não encontrado: " + os.path.basename(file_path))
                self.viewer_text.config(state=tk.DISABLED)
        except Exception as e:
            self.selected_file_label.config(text=f"Erro ao abrir arquivo: {e}")
            self.viewer_text.config(state=tk.DISABLED)
            print(f"❌ Erro ao visualizar arquivo {file_path}: {e}")

    def passes_date_filter(self, modified_date):
        """Verifica se a data passa no filtro"""
        if self.date_filter.get() == "all":
            return True
            
        now = datetime.now()
        if self.date_filter.get() == "7days":
            return modified_date > now - timedelta(days=7)
        elif self.date_filter.get() == "30days":
            return modified_date > now - timedelta(days=30)
        elif self.date_filter.get() == "1year":
            return modified_date > now - timedelta(days=365)
        return True
        
    def passes_type_filter(self, file_type):
        """Verifica se o tipo passa no filtro"""
        if self.type_filter.get() == "all":
            return True
            
        if self.type_filter.get() == "documents":
            return file_type.lower() in ["documento", "pdf", "word", "excel"]
        elif self.type_filter.get() == "images":
            return file_type.lower() in ["imagem", "jpg", "png", "gif"]
        elif self.type_filter.get() == "archives":
            return file_type.lower() in ["compactado", "zip", "rar", "7z"]
        return True
        
    def passes_folder_filter(self, file_path):
        """Verifica se a pasta passa no filtro"""
        if self.folder_filter.get() == "all":
            return True
            
        path_lower = file_path.lower()
        if self.folder_filter.get() == "documents":
            return "documentos" in path_lower or "documents" in path_lower
        elif self.folder_filter.get() == "downloads":
            return "downloads" in path_lower or "download" in path_lower
        elif self.folder_filter.get() == "images":
            return "imagens" in path_lower or "images" in path_lower
        return True
        
    def apply_filters(self):
        """Aplica filtros aos resultados atuais"""
        if hasattr(self, 'current_results'):
            filtered_results = self.apply_filters_to_results(self.current_results)
            self.display_search_results(filtered_results)
            
    def stop_indexing(self):
        """Para a indexação em andamento"""
        if self.is_indexing:
            if messagebox.askyesno("Parar Indexação", "Tem certeza que deseja parar a indexação em andamento?"):
                self.is_indexing = False
                self.total_files_to_process = 0
                self.processed_files = 0
                self.update_stats()
                print("🛑 Indexação interrompida pelo usuário.")
        else:
            messagebox.showinfo("Indexação Parada", "A indexação não está em andamento.")
            
    def refresh_files(self):
        """Atualiza a indexação de arquivos"""
        if self.is_indexing:
            messagebox.showinfo("Indexação em Andamento", "A indexação já está em andamento. Aguarde a conclusão.")
            return
            
        print("🔄 Botão Atualizar clicado!")
        
        # Verificar configuração
        if not self.config.get('path'):
            messagebox.showerror("Erro", "Configure o caminho do servidor primeiro!")
            self.show_config_dialog()
            return
            
        # Iniciar indexação em thread separada
        self.is_indexing = True
        indexing_thread = threading.Thread(target=self.index_files, daemon=True)
        indexing_thread.start()
        
    def index_files(self):
        """Indexa arquivos em thread separada"""
        try:
            server_type = self.config.get('type', 'local')
            path = self.config.get('path', '')
            
            if server_type == 'local':
                self.index_local_files(path)
            elif server_type == 'ftp':
                self.index_ftp_files()
            elif server_type == 'network':
                self.index_network_files()
            else:
                print(f"❌ Tipo de servidor não suportado: {server_type}")
                
        except Exception as e:
            print(f"❌ Erro durante indexação: {e}")
            traceback.print_exc()
        finally:
            self.is_indexing = False
            self.save_file_cache()
            self.update_stats()
            print("✅ Indexação concluída!")
            
    def index_local_files(self, path):
        """Indexa arquivos locais"""
        try:
            if not os.path.exists(path):
                print(f"❌ Caminho não encontrado: {path}")
                return
                
            print(f"📁 Iniciando indexação de: {path}")
            
            # Contar total de arquivos primeiro
            total_files = 0
            for root, dirs, files in os.walk(path):
                total_files += len(files)
                
            self.total_files_to_process = total_files
            self.processed_files = 0
            print(f"📊 Total de arquivos a processar: {total_files:,}")
            
            # Backup do cache atual
            old_cache = dict(self.file_cache)
            
            # Processar arquivos
            file_count = 0
            for root, dirs, files in os.walk(path):
                for file in files:
                    if not self.is_indexing:  # Verificar se foi interrompido
                        print("🛑 Indexação interrompida!")
                        return
                        
                    try:
                        file_path = os.path.join(root, file)
                        file_info = self.extract_file_info(file_path)
                        
                        if file_info:
                            self.file_cache[file_path] = file_info
                            
                        file_count += 1
                        self.processed_files += 1
                        
                        # Atualizar progresso a cada 50 arquivos
                        if file_count % 50 == 0:
                            self.update_progress_ui(file_count, total_files)
                            
                        # Mostrar arquivos em tempo real a cada 200
                        if file_count % 200 == 0:
                            self.show_realtime_files()
                            
                    except PermissionError:
                        print(f"⚠️ Sem permissão para acessar: {file}")
                        continue
                    except OSError as e:
                        print(f"⚠️ Erro de sistema: {file} - {e}")
                        continue
                    except Exception as e:
                        print(f"⚠️ Erro ao processar {file}: {e}")
                        continue
                        
            print(f"✅ Indexação local concluída: {file_count:,} arquivos processados")
            
        except Exception as e:
            print(f"❌ Erro na indexação local: {e}")
            # Restaurar cache anterior em caso de erro
            self.file_cache = old_cache
            traceback.print_exc()

    def update_progress_ui(self, processed, total):
        """Atualiza a interface de progresso"""
        try:
            if total > 0:
                percentage = (processed / total) * 100
                self.progress_bar['value'] = percentage
                self.progress_label.config(text=f"Progresso: {percentage:.1f}%")
                self.progress_text.config(text=f"{processed:,} / {total:,} arquivos processados")
                self.stats_label.config(text=f"Arquivos indexados: {len(self.file_cache):,}")
                self.root.update_idletasks()
        except Exception as e:
            print(f"⚠️ Erro ao atualizar progresso: {e}")
            
    def show_realtime_files(self):
        """Mostra arquivos em tempo real durante indexação"""
        try:
            # Limpar resultados anteriores
            for item in self.results_tree.get_children():
                self.results_tree.delete(item)
                
            # Pegar últimos 100 arquivos do cache
            recent_files = list(self.file_cache.items())[-100:]
            
            for file_path, file_info in recent_files:
                try:
                    if os.path.exists(file_path):
                        self.results_tree.insert('', 'end', values=(
                            file_info['name'],
                            file_info['modified'].strftime('%d/%m/%Y %H:%M'),
                            file_info['type'],
                            self.format_file_size(file_info['size']),
                            file_info['path']
                        ), tags=(file_path,))
                except Exception as e:
                    continue
                    
            self.results_count_label.config(text=f"{len(recent_files)} arquivos indexados recentemente")
            
        except Exception as e:
            print(f"⚠️ Erro ao mostrar arquivos em tempo real: {e}")
            
    def update_ui_timer(self):
        """Timer para atualizar a UI durante indexação"""
        if self.is_indexing:
            self.update_stats()
            self.root.update_idletasks()
            self.root.after(100, self.update_ui_timer)
        else:
            self.progress_bar['value'] = 0
            self.progress_label.config(text="Progresso: 0%")
            self.progress_text.config(text="0 / 0 arquivos processados")
            
    def update_stats(self):
        """Atualiza estatísticas da interface"""
        try:
            # Arquivos indexados
            self.stats_label.config(text=f"Arquivos indexados: {len(self.file_cache):,}")
            
            # Status dinâmico
            if self.is_indexing:
                self.status_label.config(text="Status: 🔄 Indexando...")
            elif len(self.file_cache) > 0:
                self.status_label.config(text="Status: ✅ Pronto para busca")
            else:
                self.status_label.config(text="Status: ⚠️ Sem arquivos")
                
            # Tamanho do cache
            cache_size = len(json.dumps(self.file_cache, default=str))
            self.cache_size_label.config(text=f"Tamanho do cache: {cache_size / 1024:.1f} KB")
            
        except Exception as e:
            print(f"⚠️ Erro ao atualizar estatísticas: {e}")
            
    def extract_file_info(self, file_path):
        """Extrai informações do arquivo"""
        try:
            stat = os.stat(file_path)
            file_name = os.path.basename(file_path)
            file_ext = os.path.splitext(file_name)[1].lower()
            
            # Determinar tipo de arquivo
            if file_ext in ['.docx', '.doc']:
                file_type = "Documento"
            elif file_ext in ['.pdf']:
                file_type = "PDF"
            elif file_ext in ['.jpg', '.jpeg', '.png', '.gif']:
                file_type = "Imagem"
            elif file_ext in ['.zip', '.rar', '.7z']:
                file_type = "Compactado"
            else:
                file_type = "Arquivo"
                
            return {
                'name': file_name,
                'path': os.path.dirname(file_path),
                'type': file_type,
                'size': stat.st_size,
                'modified': datetime.fromtimestamp(stat.st_mtime)
            }
            
        except Exception as e:
            print(f"⚠️ Erro ao extrair info de {file_path}: {e}")
            return None
            
    def format_file_size(self, size_bytes):
        """Formata tamanho do arquivo"""
        if size_bytes == 0:
            return "0 B"
        size_names = ["B", "KB", "MB", "GB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        return f"{size_bytes:.1f} {size_names[i]}"
        
    def clear_cache(self):
        """Limpa o cache de arquivos"""
        if messagebox.askyesno("Limpar Cache", "Tem certeza que deseja limpar o cache?\n\nIsso removerá todos os arquivos indexados."):
            self.file_cache.clear()
            self.save_file_cache()
            self.update_stats()
            self.clear_search_results()
            messagebox.showinfo("Cache Limpo", "Cache limpo com sucesso!")
            
    def load_file_cache(self):
        """Carrega cache de arquivos do disco"""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    cache_data = json.load(f)
                    
                # Converter strings de data de volta para datetime
                for file_path, file_info in cache_data.items():
                    if 'modified' in file_info and isinstance(file_info['modified'], str):
                        try:
                            file_info['modified'] = datetime.fromisoformat(file_info['modified'])
                        except:
                            file_info['modified'] = datetime.now()
                            
                self.file_cache = cache_data
                print(f"📁 Cache carregado: {len(self.file_cache)} arquivos")
            else:
                print("📁 Nenhum cache encontrado, iniciando novo")
                
        except Exception as e:
            print(f"❌ Erro ao carregar cache: {e}")
            self.file_cache = {}
            
    def save_file_cache(self):
        """Salva cache de arquivos no disco"""
        try:
            # Converter datetime para string ISO
            cache_data = {}
            for file_path, file_info in self.file_cache.items():
                cache_data[file_path] = file_info.copy()
                if isinstance(file_info['modified'], datetime):
                    cache_data[file_path]['modified'] = file_info['modified'].isoformat()
                    
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
                
            print(f"💾 Cache salvo: {len(self.file_cache)} arquivos")
            
        except Exception as e:
            print(f"❌ Erro ao salvar cache: {e}")
            
    def load_config(self):
        """Carrega configurações"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
                print("⚙️ Configurações carregadas")
            else:
                self.config = {
                    'type': 'local',
                    'host': '',
                    'user': '',
                    'password': '',
                    'path': 'C:\\Documentos',
                    'port': ''
                }
                self.save_config()
                print("⚙️ Configurações padrão criadas")
                
        except Exception as e:
            print(f"❌ Erro ao carregar configurações: {e}")
            self.config = {'type': 'local', 'path': 'C:\\Documentos'}
            
    def save_config(self):
        """Salva configurações"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
            print("💾 Configurações salvas")
        except Exception as e:
            print(f"❌ Erro ao salvar configurações: {e}")
            
    def check_initial_config(self):
        """Verifica configuração inicial"""
        if not self.config.get('path') or self.config.get('path') == 'C:\\Documentos':
            messagebox.showinfo("Configuração", 
                              "Configure o caminho do servidor de arquivos!\n\n"
                              "Clique em '⚙️ Configurar' para definir o local dos arquivos.")
        else:
            print(f"✅ Configuração válida: {self.config['path']}")
            
        # Verificar cache
        if len(self.file_cache) > 0:
            print(f"📁 Cache encontrado: {len(self.file_cache)} arquivos")
        else:
            print("📁 Nenhum arquivo indexado. Clique em '🔄 Atualizar' para começar.")
            
    def show_config_dialog(self):
        """Mostra diálogo de configuração"""
        config_window = tk.Toplevel(self.root)
        config_window.title("⚙️ Configurações do Servidor")
        config_window.geometry("500x400")
        config_window.transient(self.root)
        config_window.grab_set()
        
        # Frame principal
        main_frame = ttk.Frame(config_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        ttk.Label(main_frame, text="⚙️ Configurações do Servidor", style='Title.TLabel').pack(pady=(0, 20))
        
        # Tipo de servidor
        server_type_frame = ttk.Frame(main_frame)
        server_type_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(server_type_frame, text="Tipo de Servidor:", style='Header.TLabel').pack(anchor=tk.W)
        self.config_server_type = ttk.Combobox(server_type_frame, 
                                             values=['local', 'ftp', 'network'], 
                                             width=20, state='readonly')
        self.config_server_type.pack(side=tk.LEFT, pady=(5, 0))
        self.config_server_type.set(self.config.get('type', 'local'))
        
        # Caminho local
        path_frame = ttk.Frame(main_frame)
        path_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(path_frame, text="Caminho do Servidor:", style='Header.TLabel').pack(anchor=tk.W)
        path_input_frame = ttk.Frame(path_frame)
        path_input_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.config_path = ttk.Entry(path_input_frame, width=40)
        self.config_path.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.config_path.insert(0, self.config.get('path', ''))
        
        ttk.Button(path_input_frame, text="📁 Procurar", 
                  command=self.browse_path).pack(side=tk.RIGHT, padx=(5, 0))
        
        # Botões
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        ttk.Button(button_frame, text="💾 Salvar", 
                  command=lambda: self.save_config_from_dialog(config_window)).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(button_frame, text="❌ Cancelar", 
                  command=config_window.destroy).pack(side=tk.RIGHT)
        
    def browse_path(self):
        """Abre diálogo para selecionar pasta"""
        path = filedialog.askdirectory(title="Selecionar Pasta do Servidor")
        if path:
            self.config_path.delete(0, tk.END)
            self.config_path.insert(0, path)
            
    def save_config_from_dialog(self, window):
        """Salva configurações do diálogo"""
        self.config['type'] = self.config_server_type.get()
        self.config['path'] = self.config_path.get()
        
        self.save_config()
        messagebox.showinfo("Sucesso", "Configurações salvas com sucesso!")
        window.destroy()
        
    def filter_by_type(self, file_type):
        """Filtra resultados por tipo"""
        # Implementar filtros específicos
        pass
        
    def show_favorites(self):
        """Mostra arquivos favoritos"""
        # Implementar sistema de favoritos
        pass
        
    def index_ftp_files(self):
        """Indexa arquivos FTP (placeholder)"""
        print("📡 Indexação FTP não implementada ainda")
        
    def index_network_files(self):
        """Indexa arquivos de rede (placeholder)"""
        print("🌐 Indexação de rede não implementada ainda")

def main():
    root = tk.Tk()
    app = AdvancedFileSearchDesktop(root)
    root.mainloop()

if __name__ == "__main__":
    main()
