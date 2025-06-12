from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import openai
import os

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

# OpenAI API key (تأكد إنها مضافة في Replit Secrets باسم 'key')
openai.api_key = os.environ['key']

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/ai-review', methods=['POST'])
def ai_review():
    try:
        description = request.form.get('description')
        agree = request.form.get('agreeAI', '').lower() in ['true', '1', 'yes']

        print("Form Data Received:", request.form)

        if not agree:
            return jsonify({"error": "User did not agree to AI processing."}), 400

        prompt = f"You are a real estate expert. Improve this property description in Arabic for better marketing: {description}"
        
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        improved_description = response.choices[0].message['content'].strip()

        # Placeholder image URLs
        enhanced_image_urls = [
            "https://via.placeholder.com/100?text=Enhanced+1",
            "https://via.placeholder.com/100?text=Enhanced+2"
        ]

        return jsonify({
            "description": improved_description,
            "image_urls": enhanced_image_urls
        })

    except Exception as e:
        print("Error in /ai-review:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
