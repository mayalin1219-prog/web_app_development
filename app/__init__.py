import os
from flask import Flask
from config import Config
from app.models import db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 確保 instance 目錄與資料庫目錄存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
        
    # 確保上傳目錄存在
    try:
        os.makedirs(app.config['UPLOAD_FOLDER'])
    except OSError:
        pass

    db.init_app(app)

    # 註冊 Blueprints
    from app.routes import register_blueprints
    register_blueprints(app)

    return app
