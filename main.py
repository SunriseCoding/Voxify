from AdityaSR import speechRecognition as sr
import AdityaSR
import asyncio
from argostranslate import translate
import argosModelInstaller as guard
import os, time
from PIL import Image, ImageTk
import tkinter as tk

def english_to_asl_gloss(text: str) -> str:
    text = text.lower().strip()
    replacements = {
        " i am ": " I ",
        " you are ": " YOU ",
        " he is ": " HE ",
        " she is ": " SHE ",
        " they are ": " THEY ",
        " we are ": " WE ",
        " going to ": " GO ",
        " want to ": " WANT ",
        " have ": " HAVE ",
        " has ": " HAVE ",
        " the ": "",
        " a ": "",
        " an ": "",
        " is ": "",
        " am ": "",
        " are ": "",
        " to ": "",
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    words = [w.upper() for w in text.split() if w]
    return " ".join(words)

def show_asl_signs(gloss_text: str, folder: str = "asl_signs", delay: float = 0.2):
    words = gloss_text.split()
    root = tk.Tk()
    root.configure(bg="white")
    label = tk.Label(root, bg="white")
    label.pack()
    for word in words:
        for i in range(0, len(word)):
            file_path = None
            for ext in (".png", ".jpg", ".gif", ".jpeg"):
                candidate = os.path.join(folder, f"{word[i].lower()}{ext}")
                if os.path.exists(candidate):
                    file_path = candidate
                    break
            if file_path:
                img = Image.open(file_path)
                img = Image.open(file_path).convert("RGBA")
                bg = Image.new("RGBA", img.size, (255, 255, 255, 255))
                combined = Image.alpha_composite(bg, img)
                tk_img = ImageTk.PhotoImage(combined)
                label.config(image=tk_img)
                root.update()
                time.sleep(delay)
            else:
                print(f"(No sign for {word[i]})")
    root.destroy()

def translate_to_asl(text: str, display=True, folder="asl_signs"):
    gloss = english_to_asl_gloss(text)
    print("ASL Gloss:", gloss)
    if display:
        show_asl_signs(gloss, folder)
    return gloss

AdityaSR.loadModel("large")

async def sMain():
    result = await sr(2, True)
    text = result["text"].strip()
    language = result["language"].strip()
    if language != "en":
        if guard.checkModel(language, "en") == True:
            text = translate.translate(text, language, 'en')
        else:
            print("An error occurred")
    print(text)
    translate_to_asl(text)

async def main():
    while True:
        await sMain()

asyncio.run(main())
