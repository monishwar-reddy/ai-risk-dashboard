# app.py
import os
import json
import uuid
import requests
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from google.cloud import storage
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)
# ---------------- Google Cloud Storage Setup ----------------
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service-account.json"

def upload_to_bucket(bucket_name, data, destination_blob_name):
    """Uploads a JSON object to the specified Cloud Storage bucket."""
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_string(
        json.dumps(data, indent=2),
        content_type='application/json'
    )
    print(f"✅ Uploaded report to gs://{bucket_name}/{destination_blob_name}")

# Ensure static files are served properly
@app.route('/static/<path:filename>')
def static_files(filename):
    return app.send_static_file(filename)

# CONFIG: set these as environment variables, do NOT hardcode keys in production
OPENWEATHER_KEY = os.getenv("OPENWEATHER_KEY")
GEMINI_KEY = os.getenv("GEMINI_KEY")
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={}".format(GEMINI_KEY)

# Geocoding function to get location name
def get_location_name(lat, lon):
    try:
        url = f"https://api.openweathermap.org/geo/1.0/reverse?lat={lat}&lon={lon}&limit=1&appid={OPENWEATHER_KEY}"
        r = requests.get(url, timeout=5)
        r.raise_for_status()
        data = r.json()
        if data:
            location = data[0]
            name = location.get('name', 'Unknown')
            country = location.get('country', '')
            state = location.get('state', '')
            return f"{name}, {state}, {country}" if state else f"{name}, {country}"
        return f"Location {lat:.3f}, {lon:.3f}"
    except Exception as e:
        print("Geocoding error:", e)
        return f"Location {lat:.3f}, {lon:.3f}"

# In-memory store for analyzed points (id, lat, lon, data, risk_report)
ANALYZED_POINTS = []

# Error handling wrapper
def handle_analysis_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Analysis error: {str(e)}")
            return {
                "error": True,
                "message": "Analysis failed. Please try again.",
                "risk_level": "Unknown",
                "risk_score": 0,
                "recommendation": "Unable to analyze due to technical issues."
            }
    return wrapper

# ---------------- Helpers ----------------
def get_live_weather(lat, lon):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={OPENWEATHER_KEY}"
        print(f"Fetching weather from: {url}")
        
        r = requests.get(url, timeout=10)
        print(f"Weather API status: {r.status_code}")
        
        if r.status_code == 401:
            print("Weather API key is invalid or expired")
            raise Exception("Weather API authentication failed")
        elif r.status_code == 404:
            print("Location not found in weather API")
            raise Exception("Location not found")
        
        r.raise_for_status()
        j = r.json()
        print(f"Raw weather response: {j}")
        
        # Validate required fields exist
        if "main" not in j:
            raise Exception("Invalid weather data structure - missing 'main' field")
            
        weather_data = {
            "temperature": round(j["main"]["temp"], 1),
            "humidity": round(j["main"]["humidity"], 1),
            "wind_speed": round(j.get("wind", {}).get("speed", 0), 1),
            "rainfall": round(j.get("rain", {}).get("1h", 0) if j.get("rain") else 0, 1)
        }
        print(f"Processed weather data: {weather_data}")
        return weather_data
        
    except requests.exceptions.Timeout:
        print("Weather API request timed out")
        raise Exception("Weather service timeout")
    except requests.exceptions.ConnectionError:
        print("Failed to connect to weather API")
        raise Exception("Weather service unavailable")
    except Exception as e:
        print(f"Weather fetch error: {e}")
        # Only return mock data if it's a network issue, not API key issues
        if "authentication" in str(e).lower() or "not found" in str(e).lower():
            raise e
        
        print("Using fallback weather data due to service issues")
        return {
            "temperature": 25.0,
            "humidity": 60.0,
            "wind_speed": 5.0,
            "rainfall": 0.0
        }

