#Libraries
import pyttsx3
import speech_recognition as sr
import random

#setin engine
engine = pyttsx3.init()

#engine settings
engine.setProperty('rate', 40)
engine.setProperty('volume', 0.9)

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

        #model replies
        engine.say(ans)
    except:
        print('Error')

while True:
    record_volume()
    engine.runAndWait()

    x = 5