# 🌍 AI Environment Dashboard

AI Environment Dashboard is a smart, serverless web app that visualizes **real-time environmental data** such as temperature, humidity, and air quality.  
It uses **Flask** and **Google Cloud Run**, with AI-powered logic through **Google AI Studio (Gemini API)**.

---

## 🧠 Features
- Displays **real-time weather and environmental conditions**
- Integrates **public APIs** like OpenWeatherMap and USGS Earthquake API
- Provides **AI-based contextual insights** using Google AI Studio
- Deployed seamlessly on **Google Cloud Run**

---

## 🧩 Technologies Used
- **Frontend:** HTML, CSS, JavaScript  
- **Backend:** Python (Flask)  
- **APIs:** OpenWeatherMap API, USGS Earthquake API  
- **AI Layer:** Google AI Studio (Gemini Prompt API)  
- **Hosting:** Google Cloud Run  

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository  
Run the following commands in your terminal:  
git clone https://github.com/<your-username>/ai-environment-dashboard.git  
cd ai-environment-dashboard  

### 2️⃣ Install Dependencies  
Use pip to install the required packages:  
pip install -r requirements.txt  

### 3️⃣ Run Locally  
Start the Flask server with:  
python app.py  

Visit **http://127.0.0.1:5000** in your browser or as shown in your terminal output.

---

## 🌐 Deploying to Google Cloud Run  

1. Go to **Google Cloud Console → Cloud Run**  
2. Connect this **GitHub repository**  
3. Set **Environment Variables** for your API keys  
4. Deploy the app — you’ll get a public URL like:  
   https://ai-dashboard-xxxx.a.run.app  

---

## 🔐 API Keys & Security  

⚠️ **Important Notice:**  
The API keys included in this repository are sample placeholders only.  
Replace them with your own valid keys before deployment.  
Use `.env` files (added to `.gitignore`) or Cloud Run environment variables instead.  

**Example `.env` file:**  
OPENWEATHERMAP_API_KEY=your_real_key_here  
AI_STUDIO_API_KEY=your_real_key_here  

---

## 📜 License  
This project is open-source and created for educational and hackathon purposes only.  
Licensed under the **MIT License**.

---

## ✨ Author  
**Vardireddy Monishwar Reddy**  
📧 monishwar26413@gmail.com  

---

## 🤝 Contributions  
Feel free to contribute via pull requests or by emailing suggestions and improvements.
