#Libraries
import pyttsx3
import speech_recognition as sr
import random
import requests
import subprocess
import os

open_weather_token = 'a47d6ab82e58378d27beefdd5318771c'
city = "Moscow"

#setin engine
engine = pyttsx3.init()

#engine settings
engine.setProperty('rate', 40)
engine.setProperty('volume', 0.9)
engine.setProperty('voice', 'com.apple.voice.compact.ru-RU.Milena')

#moods
mood = ['Отлично', 'Всё в порядке', 'Отстань', 'пока не родила азазазазаз']

def record_volume():
    r = sr.Recognizer()

    with sr.Microphone(device_index=0) as source:
        print('Настраиваюсь.')
        r.adjust_for_ambient_noise(source, duration=0.5)
        print('Слушаю...')
        audio = r.listen(source)

    print('Услышала.')

    try:
        ans = ''

        query = r.recognize_google(audio, language='ru-RU')
        text = query.lower()

        #checking basic scenarios
        if 'привет' in text or 'Добрый' in text:
            ans += 'Здравствуйте'

        if 'как' in text and 'дела' in text:
            ans += (random.choice(mood) + 'а у вас')

        if 'я' in text and 'люблю' in text and 'тебя' in text:
            ans += ('Если ваш день вдруг станет пасмурным, подойдите к зеркалу и увидите солнышко')

        if 'погода' in text or 'температура' in text:
            result = requests.get(
                f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric"
            )
            data = result.json()
            ans += ("Температура в Москве " + str(
                data['main']['temp']) + "Ощущается как " + str(data['main']['feels_like']))
        if 'telegram' in text:
            subprocess.Popen(["open", '/Applications/Telegram.app'])

        #model replies
        print(text)
        engine.say(ans)
    except:
        print('Error')

while True:
    record_volume()
    engine.runAndWait()