"""
Módulo para processamento e indexação de arquivos Word e PDF
"""
import os
import json
from datetime import datetime
from docx import Document
import PyPDF2
from flask import current_app


class FileProcessor:
    """Classe para processar e indexar arquivos"""
    
    def __init__(self, index_file=None):
        if index_file is None:
            try:
                # Tentar usar configuração do Flask
                self.index_file = current_app.config.get('INDEX_FILE', 'search_index.json')
            except RuntimeError:
                # Se não estiver no contexto Flask, usar padrão
                self.index_file = 'search_index.json'
        else:
            self.index_file = index_file
        
        self._ensure_index_exists()
    
    def _ensure_index_exists(self):
        """Garante que o arquivo de índice existe"""
        if not os.path.exists(self.index_file):
            self._save_index({})
    
    def _load_index(self):
        """Carrega o índice de busca do arquivo"""
        try:
            with open(self.index_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def _save_index(self, index):
        """Salva o índice de busca no arquivo"""
        with open(self.index_file, 'w', encoding='utf-8') as f:
            json.dump(index, f, ensure_ascii=False, indent=2)
    
    def extract_text_from_docx(self, file_path):
        """Extrai texto de arquivos Word (.docx)"""
        try:
            doc = Document(file_path)
            text = []
            for paragraph in doc.paragraphs:
                text.append(paragraph.text)
            return ' '.join(text)
        except Exception as e:
            print(f"Erro ao extrair texto do Word: {e}")
            return ""
    
    def extract_text_from_pdf(self, file_path):
        """Extrai texto de arquivos PDF"""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = []
                for page in pdf_reader.pages:
                    text.append(page.extract_text())
            return ' '.join(text)
        except Exception as e:
            print(f"Erro ao extrair texto do PDF: {e}")
            return ""
    
    def index_file(self, filename, file_path, file_type):
        """Indexa um arquivo para busca"""
        index = self._load_index()
        
        # Extrair texto baseado no tipo de arquivo
        if file_type == 'docx':
            content = self.extract_text_from_docx(file_path)
        elif file_type == 'pdf':
            content = self.extract_text_from_pdf(file_path)
        else:
            content = ""
        
        # Criar entrada no índice
        file_info = {
            'filename': filename,
            'file_type': file_type,
            'upload_date': datetime.now().isoformat(),
            'file_size': os.path.getsize(file_path),
            'content': content.lower(),  # Converter para minúsculas para busca
            'file_path': file_path
        }
        
        index[filename] = file_info
        self._save_index(index)
        
        return file_info
    
    def search_files(self, query):
        """Realiza busca nos arquivos indexados"""
        index = self._load_index()
        results = []
        query_lower = query.lower()
        
        for filename, file_info in index.items():
            # Buscar no nome do arquivo
            if query_lower in filename.lower():
                results.append({
                    'filename': filename,
                    'file_type': file_info['file_type'],
                    'upload_date': file_info['upload_date'],
                    'file_size': file_info['file_size'],
                    'match_type': 'Nome do arquivo',
                    'relevance': 100
                })
            # Buscar no conteúdo
            elif query_lower in file_info['content']:
                # Calcular relevância baseada na frequência da palavra
                content_words = file_info['content'].split()
                query_words = query_lower.split()
                matches = sum(1 for word in content_words if any(q in word for q in query_words))
                relevance = min(100, matches * 10)
                
                results.append({
                    'filename': filename,
                    'file_type': file_info['file_type'],
                    'upload_date': file_info['upload_date'],
                    'file_size': file_info['file_size'],
                    'match_type': 'Conteúdo do arquivo',
                    'relevance': relevance
                })
        
        # Ordenar por relevância
        results.sort(key=lambda x: x['relevance'], reverse=True)
        return results
    
    def get_all_files(self):
        """Retorna todos os arquivos indexados"""
        index = self._load_index()
        files = []
        
        for filename, file_info in index.items():
            files.append({
                'filename': filename,
                'file_type': file_info['file_type'],
                'upload_date': file_info['upload_date'],
                'file_size': file_info['file_size']
            })
        
        # Ordenar por data de upload (mais recente primeiro)
        files.sort(key=lambda x: x['upload_date'], reverse=True)
        return files
    
    def get_file_stats(self):
        """Retorna estatísticas dos arquivos indexados"""
        files = self.get_all_files()
        total_files = len(files)
        total_docx = len([f for f in files if f['file_type'] == 'docx'])
        total_pdf = len([f for f in files if f['file_type'] == 'pdf'])
        
        return {
            'total_files': total_files,
            'total_docx': total_docx,
            'total_pdf': total_pdf
        }
