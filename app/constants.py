import os
from dotenv import load_dotenv


load_dotenv()

DATABASE_USER = os.getenv("DATABASE_USER", "user")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "password")
DATABASE_NAME = os.getenv("DATABASE_NAME", "synthetick_db")
DATABASE_PORT = os.getenv("DATABASE_PORT", "5432")

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_USER = os.getenv("REDIS_USER", "default")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "password")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
REDIS_DB = os.getenv("REDIS_DB", "0")

DATABASE_URL = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@db:{DATABASE_PORT}/{DATABASE_NAME}"
REDIS_URL = f"redis://{REDIS_USER}:{REDIS_PASSWORD}@redis:{REDIS_PORT}/{REDIS_DB}"

PROJECT_NAME = "Synthetick API"
VERSION = "1.0.0"

REQUEST_ID_SIZE = 12
