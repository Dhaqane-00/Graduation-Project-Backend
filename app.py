import sys
import os
from dotenv import load_dotenv
from flask_cors import CORS

# Load environment variables from .env file
load_dotenv()

# Retrieve host and port from environment variables
host = os.getenv('HOST')
port = os.getenv('PORT')

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from __init__ import create_app

if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.INFO)
    app = create_app()
    app.run(host=host, port=int(port),debug=True)
