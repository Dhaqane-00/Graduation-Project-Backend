from flask import Blueprint, send_from_directory, current_app

bp = Blueprint('image', __name__, url_prefix='/image')

@bp.route('/<filename>')
def serve_image(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
