import os
import openai

from utils import spelling_corrector, get_category_and_subcategory, get_question, check_answer, get_meaning
from db_connector import AWS_POSTGRE
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
db = AWS_POSTGRE()

db.create_user('sj', "shanejms2@gmail.com", 'shane100', 20)
db.user_login('sj', 'shanejms2@gmail.com', 'shane100')
# words = spelling_corrector(openai)
# get_category_and_subcategory(openai, words)

get_meaning(openai)