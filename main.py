# dependencies
import speech_recognition as sr  # recognise speech
import playsound as ps  # to play an audio file
from gtts import gTTS  # google text to speech
import pyjokes  # to get jokes
import pyautogui  # for typing
import pywhatkit  # to search on google and youtube

# python modules
import random
from time import ctime  # get time details
from time import sleep
import os  # to remove created audio files
import sys


class Person:
    name = ''

    def set_name(self, name):
        self.name = name


def there_exists(terms):
    for term in terms:
        if term in voice_data:
            return True


r = sr.Recognizer()  # initialise a recogniser


# listen for audio and convert it to text:
def record_audio(ask=False):
    print("I'm listening...")
    with sr.Microphone() as source:  # microphone as source
        if ask:
            speak(ask)
        audio = r.listen(source)  # listen for the audio via source
        voice_data = ''
        try:
            voice_data = r.recognize_google(audio)  # convert audio to text
        except sr.UnknownValueError:  # error: recognizer does not understand
            speak('I did not get that')
        except sr.RequestError:
            speak('Sorry, the service is down')  # error: recognizer is not connected
        print(f">> {voice_data.lower()}")  # print what user said
        return voice_data.lower()


# type the given text
def type(text):
    for letter in text:
        pyautogui.press(letter)
        sleep(0.1)


# get string and make a audio file to be played
def speak(audio_string):
    tts = gTTS(text=audio_string, lang='en')  # text to speech(voice)
    r = random.randint(1, sys.maxsize)
    audio_file = f'audio-{r}.mp3'
    tts.save(audio_file)  # save as mp3
    ps.playsound(audio_file)  # play the audio file
    print(f"siri: {audio_string}")  # print what app said
    os.remove(audio_file)  # remove audio file


