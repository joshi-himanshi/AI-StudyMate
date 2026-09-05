from flask import Flask, render_template, request
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():

    topic = request.form["topic"]
    difficulty = request.form["difficulty"]

    prompt = f"""
    Create study material for the topic: {topic}.

    Difficulty level: {difficulty}.

    Explain the topic in simple language.
    Include:
    1. A short introduction
    2. Important concepts
    3. Examples
    4. Key points to remember
    """

    response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=prompt,
    config=types.GenerateContentConfig(
        max_output_tokens=1000
    )
)

    study_material = response.text

    return render_template(
        "result.html",  
        topic=topic,
        difficulty=difficulty,
        study_material=study_material
    )


if __name__ == "__main__":
    app.run(debug=True)