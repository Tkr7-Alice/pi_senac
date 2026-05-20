import os
import sys
from flask import Flask
from dotenv import load_dotenv

# Determina o diretório base do backend
base_dir = os.path.dirname(os.path.abspath(__file__))

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv(os.path.join(base_dir, ".env"))

# Adiciona o diretório base ao PYTHONPATH para garantir que imports internos funcionem
sys.path.append(base_dir)

from routes.chat_routes import chat_bp
from routes.admin_routes import admin_bp
from services.db_service import DBService

# Inicializa o banco de dados SQLite na inicialização do Flask
DBService.init_db()

# Configura o Flask para servir os arquivos estáticos da pasta raiz
app = Flask(__name__, static_folder=os.path.join(base_dir, ".."), static_url_path="")

# Registra os blueprints
app.register_blueprint(chat_bp)
app.register_blueprint(admin_bp)

@app.route('/')
def index():
    return app.send_static_file('index.html')

# Adiciona cabeçalhos CORS manualmente para suportar chamadas locais de páginas hospedadas externamente
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
    return response

if __name__ == '__main__':
    # Inicializa o Flask na porta 5000
    app.run(
        debug=False,
        host='0.0.0.0',
        port=5000
    )
