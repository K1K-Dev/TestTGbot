import requests
import json

import telebot
bot = telebot.TeleBot('7718324508:AAEg0uJI_moQhjHKQXPYeVYabZEXKsjGhHE');

API_KEY = "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" 

#IsAntworted = False
MODEL = "deepseek/deepseek-r1"

def process_content(content):
    return content.replace('<think>', '').replace('</think>', '').replace('###', '').replace('**', '').replace("\\times", '*').replace('\\cdot', '*').replace('\\frac', '/').replace('\\sqr', '√')

def chat_stream(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "stream": True
    }

    with requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=data,
        stream=True
    ) as response:
        if response.status_code != 200:
            #print("Ошибка API:", response.status_code)
            return "Ошибка API:", response.status_code

        full_response = []
        
        for chunk in response.iter_lines():
            if chunk:
                chunk_str = chunk.decode('utf-8').replace('data: ', '')
                try:
                    chunk_json = json.loads(chunk_str)
                    if "choices" in chunk_json:
                        content = chunk_json["choices"][0]["delta"].get("content", "")
                        if content:
                            cleaned = process_content(content)
                            #print(cleaned, end='', flush=True)
                            full_response.append(cleaned)
                except:
                    pass

        #IsAntworted = False
        return ''.join(full_response)
    


@bot.message_handler(content_types=['text'])
def start(message):
    #if(IsAntworted == False):
    if message != ' ':
        msgFrage = bot.send_message(message.from_user.id, "Запрос принят, готовлю ответ");
        #bot.send_message(message.from_user.id, chat_stream(message.text));
        #bot.edit_message_text(message.id, chat_stream(message.text))
        answ = chat_stream(message.text)
        ##answ.replace("###", " ").replace("**", " ")
        #bot.edit_message_text(chat_id = message.from_user.id, message_id = test.message_id, text = answ)
        #bot.send_message(message.from_user.id, chat_stream(message.text));
        if answ != '':
            bot.edit_message_text(chat_id=message.chat.id, message_id=msgFrage.message_id, text=answ)
        else:
            bot.edit_message_text(chat_id=message.chat.id, message_id=msgFrage.message_id, text="извите не смог найти ответ, попробуйте еще раз задать вопрос")

    #IsAntworted == True
    #bot.send_message(chat_stream(message.text))



bot.polling(none_stop=True, interval=0)
