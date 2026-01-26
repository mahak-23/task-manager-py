from flask import Flask, redirect, url_for, current_app
from flask_login import LoginManager
from models import db, User
from config import Config
from routes.auth import auth_bp
from routes.tasks import tasks_bp
from services.email_service import mail
from services.email_service import send_daily_task_notifications
from services.scheduler import init_scheduler
from dotenv import load_dotenv
import os

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    mail.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(tasks_bp)

    @app.route("/")
    def index():
        return redirect(url_for("auth.login"))

    @app.route("/test-email")
    def test_email():
        print("🔥 Test email route hit")
        result = send_daily_task_notifications(current_app)
        return f"Triggered: {result}"

    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            app.logger.error(f"Database connection error: {str(e)}")

    if os.environ.get("ENABLE_SCHEDULER", "false").lower() == "true":
        init_scheduler(app)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
