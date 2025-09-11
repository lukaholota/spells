from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    DB_URL = os.getenv('SPELLS_DB')
    SECRET_KEY = os.getenv('SPELLS_SECRET_KEY')

settings = Settings()
