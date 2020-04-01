from dotenv import load_dotenv
import os


load_dotenv()

APP_NAME = os.getenv("APP_NAME")
APP_URL = os.getenv("APP_URL")
API_TOKEN = os.getenv("API_TOKEN")

