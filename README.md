# AI Risk Dashboard & Disaster Response System

A powerful AI-driven platform for real-time disaster risk analysis, emergency communication, and situational awareness. This application leverages Google's Gemini AI and OpenWeatherMap to provide actionable insights based on environmental data.

## 🚀 Features

### 🌍 Real-time Risk Analysis
- **Environmental Monitoring**: Fetches live weather data (Temperature, Humidity, Rainfall, Wind Speed) using OpenWeatherMap API.
- **AI-Powered Assessment**: Uses **Google Gemini AI** to analyze weather conditions and calculate a risk score (0-100) and level (Low/Medium/High).
- ** actionable Recommendations**: Provides immediate, practical advice based on the assessed risk.
- **Geocoding**: Automatically determines the location name from coordinates.

### 💬 AI Disaster Assistant Chatbot
- **Expert Guidance**: A built-in chatbot acting as a disaster-response expert to answer user queries instantly.
- **Session Management**: chat sessions can be saved, retrieved, and managed via Google Cloud Storage.

### 📊 Interactive Dashboard
- **Visual Analytics**: View analyzed risk points on a map (heatmap support).
- **History & Reporting**: Access detailed reports of past analyses.

### ☁️ Cloud Integration
- **Google Cloud Storage**: Securely stores analysis reports and chat histories for future reference.

## 🛠️ Tech Stack

- **Backend**: Python, Flask
- **AI Engine**: Google Gemini API (Generative Language API)
- **Data Source**: OpenWeatherMap API
- **Storage**: Google Cloud Storage
- **Frontend**: HTML, CSS, JavaScript (Templates)

## 🔧 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/monishwar-reddy/ai-risk-dashboard.git
   cd ai-risk-dashboard
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Environment Variables:**
   Create a `.env` file or export the following variables (defaults are present in code but should be overridden for security):
   - `OPENWEATHER_KEY`: Your OpenWeatherMap API Key
   - `GEMINI_KEY`: Your Google Gemini API Key
   - `GOOGLE_APPLICATION_CREDENTIALS`: Path to your Service Account JSON file

4. **Run the Application:**
   ```bash
   python app.py
   ```
   The app will start at `http://localhost:8080`.

## 📂 Project Structure

```
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── service-account.json   # GCP Credentials (should be ignored in git)
├── static/                # Static assets (CSS, JS, Images)
├── templates/             # HTML Templates
└── README.md              # Project Documentation
```

## 🛡️ API Usage

- **Analyze Risk**: `POST /api/analyze`
  - Body: `{"location": "lat,lon"}`
- **Chat**: `POST /api/chat`
  - Body: `{"message": "user query"}`
- **Get Points**: `GET /api/points`

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements.

## 📄 License

This project is licensed under the MIT License.
