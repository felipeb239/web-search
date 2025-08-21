"""
Arquivo de configuração centralizado para o Sistema de Busca de Arquivos
"""

import os

class Config:
    """Configurações da aplicação"""
    
    # Configurações básicas
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    # Configurações de upload
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS = {'docx', 'pdf'}
    
    # Configurações de arquivos
    INDEX_FILE = 'search_index.json'
    
    # Configurações do servidor
    HOST = os.environ.get('FLASK_HOST', '0.0.0.0')
    PORT = int(os.environ.get('FLASK_PORT', 5000))
    
    # Configurações de segurança
    MAX_FILES_PER_UPLOAD = 10  # Máximo de arquivos por upload
    
    @staticmethod
    def init_app(app):
        """Inicializa configurações na aplicação Flask"""
        # Criar pasta de uploads se não existir
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        
        # Configurar tamanho máximo de upload
        app.config['MAX_CONTENT_LENGTH'] = Config.MAX_CONTENT_LENGTH


class DevelopmentConfig(Config):
    """Configurações para desenvolvimento"""
    DEBUG = True
    HOST = 'localhost'
    PORT = 5000


class ProductionConfig(Config):
    """Configurações para produção"""
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'production-secret-key-must-be-set'
    
    @classmethod
    def init_app(cls, app):
        super().init_app(app)
        
        # Log para produção
        import logging
        from logging.handlers import RotatingFileHandler
        
        if not app.debug and not app.testing:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            
            file_handler = RotatingFileHandler('logs/web-search.log', maxBytes=10240, backupCount=10)
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
            ))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)
            app.logger.setLevel(logging.INFO)
            app.logger.info('Web Search startup')


class TestingConfig(Config):
    """Configurações para testes"""
    TESTING = True
    INDEX_FILE = 'test_search_index.json'
    UPLOAD_FOLDER = 'test_uploads'


# Dicionário de configurações
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
