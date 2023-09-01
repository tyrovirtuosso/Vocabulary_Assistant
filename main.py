import os
import openai
import ast

from utils import spelling_corrector
from db_connector import AWS_POSTGRE

from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
db = AWS_POSTGRE()
words = spelling_corrector(openai)
print(words)