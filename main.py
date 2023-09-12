import os

# from db_connector import AWS_POSTGRE
from openai_api import OpenAI_API

from dotenv import load_dotenv
load_dotenv()

# db = AWS_POSTGRE()
ai = OpenAI_API()

# username = os.getenv("username")
# email = os.getenv("email")
# password = os.getenv("password")
# db.create_user(username, email, password, 20)
# user_id = db.user_login(username, email, password)
# db.insert_words(ai, user_id)


ai.website_designer()