def respond(voice_data):
    # 1: greeting
    if there_exists(['hey', 'hi', 'hello', 'hey siri']):
        if person_obj.name:
            greetings = [f"Hey, how can I help you? {person_obj.name}", f"Hey, what's up? {person_obj.name}",
                         f"I'm listening {person_obj.name}", f"How can I help you? {person_obj.name}",
                         f"Hello {person_obj.name}!"]
            greet = random.choice(greetings)
            speak(greet)
        else:
            greetings = ["Hey, how can I help you?", "Hey, what's up?",
                         "I'm listening", "How can I help you?",
                         f"Hello!"]
            greet = random.choice(greetings)
            speak(greet)

    # 2: name
    elif there_exists(["what is your name", "what's your name", "tell me your name"]):
        if person_obj.name:
            speak("My name is Siri")
        else:
            speak("My name is Siri. What's your name?")
            print('You should say: "my name is __" ')
            if there_exists(["my name is"]):
                person_name = voice_data.split("is")[-1].strip()
                speak(f"Okay, i will remember that, {person_name}")
                person_obj.set_name(person_name)  # remember name in person object

    elif there_exists(['what is my name', "what's my name"]):
        if person_obj.name:
            speak(f"You're asking me? {person_obj.name}")
        else:
            speak("I don't know it yet. What is it?")
            person_name = record_audio()
            speak(f"Okay, i will remember that, {person_name}")
            person_obj.set_name(person_name)  # remember name in person object

    # 3: greeting
    elif there_exists(["how are you", "how are you doing"]):
        if person_obj.name:
            speak(f"I'm very well, thanks for asking {person_obj.name}")
        else:
            speak("I'm very well, thanks for asking")

    # 4: time
    elif there_exists(["what's the time", 'what is the time', "tell me the time", "what time is it"]):
        time = ctime().split(" ")[3].split(":")[0:2]
        if time[0] == "00":
            hours = '12'
        else:
            hours = time[0]
        minutes = time[1]
        time = f'The time is {hours}:{minutes}'
        speak(time)

    # 5: date
    elif there_exists(["what's the date", 'what is the date', 'what date is it']):
        full_time = ctime().split(' ')
        full_time.remove(full_time[3])
        date = ''
        for i in full_time:
            date += i + ' '
        speak(date)

    # 6: search google
    elif there_exists(["search for"]) and 'youtube' not in voice_data and 'wikipedia' not in voice_data:
        search_term = voice_data.split("for")[-1]
        pywhatkit.search(search_term)
        speak(f'Here is what I found for {search_term} on google')
        exit()

    # 7: search youtube
    elif there_exists(["on youtube"]):
        search_term = voice_data.split("for")[-1].replace('on youtube', '').replace('youtube', '').replace('search', '')
        pywhatkit.playonyt(search_term)
        speak(f'Here is what I found for {search_term} on youtube')
        exit()

    # 8: search wikipedia
    elif there_exists(["on wikipedia"]):
        search_term = voice_data.split("for")[-1].replace('on wikipedia', '').replace('wikipedia', '').replace('search', '')
        print(pywhatkit.info(search_term))
        speak(f'Here is what I found for {search_term} on wikipedia')
        exit()

    # 9: tell a joke
    elif there_exists(['tell me a joke']):
        speak(pyjokes.get_joke('en'))

    # 10: weather
    elif there_exists(['what is the weather', "what's the weather"]):
        speak('What location are you looking for?')
        answer = record_audio()
        pywhatkit.search(f'weather {answer}')

    # 11: send a whatsapp message
    elif there_exists(['send a whatspp message', 'send a message', 'message']):
        speak('Who do you want to send it to?')
        recipient = record_audio()
        speak('What do you want to say?')
        message = record_audio()
        while True:
            speak('Are you sure?')
            answer = record_audio()
            if answer == 'yes':
                break
            speak('So, what do you want to say?')
            message = record_audio()

        # open whatsapp web
        pyautogui.moveTo(1450, 1060, 1.5)
        pyautogui.doubleClick()
        pyautogui.moveTo(1780, 85, 2)
        pyautogui.click()
        pyautogui.sleep(6)

        # search for the contact
        pyautogui.moveTo(1580, 175, 0.5)
        pyautogui.click()
        type(recipient)

        # open the chat
        pyautogui.moveTo(1390, 300, 0.5)
        pyautogui.click()

        # write the message and send it
        pyautogui.moveTo(1115, 990, 0.5)
        pyautogui.click()
        type(message)
        pyautogui.press('enter')
        exit()

    # 12: spam your friend
    elif there_exists(['annoying bot', 'bothering bot', 'annoy', 'annoying', 'bother', 'bothering']):
        speak('Who do you want to spam?')
        recipient = record_audio()
        speak('What message do you want to spam with?')
        message = record_audio()
        while True:
            speak('Are you sure?')
            answer = record_audio()
            if answer == 'yes':
                break
            speak('So, what do you want to spam with?')
            message = record_audio()

        # open whatsapp web
        pyautogui.moveTo(1450, 1060, 1.5)
        pyautogui.doubleClick()
        pyautogui.moveTo(1780, 85, 2)
        pyautogui.click()
        pyautogui.sleep(7)

        # search for the contact
        pyautogui.moveTo(1578, 174, 0.5)
        pyautogui.click()
        type(recipient)

        # open the chat
        pyautogui.moveTo(1390, 300, 0.5)
        pyautogui.click()

        # go to textbox
        pyautogui.moveTo(1115, 990, 0.5)
        pyautogui.click()

        # spam
        for i in range(100):
            # write the message and send it
            type(message)
            pyautogui.press('enter')
            sleep(0.2)
        exit()

    # 13: speech to text
    elif there_exists(['write my words', 'write']):
        # go to the end and add long comment sign
        speak('Just a second...')
        for i in range(271):
            pyautogui.press('down')
        words = "'''"
        type(words)
        pyautogui.press('enter')
        pyautogui.press('enter')
        pyautogui.press('up')

        # get user input
        speak('What do you want to write?')
        while True:
            words = record_audio()
            # stop typing
            if 'exit' in words:
                speak('Shutting down...')
                break
            # type
            type(words)
            pyautogui.press('enter')

    # 14: exit
    elif there_exists(["exit", "quit", "goodbye", 'stop']):
        speak("Going offline...")
        exit()


sleep(1)
person_obj = Person()
while True:
    voice_data = record_audio()  # get the voice input
    respond(voice_data)  # respond

