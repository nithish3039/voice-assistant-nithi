import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import pywhatkit
import webbrowser
import pyjokes
import requests

engine = pyttsx3.init()
engine.setProperty('rate', 175)
engine.setProperty('volume', 1.0)

def speak(text):
    print(f"Nithi: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    listener = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = listener.listen(source)
    try:
        command = listener.recognize_google(audio)
        print(f"You said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
        return ""
    except sr.RequestError:
        speak("Speech recognition service is down.")
        return ""

def get_weather(city):
    api_key = "YOUR_API_KEY"  # Replace with OpenWeatherMap API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url).json()
        if response["cod"] == 200:
            temp = response['main']['temp']
            desc = response['weather'][0]['description']
            return f"The temperature in {city} is {temp}°C with {desc}"
        else:
            return "City not found."
    except Exception:
        return "Unable to fetch weather right now."

def run_nithi():
    speak("Hello! I am Nithi, your personal assistant. How can I help you?")
    while True:
        command = listen()
        if not command:
            continue

        if "time" in command:
            time = datetime.datetime.now().strftime('%I:%M %p')
            speak(f"The current time is {time}")

        elif "date" in command:
            date = datetime.datetime.now().strftime('%d %B %Y')
            speak(f"Today's date is {date}")

        elif "search" in command:
            topic = command.replace("search", "").strip()
            speak(f"Searching Wikipedia for {topic}")
            try:
                result = wikipedia.summary(topic, sentences=2)
                speak(result)
            except Exception:
                speak("Sorry, I couldn't find anything.")

        elif "play" in command:
            song = command.replace("play", "").strip()
            speak(f"Playing {song} on YouTube")
            try:
                pywhatkit.playonyt(song)
            except Exception:
                speak("Unable to play the song right now.")

        elif "open chrome" in command:
            speak("Opening Google Chrome")
            webbrowser.open("https://www.google.com")

        elif "weather" in command:
            city = command.replace("weather", "").strip()
            if city == "":
                city = "New York"
            speak(get_weather(city))

        elif "joke" in command:
            speak(pyjokes.get_joke())

        elif "exit" in command or "quit" in command:
            speak("Goodbye!")
            break

        else:
            speak("I can open Chrome, tell weather, play music, search Wikipedia, and tell jokes.")

if __name__ == "__main__":
    run_nithi()
