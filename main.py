import requests
import json
from difflib import get_close_matches
import wikipedia

# some parametrs
token = 'a47d6ab82e58378d27beefdd5318771c'
city = "Moscow"
flag = False
question = ''

class Weather:
    @staticmethod
    def get_weather():
        result = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={token}&units=metric")
        data = result.json()

        return str(data['main']['temp']), str(data['main']['feels_like'])


class DataBase:
    @staticmethod
    def load_knowledge_basis(file_path: str):
        with open(file_path, 'r') as file:
            data = json.load(file)

        return data

    @staticmethod
    def save_knowledge_base(filepath: str, data: dict):
        with open(filepath, 'w') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

    @staticmethod
    def find_friends(user_input: str, questions: list[str]):
        matches = get_close_matches(user_input, questions, n=1, cutoff=0.6)

        if matches:
            return matches[0]

        else:
            return None

    @staticmethod
    def get_answer(question: str, knowledge_base: dict):
        for val in knowledge_base['questions']:
            if val['question'] == question:

                return val['answer']

class DataHandler:
    @staticmethod
    def brain(text):
        global flag
        global question

        base = DataBase.load_knowledge_basis('knowledge_basis.json')
        best_match = DataBase.find_friends(text, [val['question'] for val in base['questions']])

        if 'погода' in text or 'температура' in text:
            real, relative = Weather.get_weather()

            return ("Температура в Москве " + real + "Ощущается как " + relative)

        elif 'пока' in text:
            return ('Вы уже уходите? Я буду скучать')

        elif 'загугл' in text:
            text = text.replace('загугли ', '')
            wikipedia.set_lang('ru')
            try:
                reply = wikipedia.summary(text)
                return reply
            except:
                return 'Ничего не нашла на эту тему'

        elif flag:
            base['questions'].append({'question': question, 'answer': text})
            DataBase.save_knowledge_base('knowledge_basis.json', base)
            flag = False
            question = ''
            return ('Спасибо, моя база знаний пополнилась')

        else:
            if best_match:
                return (DataBase.get_answer(best_match, base))

            else:
                flag = True
                question = text
                return ('Я не знаю что ответить, какой правильный ответ?')