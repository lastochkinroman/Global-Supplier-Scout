import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')

    GROQ_MODEL = "llama3-70b-8192"
    GROQ_TEMPERATURE = 0.7

    TEMP_DIR = "temp_reports"
    MAX_SUPPLIERS_PER_PRODUCT = 5

    DEFAULT_DELIVERY_PERCENT = 3
    DEFAULT_STORAGE_PERCENT = 2
    DEFAULT_ADDITIONAL_COSTS_PERCENT = 1.5
