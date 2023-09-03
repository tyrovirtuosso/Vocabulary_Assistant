from words import words
from categories import category_subcategory_dict
import ast


def use_model(openai, messages, model="gpt-3.5-turbo", temperature=0):
  response = openai.ChatCompletion.create(
      model=model,
      messages=messages,
      temperature=temperature,
      max_tokens=256,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
      )
  chat_response = response.choices[0].message.content
  return chat_response


def spelling_corrector(openai):
  messages = []
  words_string = " ".join(words)
  print(f"These are the words before correction: {words}")

  system_msg = {
    "role": "system",
    "content": "I will give you a list of words. I need you to check if the spelling of the words are correct and if not correct the spelling and return a list with the corrected words. Don't give anything else in the response, only return the completed and corrected list that i can use in python programming language."
    }
  user_msg = {"role": "user", "content": words_string}

  messages.append(system_msg)
  messages.append(user_msg)

  chat_response =use_model(openai, messages)
  
  word_corrected_list = ast.literal_eval(chat_response)
  return word_corrected_list 


    
def get_category_and_subcategory(openai, words):
  messages = []
  words_string = " ".join(words)
  
  system_msg = {
      "role": "system",
      "content": f"I will give you a list of words. I will need you to determine which category and subcategory each word belongs to and return it as a python dictionary that contains the word as key and for each value a dictionary where category and subcategory are keys. Only return the dictionary as output. Here is a dictionary that contains categories and the available subcategories for each category: {category_subcategory_dict}. It is an absolute must that you have to choose the category and subcategory from this dictionary"
      }
  user_msg = {"role": "user", "content": words_string}
  
  messages.append(system_msg)
  messages.append(user_msg)
  
  chat_response = use_model(openai, messages)
  print(chat_response)
  
  
def get_question(openai):
  messages = []
  word = 'Turpitude'
  system_msg = {
      "role": "system",
      "content": "I want you to be an vocabulary master and a general teacher for everything. I want you to give a challenging question to check if the user knows the meaning of the word, topic, popular figure, place or whatever that the user presents as input. There should only be the question in the output, nothing else."
      }
  user_msg = {"role": "user", "content": f"The Word/Topic is: {word}"}
  
  messages.append(system_msg)
  messages.append(user_msg)
  
  chat_response =use_model(openai, messages, model="gpt-4", temperature=1.3)
  print(chat_response)
  
def check_answer(openai):
  messages = []
  question = "If a patient is treated in a holistic manner in healthcare, what aspect is emphasis given more - physical symptoms only or the entire physical, mental, social and psychological condition and wellness?"
  system_msg = {
      "role": "system",
      "content": f"I want you to be an vocabulary master and a general teacher for everything. I want you to check whether the users answer to the following question is correct or not. If you think its correct, give the ouput as [1], otherwise give the output as [0]. In case the users answer is wrong and the output is 0, then after leaving a new line, give the reason why its wrong and the right answer to the question. Apart from what i specified, there shouldn't be anything else in the output. Heres the question:{question}"
      }
  answer = "Emphasis is given more to the conspicous symptoms"
  user_msg = {"role": "user", "content": f"{answer}"}
  
  messages.append(system_msg)
  messages.append(user_msg)
  
  chat_response =use_model(openai, messages, model="gpt-4", temperature=1.3)
  print(chat_response)
  

def get_meaning(openai):
  messages = []
  
  system_msg = {
      "role": "system",
      "content": f"You are a master of vocabulary and great teacher of teaching from first principles and simple manners that explain the nuanced details in an simple and elegant manner. The user will give a word or topic and you should give the meaning using simple language and first principles approach. Also give real life examples while explaining. Apart from what i specified, there shouldn't be anything else in the output"
      }
  
  word = "standard deviation"
  user_msg = {"role": "user", "content": f"{word}"}
  
  messages.append(system_msg)
  messages.append(user_msg)
  
  chat_response =use_model(openai, messages, model="gpt-4", temperature=0.2)
  print(chat_response)