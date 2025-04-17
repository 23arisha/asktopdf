import os
from flask import Flask
from dotenv import load_dotenv

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config["UPLOAD_FOLDER"] = "app/static/uploads"

    from .routes.upload import upload_bp
    from .routes.chat import chat_bp

    app.register_blueprint(upload_bp)
    app.register_blueprint(chat_bp)

    return app
