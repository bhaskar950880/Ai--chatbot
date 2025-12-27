import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
API_KEY = os.getenv("GEMINI_API_KEY")

# --- MODEL SELECTION LOGIC ---
model = None
try:
    genai.configure(api_key=API_KEY)
    
    # Available models ki list nikalna
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    print(f"Available Models: {available_models}")

    # Sabse pehle 'gemini-1.5-flash' try karo, phir 'gemini-1.5-pro', phir jo bhi mile
    if any("gemini-1.5-flash" in m for m in available_models):
        model_name = "gemini-1.5-flash"
    elif any("gemini-1.5-pro" in m for m in available_models):
        model_name = "gemini-1.5-pro"
    else:
        # Agar upar waale nahi mile toh jo pehla model hai wahi le lo
        model_name = available_models[0].split('/')[-1]

    model = genai.GenerativeModel(model_name)
    print(f"✅ AI Connected using model: {model_name}")

except Exception as e:
    print(f"❌ Setup Error: {e}")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_msg = data.get("message")

        if not model:
            return jsonify({"reply": "AI setup sahi se nahi hua. Console check karein."})

        # AI se response mangna
        response = model.generate_content(user_msg)
        return jsonify({"reply": response.text})

    except Exception as e:
        print(f"❌ Chat Error: {e}")
        return jsonify({"reply": f"Error: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)