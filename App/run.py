import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from __init__ import create_app

if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.INFO)
    app = create_app()
    app.run(host='127.0.0.1', port=5000, debug=True)
