from flask import Flask, request, jsonify, render_template
import os
from dotenv import load_dotenv
from google import genai
from datetime import datetime

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Get Gemini API key
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
        mode = data.get("mode", "analyst")

        if not user_message:
            return jsonify({"reply": "⚠ Please enter a message."})

        user_lower = user_message.lower()

        # -------------------------
        # 1️⃣ Greeting Detection
        # -------------------------
        greetings = ["hi", "hello", "hey", "yo", "what's up", "whats up"]
        if user_lower in greetings:
            return jsonify({
                "reply": (
                    "Hey there 👋 I’m **HelixAI**.\n\n"
                    "Switch between **Analyst Mode** and **Defender Mode** "
                    "and ask me about any cybersecurity threat."
                )
            })

        # -------------------------
        # 2️⃣ Real-Time Date & Time
        # -------------------------
        if any(keyword in user_lower for keyword in ["date", "time", "current date", "current time"]):
            now = datetime.utcnow()
            formatted_time = now.strftime("%A, %B %d, %Y at %I:%M %p UTC")
            return jsonify({
                "reply": f"The current date and time is **{formatted_time}**."
            })

        # -------------------------
        # 3️⃣ Mode-Based Prompt Logic
        # -------------------------
        if mode == "analyst":
            system_prompt = (
                "You are HelixAI operating in Analyst Mode.\n"
                "If the topic is cybersecurity related, respond with structured analysis.\n"
                "If not related to cybersecurity, respond casually.\n\n"
                "For cybersecurity topics, structure response as:\n"
                "• Overview\n"
                "• How It Works (Conceptual)\n"
                "• Impact\n"
                "• Risk Level\n"
                "Keep response professional but concise."
            )
        else:
            system_prompt = (
                "You are HelixAI operating in Defender Mode.\n"
                "If the topic is cybersecurity related, focus on defense strategies.\n"
                "If unrelated to cybersecurity, respond casually.\n\n"
                "For cybersecurity topics, structure response as:\n"
                "• Threat Summary\n"
                "• Prevention Methods\n"
                "• Detection Techniques\n"
                "• Mitigation Steps\n"
                "Keep response professional but clear."
            )

        # -------------------------
        # 4️⃣ Gemini API Call
        # -------------------------
        response = client.models.generate_content(
            model="models/gemini-flash-latest",
            contents=system_prompt + "\n\nUser Question: " + user_message
        )

        return jsonify({"reply": response.text})

    except Exception as e:
        print("ERROR:", e)
        return jsonify({
            "reply": "⚠ HelixAI encountered an error generating response."
        })


# -------------------------
# Run App (Render Compatible)
# -------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)