import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import os
import sys

# Initialize speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 170)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Use female voice

def talk(text):
    print("Cutie:", text)
    engine.say(text)
    engine.runAndWait() 

def take_command():
    listener = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")    
        listener.adjust_for_ambient_noise(source)
        voice = listener.listen(source)
    try:
        command = listener.recognize_google(voice)
        command = command.lower()
        print("You said:", command)
    except sr.UnknownValueError:
        talk("Sorry bro, I didn’t catch that.")
        return ""
    except sr.RequestError:
        talk("Network issue with Google service.")
        return ""
    return command

def run_cutie():
    command = take_command()

    if "play" in command:
        song = command.replace("play", "")
        talk("Playing on YouTube ")
        pywhatkit.playonyt(song)

    elif "what is the time" in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk(f"It’s {time}")

    elif "who is Ram Charan" in command or "who is Konidela Ram Charan" in command:
        info = (
            "Charan, known as alwaysramcharan on Instagram, is an Indian Actor and producer. "
            "He is also knowm as megapower star and acts in pan india movies. "
        )
        talk(info)

    elif "who is" in command:
        person = command.replace("who is", "").strip()
        try:
            info = wikipedia.summary(person, sentences=1)
            talk(info)
        except:
            talk("Sorry, I couldn’t find information about that person.")

    elif "joke" in command:
        talk(pyjokes.get_joke())

    elif "open chrome" in command:
        chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
        if os.path.exists(chrome_path):
            talk("Opening Chrome ")
            os.startfile(chrome_path)
        else:
            talk("Chrome path not found ")

    elif "open code" in command or "open vs code" in command:
        talk("Opening VS Code")
        os.system("code")

    elif "exit" in command or "stop" in command:
        talk("Okay bro, see you later ")
        sys.exit()

    elif command != "":
        talk("I heard you, but I don’t understand that yet ")

talk("hi! I'm Cutie – your personal voice assistant. what's on your mind? tell me ")
while True:
    run_cutie()