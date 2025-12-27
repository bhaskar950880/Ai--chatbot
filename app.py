import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv

# .env file load karna
load_dotenv()

app = Flask(__name__)

# API Key load karna
API_KEY = os.getenv("GEMINI_API_KEY")

# --- MODEL SETUP (Bina date ke, sirf connection) ---
model = None
try:
    if not API_KEY:
        print("❌ Error: API Key nahi mili!")
    else:
        genai.configure(api_key=API_KEY)
        
        # 404 Error se bachne ke liye hum available model auto-detect kar rahe hain
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        if available_models:
            # Jo model aapke account mein chalta hai wahi pick hoga (e.g., gemini-1.5-flash)
            active_model = available_models[0]
            model = genai.GenerativeModel(active_model)
            print(f"✅ AI Connected using: {active_model}")
        else:
            print("❌ No models found!")
except Exception as e:
    print(f"❌ Setup Error: {e}")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    if not model:
        return jsonify({"reply": "AI Setup error. Check Console."})

    try:
        data = request.get_json()
        user_msg = data.get("message")

        # Puraana simple tarika: No Date, No Instructions
        response = model.generate_content(user_msg)
        
        return jsonify({"reply": response.text})

    except Exception as e:
        print(f"❌ Chat Error: {e}")
        return jsonify({"reply": "Kuch error aa gaya hai, terminal check karein!"})

if __name__ == "__main__":
    app.run(debug=True)