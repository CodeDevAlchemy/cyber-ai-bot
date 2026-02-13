from flask import Flask, request, jsonify, render_template
import os
from dotenv import load_dotenv
from google import genai

print("Current working directory:", os.getcwd())
print("Files in this directory:", os.listdir())

load_dotenv() 
print("API KEY:", os.getenv("GEMINI_API_KEY"))

app = Flask(__name__)

# Create client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")

    system_prompt = """
    You are a Cybersecurity AI Assistant.
    Explain topics clearly and technically.
    If user asks about hacking, explain ethical use and prevention.
    Be professional but friendly.
    """
    try:
        response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=user_message,
)

        return jsonify({"reply": response.text})

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"reply": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

