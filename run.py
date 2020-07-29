from app.app import create_app
from flask_cors import CORS

app = create_app()
CORS(app, supports_credentials=True)