def call_gemini_risk(data):
    # Construct prompt asking Gemini to return JSON with numeric risk_score (0-100)
    prompt = f"""
You are an AI Disaster Risk Analyst. Analyze the following environmental conditions and return a JSON object EXACTLY like:
{{"risk_level":"Low|Medium|High", "risk_score": <0-100 integer>, "recommendation":"one-line advice"}}

Data:
Temperature: {data.get('temperature')} °C
Humidity: {data.get('humidity')} %
Rainfall: {data.get('rainfall')} mm
Wind Speed: {data.get('wind_speed')} m/s
"""
    body = {"contents": [{"parts": [{"text": prompt}]}]}
    try:
        print("Calling Gemini API...")
        resp = requests.post(GEMINI_URL, headers={"Content-Type":"application/json"}, json=body, timeout=12)
        print(f"Gemini API status: {resp.status_code}")
        resp.raise_for_status()
        js = resp.json()
        print(f"Gemini response: {js}")
        if "candidates" in js and js["candidates"]:
            text = js["candidates"][0]["content"]["parts"][0]["text"]
            # try parse JSON from text
            try:
                parsed = json.loads(text.strip().replace("```json", "").replace("```", ""))
                # ensure numeric risk_score
                parsed["risk_score"] = int(parsed.get("risk_score")) if str(parsed.get("risk_score")).isdigit() else int(float(parsed.get("risk_score") or 0))
                return parsed
            except Exception:
                # fallback: basic extraction
                # attempt to find words
                tl = text.lower()
                level = "Medium"
                if "high" in tl: level = "High"
                elif "low" in tl: level = "Low"
                # attempt to find a number
                import re
                m = re.search(r"(\d{1,3})", text)
                score = int(m.group(1)) if m else 50
                return {"risk_level": level, "risk_score": score, "recommendation": text.strip()}
        else:
            return {"risk_level":"Unknown","risk_score":0,"recommendation":"No response from AI"}
    except Exception as e:
        print(f"Gemini error: {e}")
        # Fallback risk assessment based on weather data
        temp = data.get('temperature', 0)
        humidity = data.get('humidity', 0)
        rainfall = data.get('rainfall', 0)
        wind = data.get('wind_speed', 0)
        
        # Simple risk calculation
        risk_score = 0
        if temp > 35 or temp < 5:
            risk_score += 30
        elif temp > 30 or temp < 10:
            risk_score += 15
            
        if humidity > 80:
            risk_score += 20
        elif humidity < 20:
            risk_score += 15
            
        if rainfall > 10:
            risk_score += 25
        elif rainfall > 5:
            risk_score += 10
            
        if wind > 15:
            risk_score += 20
        elif wind > 10:
            risk_score += 10
            
        risk_score = min(risk_score, 100)
        
        if risk_score >= 60:
            level = "High"
            rec = "Take immediate precautions and monitor conditions closely"
        elif risk_score >= 30:
            level = "Medium" 
            rec = "Stay alert and be prepared for changing conditions"
        else:
            level = "Low"
            rec = "Conditions are generally safe, continue normal activities"
            
        return {"risk_level": level, "risk_score": risk_score, "recommendation": rec}

# ---------------- Routes ----------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/menu")
def menu():
    return render_template("menu.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/chat")
