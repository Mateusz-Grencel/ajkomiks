from dotenv import load_dotenv
import os
import tkinter as tk
from tkinter import Label, Button
from tkinter import PhotoImage
import re

load_dotenv()

openai_apikey = os.getenv("openai.api_key")
color_scheme = "default"

def set_color_scheme(scheme):
    global color_scheme
    color_scheme = scheme

# Tworzenie głównego okna
root = tk.Tk()
root.title("Generator komiksów ArtJam")

# Dodanie logo (jeśli posiadasz w formacie PNG)
logo = PhotoImage(file="C:/Users/mateu/OneDrive/Pulpit/artjamlogo.png")  # Zakładając, że masz logo w formacie PNG
logo_label = Label(root, image=logo)
logo_label.pack()

# Tytuł
title = Label(root, text="Generator komiksów ArtJam", font=("Arial", 16))
title.pack()

# Pole tekstowe do wpisania promptu
prompt_entry = tk.Entry(root, width=30)
prompt_entry.pack()

# Przycisk do generowania komiksu czarno-białego
button = Button(root, text="Czarno-biały", command=lambda: set_color_scheme("black_white"))
button.pack()

# Przycisk do generowania komiksu z kolorami cdv
button = Button(root, text="Kolory CDV", command=lambda: set_color_scheme("cdv_colors"))
button.pack()

# Przycisk do generowania komiksu z kolorami aj
# #dd4464 - malinowy róż
# #5dbdac - miętowa zieleń
button = Button(root, text="Kolory ArtJamers", command=lambda: set_color_scheme("aj_colors"))
button.pack()

# Przycisk do generowania komiksu z losowymi kolorami
button = Button(root, text="Losowe kolory", command=lambda: set_color_scheme("random_colors"))
button.pack()

users_colors = Label(root, text="Wpisz wybrane kolory po ,:", font=("Arial", 16))
users_colors.pack()

users_colors_entry = tk.Entry(root, width=30)
users_colors_entry.pack()

# Przycisk do generowania komiksu z narzuconymi kolorami
button = Button(root, text="Narzucone kolory", command=lambda: set_color_scheme("preset"))
button.pack()

# Label do wyświetlania linku z wygenerowanym obrazem
url_label = Label(root, text="", fg="blue")
url_label.pack()

# Label do wyświetlania pobranego obrazu
image_label = Label(root)
image_label.pack()

# Uruchomienie aplikacji
root.mainloop()
