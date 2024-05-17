import tkinter as tk
from tkinter import scrolledtext
from tkinter import PhotoImage
#from PIL import Image, ImageTk  
import time
import speech_recognition as sr
import os
import webbrowser
import win32com.client
import datetime
from config import apikey
import google.generativeai as genai


genai.configure(api_key = apikey)
i=0
# Set up the model
generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 256,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro-001",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

convo = model.start_chat(history=[])



speaker = win32com.client.Dispatch("SAPI.SpVoice")

def print1():
    label.config(text="G.E.M.I.N.I A.I")
    speaker.Speak("Hello my name is Vision A.I. Your all new Virtual Assistant")
    history_text.insert(tk.END, "AI: Hello my name is Vision A.I. Your all new Virtual Assistant" + "\n")
    history_text.see(tk.END)  # Scrolls the text widget to the end
    print()
  


def print():
    while True:
        global i
        i=i+1
        
        a= takeCommand()
        history_text.insert(tk.END, "User: "+a + "\n")
        history_text.see(tk.END)  # Scrolls the text widget to the end
        speaker.Speak("1")
        ai_out(a)
        speaker.Speak("3")
        
        time.sleep(2)


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # r.pause_threshold =  0.6
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language="en-in")
            #print("Recognizing...")
            speaker.Speak("Processing Voice Input")
            #print(f"User said: {query}")
            return query
        except Exception as e:
            return "Some Error Occurred. Sorry from Jarvis"
        

def ai_out(a):
    speaker.Speak("2")
    query = a
    sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"], ["google", "https://www.google.com"],]
    for site in sites:
        if f"Open {site[0]}".lower() in query.lower():
            history_text.insert(tk.END, "AI: "+f"Opening {site[0]} sir..." + "\n")
            history_text.see(tk.END)
            if i > 10:
                history_text.delete('1.0', '2.0')  # Delete the oldest number if more than 5 are displayed
            label.update()
            speaker.Speak(f"Opening {site[0]} sir...")
            webbrowser.open(site[1])
    
    
    if "open music" in query.lower():
        musicPath = "C:\Users\adyasha\Music\once-in-paris-168895.mp3"
        history_text.insert(tk.END, "AI: "+f"Opening music sir..." + "\n")
        history_text.see(tk.END)
        if i > 10:
                history_text.delete('1.0', '2.0')  # Delete the oldest number if more than 5 are displayed
        label.update()
        speaker.Speak("Opening Music Sir...")
        os.startfile(musicPath)
        return
    
    elif "the time" in query.lower():
        hour = datetime.datetime.now().strftime("%H")
        min = datetime.datetime.now().strftime("%M")
        history_text.insert(tk.END, "AI: "+f"Sir time is {hour} hours & {min} minutes" + "\n")
        history_text.see(tk.END)
        if i > 10:
                history_text.delete('1.0', '2.0')  # Delete the oldest number if more than 5 are displayed
        label.update()
        speaker.Speak(f"Sir time is {hour} hours & {min} minutes")
        return
    else:
        #speaker.Speak(query)
        convo.send_message(query)
        j=0
        while (j<1):
            AIoutput = convo.last.text
            if AIoutput== None:
                 continue
            else:
                 j=1
        
        j=0
        history_text.insert(tk.END, "AI: "+AIoutput + "\n")
        history_text.see(tk.END)
        if i > 10:
                history_text.delete('1.0', '2.0')  # Delete the oldest number if more than 5 are displayed
        label.update()
        speaker.Speak(AIoutput)
        return


# Create the main window
root = tk.Tk()
root.title("Number Printer")

# Create a label to display the current number
label = tk.Label(root, font=("Helvetica", 48))
label.pack(padx=20, pady=20)



# Create a scrolled text widget to display the history of printed numbers
history_text = scrolledtext.ScrolledText(root, width=150, height=20)
history_text.pack(padx=20, pady=20)

# Call the function to print numbers
print1()

root.mainloop()
