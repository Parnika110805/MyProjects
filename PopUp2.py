import pandas as pd
from tkinter import Tk, Button, Label
from PIL import Image, ImageTk
import webbrowser
import time
from gtts import gTTS
import os
from deep_translator import GoogleTranslator
import threading

def ExtractData(csv_file):
    try:
        df = pd.read_csv(csv_file)
        return df
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return None

def SpeakText(course_details, language):
    try:
        click_here_text = TranslateText("Click Here", language)
        full_text = f"{course_details} {click_here_text}"
        tts = gTTS(text=full_text, lang=language)
        tts.save("temp_audio.mp3")
        os.system("start temp_audio.mp3")

    except Exception as e:
        print(f"Error in text-to-speech: {e}")

def TranslateText(text, lang):
    try:
        translation = GoogleTranslator(source='auto', target=lang).translate(text)
        return translation
    except Exception as e:
        print(f"Error in translation: {e}")
        return text
def ShowPopUp(edu_row, background_path):
    try:
        course_name = edu_row['Course name']
        link = edu_row['Link']

        if language != 'en':
            course_name = TranslateText(course_name, language)

        course_details = f"Course Name: {course_name}."
        threading.Thread(target=SpeakText, args=(course_details, language)).start()

        window = Tk()
        window.title("Course Notification")
        window.geometry("800x800")

        background = Image.open(background_path)
        background = background.resize((800, 800), Image.Resampling.LANCZOS)
        bg_image = ImageTk.PhotoImage(background)

        bg_label = Label(window, image=bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        Label(window, text=course_name, font=("Arial", 32), fg="white", bg="black").place(x=280, y=120)

        def open_link():
            webbrowser.open(link)

        Button(window, text="Click Here", command=open_link, font=("Arial", 36), bg="green", fg="white").place(x=300, y=570)
        time.sleep(2)
        window.mainloop()

    except Exception as e:
        print(f"Error displaying pop-up: {e}")

try:
    csv_file = "EduCo.csv"
    background_path = "PopUpBG2.png"

    # Choose language: 'en', 'hi' (Hindi), 'kn' (Kannada)
    language = 'hi'

    edu_data = ExtractData(csv_file)

    if edu_data is not None:
        for _, row in edu_data.iterrows():
            ShowPopUp(row, background_path)
except Exception as e:
    print(f"An error occurred: {e}")

