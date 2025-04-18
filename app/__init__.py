import os
from flask import Flask
from dotenv import load_dotenv

def create_app():
    load_dotenv()
    app = Flask(__name__)
    print("✅ Flask app created and ready.")
    app.secret_key = os.getenv("SECRET_KEY", "defaultsecret")
    app.config["UPLOAD_FOLDER"] = "app/static/uploads"

    from .routes.upload import upload_bp
    from .routes.chat import chat_bp

    app.register_blueprint(upload_bp)
    app.register_blueprint(chat_bp)

    return app
