import tkinter as tk
from tkinter import Label, Button
import requests
import openai
from tkinter import PhotoImage
from PIL import Image, ImageTk  # Biblioteka do obsługi obrazów
import pyperclip  # Biblioteka do kopiowania do schowka
from io import BytesIO  # Do przetwarzania obrazów w pamięci


# Funkcja do generowania obrazu
def generate_comic():
    # Pobranie tekstu z pola tekstowego i dodanie stałego fragmentu
    user_prompt = prompt_entry.get()
    prompt = f"{user_prompt} in a comic book style with bold black outlines, vibrant colors, and simplified features, resembling a hand-drawn cartoon with exaggerated expressions and dynamic movement, surrounded by a 2px margin and a 3px white border with a black outline around the image."

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

        # Pobieranie obrazu z URL
        image_response = requests.get(image_url)
        img_data = image_response.content
        img = Image.open(BytesIO(img_data))
        img = img.resize((300, 300))  # Możesz dostosować rozmiar obrazu

        # Konwertowanie obrazu na format Tkinter
        img_tk = ImageTk.PhotoImage(img)

        # Wyświetlenie obrazu
        image_label.config(image=img_tk)
        image_label.image = img_tk  # Przypisanie, aby nie zniknął z pamięci

        # Wyświetlenie tekstu informującego o generowaniu obrazu
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

# Pole tekstowe do wpisania promptu
prompt_entry = tk.Entry(root, width=30)
prompt_entry.pack()

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
