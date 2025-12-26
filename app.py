import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv

# 1. .env file se API key load karne ke liye
load_dotenv()

app = Flask(__name__)

# 2. API Key ko environment variable se uthana
API_KEY = os.getenv("GEMINI_API_KEY")

# 3. Gemini Setup
try:
    if not API_KEY:
        print("❌ Error: .env file mein GEMINI_API_KEY nahi mili!")
    else:
        genai.configure(api_key=API_KEY)
        
        # Check karna ki kaunsa model available hai (Auto-select)
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        if 'models/gemini-1.5-flash' in available_models:
            model_name = 'gemini-1.5-flash'
        elif 'models/gemini-pro' in available_models:
            model_name = 'gemini-pro'
        else:
            model_name = available_models[0]
            
        model = genai.GenerativeModel(model_name)
        print(f"✅ AI Connected using: {model_name}")

except Exception as e:
    print(f"❌ Setup Error: {e}")
    model = None

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    if not model:
        return jsonify({"reply": "AI setup sahi se nahi hua hai. .env file check karein."})

    try:
        data = request.get_json()
        user_msg = data.get("message")

        if not user_msg:
            return jsonify({"reply": "Bhai, kuch toh likho!"})

        # AI se response mangna
        response = model.generate_content(user_msg)
        return jsonify({"reply": response.text})

    except Exception as e:
        print(f"❌ Chat Error: {e}")
        return jsonify({"reply": f"Error: {str(e)}"})

if __name__ == "__main__":
    # Deployment ke liye zaroori configuration
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)