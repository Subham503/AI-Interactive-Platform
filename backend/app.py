from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import os
from openai import OpenAI

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def home():
    return jsonify({"message": "AI Backend is running 🚀"})

@app.route("/generate_plan", methods=["POST"])
def generate_plan():
    data = request.json

    subject = data.get("subject")
    weak_areas = data.get("weak_areas")
    hours = data.get("hours")

    prompt = f"""
    You are an AI study assistant.
    Create a concise study plan for a student.

    Subject: {subject}
    Weak Areas: {weak_areas}
    Available Time: {hours} hours

    Give:
    - A step-by-step study plan
    - Practical tips
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    ai_reply = response.choices[0].message.content

    return jsonify({"plan": ai_reply})

if __name__ == "__main__":
    app.run(debug=True)
