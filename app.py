import os
from flask import Flask, render_template, request, Response # <--- 'Response' add kiya streaming ke liye
import google.generativeai as genai
from dotenv import load_dotenv

# .env file load karna
load_dotenv()

app = Flask(__name__)

# API Key load karna
API_KEY = os.getenv("GEMINI_API_KEY")

# Gemini Setup
try:
    genai.configure(api_key=API_KEY)
    # Fast model 'gemini-1.5-flash' use kar rahe hain
    model = genai.GenerativeModel("gemini-1.5-flash")
    print("✅ AI Connected for Streaming!")
except Exception as e:
    print(f"❌ Setup Error: {e}")
    model = None

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_msg = data.get("message")

    if not model:
        return "AI Setup Error!", 500

    # --- YAHA SE STREAMING LOGIC SHURU HAI ---
    def generate():
        try:
            # stream=True karne se AI ek-ek chunk (tukda) bhejta hai
            response = model.generate_content(user_msg, stream=True)
            
            for chunk in response:
                if chunk.text:
                    # 'yield' ka matlab hai ki pura answer soche bina, 
                    # jitna milta jaye utna browser ko turant bhej do
                    yield chunk.text 
        except Exception as e:
            yield f"Error: {str(e)}"

    # Hum 'Response' bhej rahe hain 'text/plain' format mein
    # Taaki browser ise ek continuous stream ki tarah receive kare
    return Response(generate(), mimetype='text/plain')
    # --- STREAMING LOGIC KHATAM ---

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)