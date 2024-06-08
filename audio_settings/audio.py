from datetime import datetime
import speech_recognition as sr
import pyttsx3
import webbrowser
import wolframalpha


#! Speech Engine Initialization
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voices", voices[1].id)  # 0 - male, 1 - female
# whenever computer hears this word, AI Assistant activates
activationWord = "computer"

# Configure browser
# Set the path
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
webbrowser.register("chrome", None, webbrowser.BackgroundBrowser(chrome_path))


def speak(text, rate=120):
    engine.setProperty("rate", rate)
    engine.say(text)
    engine.runAndWait()


def parseCommand():
    listener = sr.Recognizer()
    print("Listening for a command...")

    with sr.Microphone() as source:
        listener.pause_threshold = 1
        input_speech = listener.listen(source)

    try:
        print("Recognizing Speech...")
        query = listener.recognize_google(input_speech, language="en_gb")
        print(f"The input speech was: {query}")
    except Exception as exception:
        print("I could not catch it...")
        speak("I could not catch it.")

        print(exception)
        return None

    return query


if __name__ == "__main__":
    speak("Activated...")

    while True:
        # Parse as a list
        query = parseCommand().lower().split()

        if query[0] == activationWord:
            query.pop(0)

            # List commands
            if query[0] == "say":
                if "hello" in query:
                    speak("Hello! My Boss!")
                else:
                    query.pop(0)  # remove say
                    speech = " ".join(query)
                    speak(speech)

            # Navigation
            if query[0] == "go" and query[1] == "to":
                speak("Opening...")
                query = " ".join(query[2:])
                webbrowser.get("chrome").open_new(query)