def chat_page():
    return render_template("chat.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

# API: analyze a clicked location (lat,lon string)
@app.route("/api/analyze", methods=["POST"])
def analyze():
    try:
        payload = request.get_json() or {}
        print(f"Received analyze request: {payload}")
        
        loc = payload.get("location", "")
        if not loc:
            return jsonify({"error": "Missing location parameter"}), 400
            
        try:
            lat_str, lon_str = loc.split(",")
            lat, lon = float(lat_str.strip()), float(lon_str.strip())
            print(f"Parsed coordinates: lat={lat}, lon={lon}")
        except Exception as e:
            print(f"Location parsing error: {e}")
            return jsonify({"error": "Invalid location format. Use 'lat,lon'."}), 400

        # Validate coordinates
        if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
            return jsonify({"error": "Invalid coordinates. Latitude must be -90 to 90, longitude -180 to 180."}), 400

        print("Fetching weather data...")
        weather = get_live_weather(lat, lon)
        print(f"Weather data received: {weather}")
        
        print("Getting risk analysis...")
        risk = call_gemini_risk(weather)
        print(f"Risk analysis received: {risk}")

        print("Getting location name...")
        location_name = get_location_name(lat, lon)
        print(f"Location name: {location_name}")
        
        point = {
            "id": str(uuid.uuid4()),
            "lat": lat,
            "lon": lon,
            "location_name": location_name,
            "data": weather,
            "risk_report": risk
        }
        ANALYZED_POINTS.append(point)
        
        response_data = {
            "id": str(uuid.uuid4()),
            "location": f"{lat},{lon}",
            "location_name": location_name,
            "data": weather,
            "risk_report": risk
        }

# Upload the report to Cloud Storage
        upload_to_bucket("ai-disaster-user-data", response_data, f"reports/{response_data['id']}.json")

        print(f"✅ Report stored and sent: {response_data}")
        return jsonify(response_data)
        
    except Exception as e:
        print(f"Unexpected error in analyze endpoint: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

# Return all points (for heatmap)
@app.route("/api/points", methods=["GET"])
def get_points():
    return jsonify(ANALYZED_POINTS)

# Chat endpoint — free form via Gemini
@app.route("/api/chat", methods=["POST"])
def api_chat():
    payload = request.get_json() or {}
    message = payload.get("message", "")
    if not message:
        return jsonify({"error":"Empty message"}), 400
    prompt = f"You are an expert disaster-response assistant. Answer briefly: {message}"
    body = {"contents":[{"parts":[{"text":prompt}]}]}
    try:
        resp = requests.post(GEMINI_URL, headers={"Content-Type":"application/json"}, json=body, timeout=12)
        resp.raise_for_status()
        js = resp.json()
        if "candidates" in js and js["candidates"]:
            text = js["candidates"][0]["content"]["parts"][0]["text"]
            return jsonify({"reply": text})
        return jsonify({"reply": "No reply from AI"})
    except Exception as e:
        print("Chat error:", e)
        return jsonify({"reply":"AI error"}), 500

# Explain endpoint — explain a point by id with Gemini
@app.route("/api/explain", methods=["POST"])
def api_explain():
    payload = request.get_json() or {}
    pid = payload.get("id")
    point = next((p for p in ANALYZED_POINTS if p["id"] == pid), None)
    if not point:
        return jsonify({"error":"Point not found"}), 404
    prompt = f"""You are an interpreter. Given this data: {json.dumps(point['data'])}
And the AI risk report: {json.dumps(point['risk_report'])}
Explain in 2-3 sentences WHY that risk level was assigned and give 2 practical actions for the local community."""
    body = {"contents":[{"parts":[{"text":prompt}]}]}
    try:
        resp = requests.post(GEMINI_URL, headers={"Content-Type":"application/json"}, json=body, timeout=12)
        resp.raise_for_status()
        js = resp.json()
        if "candidates" in js and js["candidates"]:
            text = js["candidates"][0]["content"]["parts"][0]["text"]
            return jsonify({"explanation": text})
        return jsonify({"explanation":"No explanation from AI"})
    except Exception as e:
        print("Explain error:", e)
        return jsonify({"explanation":"AI error"}), 500
    # ---------------- Chat Session Management ----------------

@app.route("/api/chat/save", methods=["POST"])
def save_chat():
    """Save chat session to Google Cloud Storage."""
    try:
        payload = request.get_json() or {}
        user_id = payload.get("user_id", str(uuid.uuid4()))
        messages = payload.get("messages", [])
        
        if not messages:
            return jsonify({"error": "No chat messages provided"}), 400

        chat_data = {
            "user_id": user_id,
            "timestamp": uuid.uuid4().hex,
            "messages": messages
        }

        upload_to_bucket("ai-disaster-user-data", chat_data, f"chats/{user_id}_{chat_data['timestamp']}.json")
        return jsonify({"message": "Chat saved successfully", "chat_id": f"{user_id}_{chat_data['timestamp']}"})
    except Exception as e:
        print("Save chat error:", e)
        return jsonify({"error": str(e)}), 500


@app.route("/api/chat/download/<chat_id>", methods=["GET"])
def download_chat(chat_id):
    """Download chat session from Google Cloud Storage."""
    try:
        client = storage.Client()
        bucket = client.bucket("ai-disaster-user-data")
        blob = bucket.blob(f"chats/{chat_id}.json")

        if not blob.exists():
            return jsonify({"error": "Chat not found"}), 404

        chat_data = blob.download_as_text()
        return jsonify(json.loads(chat_data))
    except Exception as e:
        print("Download chat error:", e)
        return jsonify({"error": str(e)}), 500


@app.route("/api/chat/delete/<chat_id>", methods=["DELETE"])
def delete_chat(chat_id):
    """Delete chat session from Google Cloud Storage."""
    try:
        client = storage.Client()
        bucket = client.bucket("ai-disaster-user-data")
        blob = bucket.blob(f"chats/{chat_id}.json")

        if not blob.exists():
            return jsonify({"error": "Chat not found"}), 404

        blob.delete()
        return jsonify({"message": f"Chat {chat_id} deleted successfully"})
    except Exception as e:
        print("Delete chat error:", e)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print("Starting app on http://127.0.0.1:8080")
    app.run(debug=True, host="0.0.0.0", port=8080)
