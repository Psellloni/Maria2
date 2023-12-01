#Libraries
import pyttsx3
import speech_recognition as sr
import requests
import json
from difflib import get_close_matches
import subprocess

open_weather_token = 'a47d6ab82e58378d27beefdd5318771c'
city = "Moscow"

#setin engine
engine = pyttsx3.init()

#engine settings
engine.setProperty('rate', 100)
engine.setProperty('volume', 0.9)
engine.setProperty('voice', 'com.apple.voice.compact.ru-RU.Milena')

r = sr.Recognizer()

#moods
mood = ['Отлично', 'Всё в порядке', 'Отстань', 'пока не родила азазазазаз']

def load_knowledge_basis(file_path: str):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def save_knowledge_base(filepath: str, data: dict):
    with open(filepath, 'w') as file:
        json.dump(data, file, indent=2)

def find_friends(user_input: str, questions: list[str]):
    matches = get_close_matches(user_input, questions, n=1, cutoff=0.6)

    if matches:
        return matches[0]
    else:
        return None

def get_answer(question: str, knowledge_base: dict):
    for val in knowledge_base['questions']:
        if val['question'] == question:
            return val['answer']

def recognize_text(flag=False):
    with sr.Microphone(device_index=0) as source:
        print('Настраиваюсь.')
        r.adjust_for_ambient_noise(source, duration=0.5)
        print('Слушаю...')
        audio = r.listen(source)

    print('Услышала.')

    try:
        query = r.recognize_google(audio, language='ru-RU')
        return query.lower()
    except:
        print('Error')

def brain():
    base = load_knowledge_basis('knowledge_basis.json')
    ans = ''

    text = recognize_text()

    best_match = find_friends(text, [val['question'] for val in base['questions']])

    if 'погода' in text or 'температура' in text:
        result = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric"
        )
        data = result.json()
        engine.say("Температура в Москве " + str(
            data['main']['temp']) + "Ощущается как " + str(data['main']['feels_like']))
    elif 'пока' in text:
        engine.say('Всего доброго')
        return False
    elif 'telegram' in text:
        engine.say('Запускаю телеграм')
        subprocess.Popen(["open", '/Applications/Telegram.app'])
    else:
        if best_match:
            engine.say(get_answer(best_match, base))
        else:
            engine.say('Я не знаю что ответить, какой правильный ответ?')
            engine.runAndWait()
            curr_ans = recognize_text()

            base['questions'].append({'question': text, 'answer': curr_ans})
            save_knowledge_base('knowledge_basis.json', base)
            engine.say('Спасибо, моя база знаний пополнилась')
    return True
def main():
    while True:
        flag = brain()
        engine.runAndWait()

        if flag == False:
            break

if __name__ == '__main__':
    main()