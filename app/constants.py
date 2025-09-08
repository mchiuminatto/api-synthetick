import os
from dotenv import load_dotenv


load_dotenv()

DB_URL: str = os.getenv("DB_URL")

REQUEST_ID_SIZE = 12
VERSION = "0.0.1"