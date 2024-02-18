import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

token = f'{os.getenv('TOKEN')}'