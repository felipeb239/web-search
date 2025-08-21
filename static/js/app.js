/**
 * Sistema de Busca de Arquivos - JavaScript Principal
 */

class FileSearchApp {
    constructor() {
        this.initializeElements();
        this.bindEvents();
        this.loadInitialData();
    }

    /**
     * Inicializa os elementos DOM
     */
    initializeElements() {
        this.uploadArea = document.getElementById('uploadArea');
        this.fileInput = document.getElementById('fileInput');
        this.uploadStatus = document.getElementById('uploadStatus');
        this.searchInput = document.getElementById('searchInput');
        this.searchResults = document.getElementById('searchResults');
        this.fileList = document.getElementById('fileList');
    }

    /**
     * Configura os event listeners
     */
    bindEvents() {
        // Drag and Drop
        this.uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            this.uploadArea.classList.add('dragover');
        });

        this.uploadArea.addEventListener('dragleave', () => {
            this.uploadArea.classList.remove('dragover');
        });

        this.uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            this.uploadArea.classList.remove('dragover');
            const files = e.dataTransfer.files;
            this.handleFiles(files);
        });

        // Seleção de arquivos
        this.fileInput.addEventListener('change', (e) => {
            this.handleFiles(e.target.files);
        });

        // Busca com Enter
        this.searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.performSearch();
            }
        });
    }

    /**
     * Carrega dados iniciais
     */
    async loadInitialData() {
        await this.loadStats();
        await this.loadFileList();
    }

    /**
     * Processa arquivos selecionados
     */
    handleFiles(files) {
        Array.from(files).forEach(file => {
            this.uploadFile(file);
        });
    }

    /**
     * Faz upload de um arquivo
     */
    async uploadFile(file) {
        const formData = new FormData();
        formData.append('file', file);

        this.showAlert('Enviando arquivo...', 'success');

        try {
            const response = await fetch('/api/upload', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (result.success) {
                this.showAlert(result.message, 'success');
                await this.loadStats();
                await this.loadFileList();
            } else {
                this.showAlert(result.error, 'error');
            }
        } catch (error) {
            this.showAlert('Erro ao enviar arquivo: ' + error.message, 'error');
        }
    }

    /**
     * Realiza busca nos arquivos
     */
    async performSearch() {
        const query = this.searchInput.value.trim();
        if (!query) {
            this.showAlert('Digite um termo para buscar', 'error');
            return;
        }

        this.searchResults.innerHTML = '<div class="loading"><div class="spinner"></div>Buscando...</div>';

        try {
            const response = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
            const result = await response.json();

            if (result.error) {
                this.showAlert(result.error, 'error');
                this.searchResults.innerHTML = '';
                return;
            }

            this.displaySearchResults(result);
        } catch (error) {
            this.showAlert('Erro na busca: ' + error.message, 'error');
            this.searchResults.innerHTML = '';
        }
    }

    /**
     * Exibe resultados da busca
     */
    displaySearchResults(result) {
        if (result.total_results === 0) {
            this.searchResults.innerHTML = `<div class="alert alert-error">Nenhum resultado encontrado para "${result.query}"</div>`;
            return;
        }

        let html = `<h3>${result.total_results} resultado(s) para "${result.query}"</h3>`;
        
        result.results.forEach(item => {
            const date = new Date(item.upload_date).toLocaleDateString('pt-BR');
            const size = this.formatFileSize(item.file_size);
            
            html += `
                <div class="result-item">
                    <div class="result-header">
                        <div class="result-title">${item.filename}</div>
                        <div class="result-type">${item.file_type.toUpperCase()}</div>
                    </div>
                    <div class="result-meta">
                        📅 Enviado em: ${date} | 📏 Tamanho: ${size}
                    </div>
                    <div class="result-match">
                        ${item.match_type} (Relevância: ${item.relevance}%)
                    </div>
                </div>
            `;
        });

        this.searchResults.innerHTML = html;
    }

    /**
     * Carrega estatísticas dos arquivos
     */
    async loadStats() {
        try {
            const response = await fetch('/api/stats');
            const stats = await response.json();

            document.getElementById('total-files').textContent = stats.total_files;
            document.getElementById('total-docx').textContent = stats.total_docx;
            document.getElementById('total-pdf').textContent = stats.total_pdf;
        } catch (error) {
            console.error('Erro ao carregar estatísticas:', error);
        }
    }

    /**
     * Carrega lista de arquivos
     */
    async loadFileList() {
        try {
            const response = await fetch('/api/files');
            const result = await response.json();

            if (result.files.length === 0) {
                this.fileList.innerHTML = '<div class="alert alert-error">Nenhum arquivo indexado ainda.</div>';
                return;
            }

            let html = '';
            result.files.forEach(file => {
                const date = new Date(file.upload_date).toLocaleDateString('pt-BR');
                const size = this.formatFileSize(file.file_size);
                
                html += `
                    <div class="file-item">
                        <div class="file-header">
                            <div class="file-name">${file.filename}</div>
                            <div class="file-type">${file.file_type.toUpperCase()}</div>
                        </div>
                        <div class="file-info">
                            📅 Enviado em: ${date} | 📏 Tamanho: ${size}
                        </div>
                    </div>
                `;
            });

            this.fileList.innerHTML = html;
        } catch (error) {
            console.error('Erro ao carregar lista de arquivos:', error);
            this.fileList.innerHTML = '<div class="alert alert-error">Erro ao carregar arquivos.</div>';
        }
    }

    /**
     * Formata tamanho do arquivo
     */
    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    /**
     * Mostra alerta na tela
     */
    showAlert(message, type) {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type}`;
        alertDiv.textContent = message;
        
        this.uploadStatus.innerHTML = '';
        this.uploadStatus.appendChild(alertDiv);
        
        setTimeout(() => {
            alertDiv.remove();
        }, 5000);
    }
}

// Inicializar aplicação quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', () => {
    // Tornar a instância globalmente acessível
    window.app = new FileSearchApp();
});
