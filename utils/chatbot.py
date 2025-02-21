from openai import OpenAI
from dotenv import load_dotenv
from utils.prompt import prompt
import os


load_dotenv()
LLM_KEY = os.getenv("OPENAI_API_KEY")

#declare openai obj 
client=OpenAI(api_key=LLM_KEY)


def chat_route(messages):
    
    if not messages:
        return "Error, No messages Recieved."
    try:
        system_prompt={"role": "system", "content": prompt}
        messages.insert(0,system_prompt)
        
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        message_dict = completion.choices[0].message.content
        
        return message_dict
    except Exception as e:
            return "Exception has Occured."


    




