# 🔍 Sistema de Busca de Arquivos

Um sistema web completo para busca e indexação de documentos Word (.docx) e PDF, desenvolvido com Python Flask e interface moderna.

## ✨ Funcionalidades

- **Upload de Arquivos**: Suporte para arquivos Word (.docx) e PDF
- **Indexação Automática**: Extração automática de texto para busca
- **Busca Inteligente**: Busca por nome de arquivo e conteúdo
- **Interface Moderna**: Design responsivo e intuitivo
- **Drag & Drop**: Upload fácil com arrastar e soltar
- **Estatísticas**: Contadores de arquivos por tipo
- **Responsivo**: Funciona em desktop e dispositivos móveis

## 🏗️ Arquitetura

O projeto foi modularizado para facilitar manutenção e desenvolvimento:

```
web-search/
├── app.py                 # Aplicação principal Flask
├── file_processor.py      # Processamento e indexação de arquivos
├── routes.py             # Rotas da API
├── requirements.txt      # Dependências Python
├── .gitignore           # Arquivos ignorados pelo Git
├── templates/
│   └── index.html       # Interface principal
├── static/
│   ├── css/
│   │   └── style.css    # Estilos CSS
│   └── js/
│       └── app.js       # JavaScript da aplicação
└── uploads/             # Pasta para arquivos enviados
```

## 🚀 Instalação

### Pré-requisitos

- Python 3.7 ou superior
- pip (gerenciador de pacotes Python)

### Passos

1. **Clone o repositório**
   ```bash
   git clone <url-do-repositorio>
   cd web-search
   ```

2. **Crie um ambiente virtual (recomendado)**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute a aplicação**
   ```bash
   python app.py
   ```

5. **Acesse no navegador**
   ```
   http://localhost:5000
   ```

## 📁 Estrutura dos Módulos

### `app.py`
- Arquivo principal da aplicação Flask
- Configurações básicas
- Registro de blueprints

### `file_processor.py`
- Classe `FileProcessor` para processamento de arquivos
- Extração de texto de Word e PDF
- Indexação e busca de arquivos
- Gerenciamento do índice de busca

### `routes.py`
- Blueprint Flask com todas as rotas da API
- Endpoints para upload, busca e listagem
- Validação de arquivos

### `templates/index.html`
- Interface HTML principal
- Estrutura responsiva
- Integração com CSS e JavaScript

### `static/css/style.css`
- Todos os estilos da aplicação
- Design moderno com gradientes
- Responsividade para mobile

### `static/js/app.js`
- Classe JavaScript `FileSearchApp`
- Gerenciamento de eventos
- Comunicação com a API
- Interface dinâmica

## 🔧 Configuração

### Variáveis de Ambiente

O sistema usa configurações padrão, mas você pode personalizar:

- **Porta**: Alterar em `app.py` (padrão: 5000)
- **Tamanho máximo de arquivo**: Configurado em `routes.py` (padrão: 16MB)
- **Tipos de arquivo permitidos**: Configurado em `routes.py`

### Personalização

- **Cores**: Editar variáveis CSS em `static/css/style.css`
- **Funcionalidades**: Adicionar métodos na classe `FileSearchApp`
- **Validações**: Modificar funções em `routes.py`

## 📡 API Endpoints

### `POST /api/upload`
- Upload de arquivos Word e PDF
- Retorna informações do arquivo processado

### `GET /api/search?q=<query>`
- Busca por termo nos arquivos indexados
- Retorna resultados ordenados por relevância

### `GET /api/files`
- Lista todos os arquivos indexados
- Ordenados por data de upload

### `GET /api/stats`
- Estatísticas dos arquivos
- Contadores por tipo

## 🎯 Como Usar

### 1. Upload de Arquivos
- Arraste arquivos para a área de upload ou clique para selecionar
- Suporta arquivos .docx e .pdf até 16MB
- Os arquivos são automaticamente indexados

### 2. Busca
- Digite termos na caixa de busca
- Pressione Enter ou clique em "Buscar"
- Resultados mostram relevância e tipo de match

### 3. Visualização
- Estatísticas em tempo real
- Lista completa de arquivos indexados
- Informações detalhadas de cada arquivo

## 🛠️ Tecnologias Utilizadas

- **Backend**: Python Flask
- **Processamento de Arquivos**: python-docx, PyPDF2
- **Frontend**: HTML5, CSS3, JavaScript ES6+
- **Interface**: Design responsivo com CSS Grid e Flexbox
- **Armazenamento**: Arquivo JSON para índice de busca

## 🔒 Segurança

- Validação de tipos de arquivo
- Sanitização de nomes de arquivo
- Limite de tamanho de upload
- Tratamento de erros robusto

## 📱 Responsividade

- Design mobile-first
- Adaptação automática para diferentes telas
- Interface otimizada para touch

## 🚀 Melhorias Futuras

- [ ] Banco de dados para melhor performance
- [ ] Sistema de usuários e permissões
- [ ] Busca avançada com filtros
- [ ] Preview de arquivos
- [ ] Compartilhamento de arquivos
- [ ] Histórico de buscas
- [ ] Exportação de resultados

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 📞 Suporte

Para dúvidas ou problemas:
- Abra uma issue no repositório
- Consulte a documentação
- Verifique os logs da aplicação

---

**Desenvolvido com ❤️ para facilitar a busca de documentos empresariais**
