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

def SpeakText(job_details, language):
    try:
        click_here_text = TranslateText("Click Here", language)
        full_text = f"{job_details} {click_here_text}"
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
def ShowPopUp(job_row, background_path):
    try:
        job_title = job_row['Job Title']
        job_location = job_row['Job Location']
        salary = job_row['Salary']
        link = job_row['Link']

        if language != 'en':
            job_title = TranslateText(job_title, language)
            job_location = TranslateText(job_location, language)
            salary = TranslateText(salary, language)

        job_details = f"Job Title: {job_title}. Location: {job_location}. Salary: {salary}."
        threading.Thread(target=SpeakText, args=(job_details, language)).start()

        window = Tk()
        window.title("Job Notification")
        window.geometry("800x800")

        background = Image.open(background_path)
        background = background.resize((800, 800), Image.Resampling.LANCZOS)
        bg_image = ImageTk.PhotoImage(background)

        bg_label = Label(window, image=bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        Label(window, text=job_title, font=("Eras Bold ITC", 36), bg="white").place(x=250, y=140)
        Label(window, text=job_location, font=("Eras Bold ITC", 36), bg="white").place(x=300, y=430)
        Label(window, text=salary, font=("Eras Bold ITC", 56), fg="green", bg="white").place(x=290, y=45)

        def open_link():
            webbrowser.open(link)

        Button(window, text="Click Here", command=open_link, font=("Arial", 36), bg="green", fg="white").place(x=300, y=500)
        time.sleep(2)
        window.mainloop()

    except Exception as e:
        print(f"Error displaying pop-up: {e}")

try:
    csv_file = "JobOp.csv"
    background_path = "PopUpBG.png"

    # Choose language: 'en', 'hi' (Hindi), 'kn' (Kannada)
    language = 'kn'

    job_data = ExtractData(csv_file)

    if job_data is not None:
        for _, row in job_data.iterrows():
            ShowPopUp(row, background_path)
except Exception as e:
    print(f"An error occurred: {e}")
