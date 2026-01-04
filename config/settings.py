import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev_secret_key')
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'data', 'temp_uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
