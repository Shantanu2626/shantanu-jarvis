import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
import os
from dotenv import load_dotenv


load_dotenv() 
key = os.getenv('newsapi')
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    engine.stop()


def processCommand(command):
    if "open google" in command.lower():
        webbrowser.open("https://www.google.com")

    elif "open facebook" in command.lower():
        webbrowser.open("https://www.facebook.com")

    elif "open spotify" in command.lower():
        webbrowser.open("https://open.spotify.com/")

    elif "open youtube" in command.lower():
        webbrowser.open("https://www.youtube.com/")

    elif command.lower().startswith("play"):
        song = command.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)
        
    elif "news" in command.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={key}")
        if(r.status_code == 200):
         data = r.json()
         articles = data.get('articles' , [])
         for article in articles:
            speak(article['title'])

if __name__ == "__main__":
    speak("Initializing Jarvis...")
    while True:
        r = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                print("Listening...")
                r.adjust_for_ambient_noise(source, duration=1)
                audio = r.listen(source, timeout=5, phrase_time_limit=3)

            word = r.recognize_google(audio)
            print(word)

            if word.lower() == "jarvis":
                speak("Yes Shantanu, how can I help you...")
                with sr.Microphone() as source:
                    print("Jarvis active Listening...")
                    r.adjust_for_ambient_noise(source, duration=1)
                    audio = r.listen(source, timeout=4, phrase_time_limit=3)
                    command = r.recognize_google(audio)
                    print(command)
                    processCommand(command)

        except sr.WaitTimeoutError:
            print("Timeout: Kuch nahi bola gaya.")
        except sr.UnknownValueError:
            print("Could not understand audio.")
        except sr.RequestError as e:
            print(f"Google API Error: {e}")
        except Exception as e:
            print(f"Unexpected Error: {e}")
