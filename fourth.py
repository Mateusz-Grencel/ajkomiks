from flask import Flask, render_template, request, redirect, url_for, session, flash, get_flashed_messages
import requests

SectionPrompts = {
    "artjam": "{user_prompt} in a comic book style with bold black outlines, using only the following colors: #d74d62 (rose), #63bfac (turquoise), and white, with simplified features, resembling a hand-drawn cartoon with exaggerated expressions and dynamic movement, surrounded by a 2px margin and a 3px white border with a black outline around the image.",
    "cdv": "{user_prompt} in a comic book style with bold black outlines, using only the following colors: #facb2c (yellow), #04b3db (light blue), and #044c64 (dark blue), with simplified features, resembling a hand-drawn cartoon with exaggerated expressions and dynamic movement, surrounded by a 2px margin and a 3px white border with a black outline around the image.",
    "blackwhite": "{user_prompt} in a comic book style with bold black outlines, simplified features, and exaggerated expressions, using only black and white colors, resembling a hand-drawn cartoon with dynamic movement, surrounded by a 2px margin and a 3px white border with a black outline around the image.",
    "random": "{user_prompt} in a comic book style with bold black outlines, vibrant and randomly chosen colors, simplified features, resembling a hand-drawn cartoon with exaggerated expressions and dynamic movement, surrounded by a 2px margin and a 3px white border with a black outline around the image.",
    "normal": "{user_prompt} in a comic book style with bold black outlines, natural and realistic colors, simplified features, resembling a hand-drawn cartoon with exaggerated expressions and dynamic movement, surrounded by a 2px margin and a 3px white border with a black outline around the image."
}

app = Flask(__name__)

# randomowy klucz sesji
app.secret_key = "comic"

@app.route("/save-key", methods=["POST"])
def save_key():
    user_key = request.form.get("userOpenAIKey")
    if user_key:
        session["userOpenAIKey"] = user_key
        flash("Klucz API został pomyślnie zapisany.")
    else:
        flash("Nie wpisano klucza API.")
    return redirect(url_for('hello'))

@app.route("/generate-comic/<section>", methods=["POST"])
def generate_comic(section):
    user_prompt = request.form.get("user_prompt")
    openai_key = session.get("userOpenAIKey")
    if not openai_key:
        flash("Brak klucza API OpenAI. Proszę najpierw wpisać klucz.")
        return redirect(url_for("hello"))

    base_prompt = SectionPrompts.get(section)
    if not base_prompt:
        flash("Nieznana sekcja.")
        return redirect(url_for("hello"))

    full_prompt = f"{user_prompt} {base_prompt}"

    url = "https://api.openai.com/v1/images/generations"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_key}"  # openai_key z sesji
    }
    data = {
        "model": "dall-e-3",
        "prompt": full_prompt,
        "n": 1,
        "size": "1024x1024"
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # rzuci wyjątek jeśli status != 200

        json_data = response.json()
        comic_url = json_data["data"][0]["url"]  # URL wygenerowanego obrazka

    except requests.exceptions.RequestException as e:
        flash(f"Błąd podczas generowania obrazka: {e}")
        return redirect(url_for("hello"))

    # Przekaż wygenerowany obrazek i aktualną sekcję do szablonu
    return render_template("layout.html", comic_url=comic_url, active_section=section)

@app.route("/", methods=["GET"])
def hello():
    messages = get_flashed_messages()
    return render_template(
        "layout.html",
        messages=messages,
        comic_url=None,
        active_section=None
    )

if __name__ == "__main__":
    app.run(debug=True)



