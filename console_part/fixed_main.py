from datetime import datetime
import speech_recognition as sr
import pyttsx3
import webbrowser
import wolframalpha
import wikipedia

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

# Wolfram Alpha client
appID = "U7RV6H-4LRPGQHG78"
wolframClient = wolframalpha.Client(appID)


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


def search_wikipedia(query=""):
    searchResults = wikipedia.search(query)
    if not searchResults:
        print("No Wikipedia result")
        return "No result received"
    try:
        wikiPage = wikipedia.page(searchResults[0])
    except wikipedia.DisambiguationError as error:
        wikiPage = wikipedia.page(error.options[0])
    print(wikiPage.title)
    wikiSummary = str(wikiPage.summary)
    return wikiSummary


def listOrDict(var):
    if isinstance(var, list):
        return var[0]["plaintext"]
    else:
        return var["plaintext"]


def search_wolframalpha(query=""):
    response = wolframClient.query(query)

    if response["@success"] == "false":
        return "Could not compute"
    # Query Resolved
    else:
        result = ""
        # Question, what was asked
        pod0 = response["pod"][0]
        pod1 = response["pod"][1]
        # May contain the answer, has the highest confidence value
        # if it's primary or has the title of result or definition, then it is the official result
        if (("result") in pod1["@title"].lower()) or (pod1.get("@primary", "false") == "true") or ("definition" in pod1["@title"].lower()):
            # Get the result
            result = listOrDict(pod1["subpod"])
            # remove the bracketed section
            return result.split('(')[0]
        else:
            question = listOrDict(pod0["subpod"])
            # remove the bracketed section
            return question.split('(')[0]
            # search wikipedia instead
            speak("Computation failed. Querying universal databank.")
            return search_wikipedia(question)


# Main Loop
if __name__ == "__main__":
    speak("Activated...")

    while True:
        query = None
        while query is None:  # Keep listening until a valid command is received
            query = parseCommand()
            if query is None:
                print("Waiting for another command...")

        query = query.lower().split()

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
            elif query[0] == "go" and query[1] == "to":
                speak("Opening...")
                query = " ".join(query[2:])
                webbrowser.get("chrome").open_new(query)

            # Wikipedia
            elif query[0] == "wikipedia":
                query = " ".join(query[1:])
                speak("Querying the universal databank.")
                speak(search_wikipedia(query))

            # Wolfram Alpha
            elif query[0] == "compute" or query[0] == "computer":
                query = " ".join(query[1:])
                speak("Computing")
                try:
                    result = search_wolframalpha(query)
                    speak(result)
                except:
                    speak("Unable to compute.")

            # Note taking
            elif query[0] == "log":
                speak("Ready to record your note")
                newNote = None
                while newNote is None:  # Keep listening until a valid note is received
                    newNote = parseCommand()
                    if newNote is None:
                        speak("I could not catch that. Please repeat your note.")
                newNote = newNote.lower()
                now = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
                with open("note_%s.txt" % now, "w") as newFile:
                    newFile.write(newNote)
                speak("Note written")

            elif query[0] == "exit":
                speak("Goodbye")
                break
