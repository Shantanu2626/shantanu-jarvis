import speech_recognition as sr
import webbrowser
import pyttsx3

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    engine.stop()


def processCommand(command):
   if "open google" in command.lower():
       webbrowser.open("https://www.google.com")

   if "open facebook" in command.lower():
       webbrowser.open("https://www.facebook.com")

   if "open spotify" in command.lower():
       webbrowser.open("https://open.spotify.com/")

   if "open you tube" in command.lower():
       webbrowser.open("https://www.youtube.com/")


if __name__ == "__main__":
    speak("Initializing Jarvis...")
    try:
        while True:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source,timeout=2, phrase_time_limit=3)  # timeout=2, phrase_time_limit=1

            word = r.recognize_google(audio)
            print(word)

            if(word.lower() == "jarvis"):
                speak("Yes Shantanu How can i help you...")
                with sr.Microphone() as source:
                    print("Jarvis active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)
                    processCommand(command)

    except Exception as e:
        print(f"Error: {e}")
