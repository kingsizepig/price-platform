from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, static_folder='static', static_url_path='')
    
    # 配置数据库
    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', f'sqlite:///{basedir}/../app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    
    # Fix static folder path
    app.static_folder = os.path.join(os.path.dirname(__file__), '../static')
    
    CORS(app)
    db.init_app(app)
    
    # 注册蓝图
    from app.api import price_api, product_api, user_api
    app.register_blueprint(product_api.bp, url_prefix='/api/product')
    app.register_blueprint(price_api.bp, url_prefix='/api/price')
    app.register_blueprint(user_api.bp, url_prefix='/api/user')
    
    @app.route('/api/health')
    def health():
        return {"status": "ok", "message": "Price Platform API is running"}
    
    # 前端静态文件
    @app.route('/')
    def index():
        return send_from_directory(app.static_folder, 'index.html')
    
    # 管理后台
    @app.route('/admin')
    @app.route('/admin/')
    def admin():
        return send_from_directory(os.path.join(app.static_folder, 'admin'), 'index.html')
    
    @app.route('/admin/<path:path>')
    def admin_static(path):
        return send_from_directory(os.path.join(app.static_folder, 'admin'), path)
    
    return app
