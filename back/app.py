import os
import sys
from flask import Flask
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))
sys.path.append(BASE_DIR)

from routes.chat_routes import chat_bp
from routes.admin_routes import admin_bp
from services.db_service import DBService

DBService.init_db()

app = Flask(__name__, static_folder=os.path.join(BASE_DIR, ".."), static_url_path="")
app.register_blueprint(chat_bp)
app.register_blueprint(admin_bp)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
    return response

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)