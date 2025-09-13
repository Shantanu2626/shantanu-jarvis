import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
import os
from dotenv import load_dotenv
import google.generativeai as genai


load_dotenv() 
key = os.getenv('newsapi')
gemini_api_key = os.getenv('GEMINI_API_KEY')

genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    engine.stop()
    
def ask_ai(question):
    try:
        response = model.generate_content(question)
        if response and response.text:
            short_answer = " ".join(response.text.split(".")[:4]) + "."
            return short_answer
        else:
            return "Sorry, I didn't get a response from Gemini."    
    except Exception as e:
        return f"Error from Gemini: {e}"
        
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
    else:
        ai_answer = ask_ai(command)
        print("AI Response:", ai_answer)
        speak(ai_answer)

if __name__ == "__main__":
    speak("Initializing Jarvis...")
    while True:
        r = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                print("Listening...")
                speak("Listening...")
                r.adjust_for_ambient_noise(source, duration=1)
                audio = r.listen(source,timeout=3,phrase_time_limit=10)

            word = r.recognize_google(audio,language="en-IN")
            print(word)
            
            if word.lower() == "jarvis":
                speak("Yes Shantanu, how can I help you...")
                while True:
                  try:
                    with sr.Microphone() as source:
                     speak("Jarvis active Listening...")
                     r.adjust_for_ambient_noise(source, duration=1)
                     audio = r.listen(source, timeout=3, phrase_time_limit=10)
                     command = r.recognize_google(audio,language="en-IN")
                     print(command)
                     processCommand(command)
                     break
                  except sr.WaitTimeoutError:
                     print("Jarvis Active: No command detected, listening again...")
                     continue
                  except sr.UnknownValueError:
                     print("Jarvis Active: Could not understand, say again...")
                     continue
                    

        except sr.WaitTimeoutError:
            print("Timeout: Kuch nahi bola gaya.")
        except sr.UnknownValueError:
            print("Could not understand audio.")
        except sr.RequestError as e:
            print(f"Google API Error: {e}")
        except Exception as e:
            print(f"Unexpected Error: {e}")
