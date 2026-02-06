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

    DEFAULT_DELIVERY_PERCENT = 3.0
    DEFAULT_STORAGE_PERCENT = 2.0
    DEFAULT_ADDITIONAL_COSTS_PERCENT = 1.5

    USD_TO_RUB_EXCHANGE_RATE = 90.0

    MAX_PRODUCTS_PER_REQUEST = 5
    MIN_SEARCH_TEXT_LENGTH = 3

    @classmethod
    def validate(cls) -> list:
        errors = []

        if not cls.TELEGRAM_TOKEN:
            errors.append("TELEGRAM_BOT_TOKEN")

        if not cls.GROQ_API_KEY:
            errors.append("GROQ_API_KEY")

        if cls.GROQ_TEMPERATURE < 0.0 or cls.GROQ_TEMPERATURE > 2.0:
            errors.append("GROQ_TEMPERATURE")

        if cls.MAX_SUPPLIERS_PER_PRODUCT <= 0:
            errors.append("MAX_SUPPLIERS_PER_PRODUCT")

        if cls.DEFAULT_DELIVERY_PERCENT < 0.0:
            errors.append("DEFAULT_DELIVERY_PERCENT")

        if cls.DEFAULT_STORAGE_PERCENT < 0.0:
            errors.append("DEFAULT_STORAGE_PERCENT")

        if cls.DEFAULT_ADDITIONAL_COSTS_PERCENT < 0.0:
            errors.append("DEFAULT_ADDITIONAL_COSTS_PERCENT")

        if cls.USD_TO_RUB_EXCHANGE_RATE <= 0.0:
            errors.append("USD_TO_RUB_EXCHANGE_RATE")

        if cls.MAX_PRODUCTS_PER_REQUEST <= 0:
            errors.append("MAX_PRODUCTS_PER_REQUEST")

        if cls.MIN_SEARCH_TEXT_LENGTH <= 0:
            errors.append("MIN_SEARCH_TEXT_LENGTH")

        return errors

    @classmethod
    def is_valid(cls) -> bool:
        return len(cls.validate()) == 0