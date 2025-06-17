# ArtJam = "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"
import tkinter as tk
from tkinter import Label, Button
import requests
import openai
from tkinter import PhotoImage
import pyperclip  # Biblioteka do kopiowania do schowka

# Funkcja do generowania obrazu
def generate_comic():
    prompt = "A cute baby sea otter"  # Przykładowy prompt, możesz go zmienić

    # Przygotowanie zapytania API do OpenAI (z użyciem requests)
    url = "https://api.openai.com/v1/images/generations"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai.api_key}"
    }
    data = {
        "model": "dall-e-3",
        "prompt": prompt,
        "n": 1,
        "size": "1024x1024"
    }

    # Wysyłamy zapytanie POST
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        # Odbieramy odpowiedź z URL do obrazu
        image_url = response.json()['data'][0]['url']

        # Wyświetlenie linku jako klikalnego
        url_label.config(text="Twoje zdjęcie 📷🖼️", fg="blue", cursor="hand2")

        # Umożliwienie kopiowania linku do schowka
        url_label.bind("<Button-1>", lambda e: pyperclip.copy(image_url))  # Kliknięcie kopiuje URL do schowka
    else:
        # Obsługa błędów
        url_label.config(text="Błąd podczas generowania obrazu")


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

# Przycisk do generowania komiksu
button = Button(root, text="Twórz w 3...2...1...!", command=generate_comic)
button.pack()

# Label do wyświetlania linku z wygenerowanym obrazem
url_label = Label(root, text="", fg="blue")
url_label.pack()

# Label do wyświetlania pobranego obrazu
image_label = Label(root)
image_label.pack()

# Uruchomienie aplikacji
root.mainloop()
