"""
Aplicação principal Flask para o Sistema de Busca de Arquivos
"""
import os
from flask import Flask, render_template
from routes import api
from config import config

def create_app(config_name=None):
    """Factory function para criar a aplicação Flask"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')
    
    app = Flask(__name__)
    
    # Carregar configurações
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # Registrar blueprint das rotas da API
    app.register_blueprint(api, url_prefix='/api')
    
    # Rota principal
    @app.route('/')
    def index():
        """Página principal"""
        return render_template('index.html')
    
    return app

# Criar aplicação
app = create_app()

if __name__ == '__main__':
    app.run(
        host=app.config.get('HOST', '0.0.0.0'),
        port=app.config.get('PORT', 5000),
        debug=app.config.get('DEBUG', True)
    )
