from words import words
import ast

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
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
        )
    chat_response = response.choices[0].message.content
    word_corrected_list = ast.literal_eval(chat_response)
    return word_corrected_list 


    
