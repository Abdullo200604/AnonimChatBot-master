from dotenv import load_dotenv
import os
from tortoise import Tortoise
load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

DB_URL = f'postgres://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

DB_CONFIG = {
    "connections": {
        "default": f"{DB_URL}",
    },
    "apps": {
        "models": {
            "models": ["models.user","models.plan", "aerich.models"],
            "default_connection": "default",
        }
    }
}


async def init_db():
    await Tortoise.init(config=DB_CONFIG)
    await Tortoise.generate_schemas()