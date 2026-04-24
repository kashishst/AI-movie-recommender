from flask import Flask, request, jsonify
from flask_cors import CORS
from model import predict_movies, load_artifacts

app = Flask(__name__)
# Enable CORS to allow our React frontend to talk to this backend!
CORS(app)

# Pre-load the AI model when the server starts uppyth so API calls are instantaneous
load_artifacts()

@app.route("/recommend", methods=["POST"])
def recommend():
    try:
        # 1. The frontend will send data in JSON format
        data = request.get_json()
        
        # 2. Extract values sent from React
        genre = data.get("genre", "")
        mood = data.get("mood", "")
        type = data.get("type", "")
        
        if not genre and not mood and not type:
            return jsonify({"error": "Please provide genre, mood, or type"}), 400
            
        # 3. Call our AI model located in model.py
        result = predict_movies(genre, mood, type)
        
        if "error" in result:
            return jsonify(result), 500
            
        # 4. Return recommendations to the browser
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Start the web server
    print("Starting API Server on http://127.0.0.1:5000...")
    app.run(debug=True, port=5000)
