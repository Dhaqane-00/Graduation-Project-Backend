from flask import Flask
from flask_cors import CORS
from flask_mail import Mail
import os
from dotenv import load_dotenv

# Initialize Flask-Mail
mail = Mail()

def create_app():
    app = Flask(__name__, static_folder='../frontend/build', static_url_path='/')
    CORS(app)  # Enable CORS for all routes

    # Load environment variables from .env file
    load_dotenv()

    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploads')
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['BASE_URL'] = os.getenv('BASE_URL', 'http://localhost:5000')

    # Set RESET_URL configuration
    app.config['RESET_URL'] = os.getenv('RESET_URL')

    # Configure Flask-Mail
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True').lower() in ['true', '1', 't']
    app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL', 'False').lower() in ['true', '1', 't']
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER', app.config['MAIL_USERNAME'])

    # Initialize Flask-Mail with app context
    mail.init_app(app)

    with app.app_context():
        from Controllers import predict, single_predict, results, chart_data, summary_chart_data, auth, image
        app.register_blueprint(predict.bp)
        app.register_blueprint(single_predict.bp)
        app.register_blueprint(results.bp)
        app.register_blueprint(chart_data.bp)
        app.register_blueprint(summary_chart_data.bp)
        app.register_blueprint(auth.bp)
        app.register_blueprint(image.bp)

        @app.route('/')
        def serve_react_app():
            return app.send_static_file('index.html')

        @app.route('/<path:path>')
        def serve_react_static_files(path):
            if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
                return app.send_static_file(path)
            else:
                return app.send_static_file('index.html')

    return app
