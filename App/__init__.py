from flask import Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv

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