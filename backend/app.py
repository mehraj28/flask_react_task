# backend/app.py
from flask import Flask
from flask_cors import CORS
from database import db
from routes import api

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Configure SQLite database
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize DB
    db.init_app(app)

    # Register routes
    app.register_blueprint(api, url_prefix="/api")

    # ✅ Ensure tables exist at startup
    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
