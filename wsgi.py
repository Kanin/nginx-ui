from app import create_app
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


app = create_app()
