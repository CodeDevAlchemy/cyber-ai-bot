from flask import Flask, request, jsonify, render_template
import os
from dotenv import load_dotenv
from google import genai
from datetime import datetime

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Get API key safely
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables.")

# Initialize Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({"reply": "⚠ Please enter a message."})

        user_lower = user_message.lower()

        # 🔥 Real-time Date & Time Handling
        if any(keyword in user_lower for keyword in ["date", "time", "current date", "current time"]):
            now = datetime.utcnow()
            formatted_time = now.strftime("%A, %B %d, %Y at %I:%M %p UTC")
            return jsonify({
                "reply": f"The current date and time is {formatted_time}."
            })

        # 🔥 Gemini AI Response
        response = client.models.generate_content(
            model="models/gemini-flash-latest",
            contents=user_message
        )

        return jsonify({"reply": response.text})

    except Exception as e:
        print("ERROR:", e)  # Logs visible in Render dashboard
        return jsonify({
            "reply": "⚠ HelixAI encountered an error generating response."
        })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)