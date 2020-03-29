from dotenv import load_dotenv
import ast
import os


load_dotenv()

APP_NAME = os.getenv("APP_NAME")
APP_URL = os.getenv("APP_URL")

DB_CONNECTION_URL = os.getenv("DB_CONNECTION_URL")

