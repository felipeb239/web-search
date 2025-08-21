"""
Módulo para as rotas da API Flask
"""
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
import os
from file_processor import FileProcessor

# Criar blueprint para as rotas
api = Blueprint('api', __name__)

# Instanciar processador de arquivos
file_processor = FileProcessor()


def allowed_file(filename):
    """Verifica se a extensão do arquivo é permitida"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


@api.route('/upload', methods=['POST'])
def upload_file():
    """Endpoint para upload de arquivos"""
    if 'file' not in request.files:
        return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
    
    # Verificar extensão do arquivo
    if not allowed_file(file.filename):
        return jsonify({'error': 'Tipo de arquivo não suportado. Use apenas .docx ou .pdf'}), 400
    
    # Salvar arquivo
    filename = secure_filename(file.filename)
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    
    # Determinar tipo de arquivo
    file_type = 'docx' if filename.endswith('.docx') else 'pdf'
    
    # Indexar arquivo
    try:
        file_info = file_processor.index_file(filename, file_path, file_type)
        return jsonify({
            'success': True,
            'message': f'Arquivo {filename} enviado e indexado com sucesso!',
            'file_info': {
                'filename': filename,
                'file_type': file_type,
                'upload_date': file_info['upload_date'],
                'file_size': file_info['file_size']
            }
        })
    except Exception as e:
        return jsonify({'error': f'Erro ao processar arquivo: {str(e)}'}), 500


@api.route('/search')
def search():
    """Endpoint para busca de arquivos"""
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify({'error': 'Termo de busca não fornecido'}), 400
    
    results = file_processor.search_files(query)
    return jsonify({
        'query': query,
        'results': results,
        'total_results': len(results)
    })


@api.route('/files')
def list_files():
    """Lista todos os arquivos indexados"""
    files = file_processor.get_all_files()
    return jsonify({'files': files})


@api.route('/stats')
def get_stats():
    """Retorna estatísticas dos arquivos"""
    stats = file_processor.get_file_stats()
    return jsonify(stats)
