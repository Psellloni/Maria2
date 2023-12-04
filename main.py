# Libraries
import pyttsx3
import speech_recognition as sr
import requests
import json
from difflib import get_close_matches
import subprocess
import bs4
import webbrowser
import random

# setting weather parametrs
token = 'a47d6ab82e58378d27beefdd5318771c'
city = "Moscow"

# seting engine
engine = pyttsx3.init()
engine.setProperty('rate', 100)
engine.setProperty('volume', 0.9)
engine.setProperty('voice', 'com.apple.voice.compact.ru-RU.Milena')

# setting speech recognizer
r = sr.Recognizer()

class Audio:
    @staticmethod
    def recognize_text():
        with sr.Microphone(device_index=0) as source:
            print('Настраиваюсь.')
            r.adjust_for_ambient_noise(source, duration=0.5)
            print('Слушаю...')
            data = r.listen(source)

        print('Услышала.')

        try:
            query = r.recognize_google(data, language='ru-RU')

            return query.lower()

        except:
            print('Error')

class Words_game:
    @staticmethod
    def play():
        with open('words_base.json', 'r') as file:
            data = json.load(file)
            curr = "роза"

            engine.say("я начну")
            engine.say(curr)
            engine.runAndWait()

            while True:
                curr_letter = curr[-1]

                engine.say("вам на " + curr_letter)
                engine.runAndWait()

                user_input = Audio.recognize_text()
                user_input = user_input.replace(' ', '')

                if user_input == 'стоп':
                    break

                else:
                    if user_input[0] == curr_letter:
                        if user_input[-1] in ["ъ", "ь", "ы"]:
                            curr = random.choice(data[user_input[-2]])

                        else:
                            curr = random.choice(data[user_input[-1]])

                        engine.say(curr)
                        engine.runAndWait()
                    else:
                        engine.say("это слово не на букву " + curr_letter)
                        engine.runAndWait()


class Browser:
    @staticmethod
    def open_browser(input: str):

        webbrowser.open('https://www.google.com/search?q=' + input)


class Anecdote:
    @staticmethod
    def get_joke():
        response = requests.get('http://anekdotme.ru/random')

        unparsed = bs4.BeautifulSoup(response.text, "html.parser")

        data = unparsed.select('.anekdot_text')

        for value in data:
            return value.getText().strip()
            break


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
            json.dump(data, file, indent=2)

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

class Maria:
    @staticmethod
    def brain():
        base = DataBase.load_knowledge_basis('knowledge_basis.json')

        text = Audio.recognize_text()

        best_match = DataBase.find_friends(text, [val['question'] for val in base['questions']])

        if 'погода' in text or 'температура' in text:
            real, relative = Weather.get_weather()

            engine.say("Температура в Москве " + real + "Ощущается как " + relative)

        elif 'пока' in text:
            engine.say('Всего доброго')

            return False

        elif 'telegram' in text:
            engine.say('Запускаю телеграм')

            subprocess.Popen(["open", '/Applications/Telegram.app'])

        elif 'discord' in text:
            engine.say('Запускаю дискорд')

            subprocess.Popen(["open", '/Applications/Discord.app'])

        elif 'шутк' in text or 'анекдот' in text:
            reply = Anecdote.get_joke()

            engine.say(reply)

        # модуль не работает
        # elif 'загугли' in text:
        #     Browser.open_browser(text)
        #     print(text)

        # дописать возможность обучаться
        elif 'давай' in text or 'поиграем' in text or 'слова' in text:
            Words_game.play()

        else:
            if best_match:
                engine.say(DataBase.get_answer(best_match, base))

            else:
                engine.say('Я не знаю что ответить, какой правильный ответ?')
                engine.runAndWait()

                curr_ans = Audio.recognize_text()
                base['questions'].append({'question': text, 'answer': curr_ans})
                DataBase.save_knowledge_base('knowledge_basis.json', base)

                engine.say('Спасибо, моя база знаний пополнилась')

        return True


def main():
    while True:
        flag = Maria.brain()
        engine.runAndWait()

        if not flag:
            break


if __name__ == '__main__':
    main()
