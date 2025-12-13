# 🌍 AI Environment Dashboard
**AI-Powered Global Environmental Intelligence for Mobility & Safety**

AI Environment Dashboard is a smart, serverless web application that provides **real-time environmental risk intelligence** to support **global mobility, international travel, and cross-border decision-making**.

The platform aggregates real-time environmental data and uses **Gemini AI** to deliver **contextual insights** that help travelers, remote workers, international teams, and organizations make safer location-based decisions worldwide.

🔗 **Live Demo:** [Click Here](https://ai-risk-dashboard-192565971483.asia-south1.run.app/)

---

## 🎯 Theme Alignment
**Primary Theme:** Global Mobility  
**Secondary Theme:** International Collaboration  

This project aligns with the VisaVerse AI Hackathon by using AI to reduce environmental and safety barriers that affect **global movement, international travel, and cross-border collaboration**.

---

## 🧩 Problem Statement
People traveling, relocating, or collaborating across countries often lack **real-time environmental awareness** such as air quality, extreme weather, or seismic activity.  
This gap can impact **travel safety, productivity, and decision-making**, especially for international teams and mobile workers.

---

## 💡 Solution Overview
AI Environment Dashboard collects real-time environmental data from global sources and leverages **Gemini AI** to generate **human-readable, actionable insights**.  
Instead of raw numbers, users receive AI-driven explanations that make environmental risks easy to understand and respond to, anywhere in the world.

---

## 🧠 Key Features
- 🌍 Real-time global environmental monitoring  
- 🌡️ Weather, air quality, and seismic activity visualization  
- 🤖 Gemini AI-powered contextual insights  
- ☁️ Fully serverless & globally accessible  
- 🧭 Supports decision-making for travelers & international teams  

---

## 🛠️ Technologies Used
- **AI Layer:** Google AI Studio (Gemini Prompt API) – Generates contextual risk insights  
- **Backend:** Python (Flask)  
- **Frontend:** HTML, CSS, JavaScript  
- **APIs:** OpenWeatherMap API, USGS Earthquake API  
- **Hosting:** Google Cloud Run (serverless deployment)

---

## 🏗️ Architecture / Workflow
1. User selects a location or views global data  
2. Environmental data is fetched in real-time from public APIs  
3. Data is sent to Gemini AI for contextual analysis  
4. AI generates actionable insights  
5. Results are displayed via an interactive web dashboard

<img width="7163" height="5588" alt="Architecture Diagram (2) (1)" src="https://github.com/user-attachments/assets/5ab3d38f-d2a5-49a1-b4e2-d9b63b69a49c" />


---

## ⚙️ Setup Instructions

##1️⃣ Clone the Repository  

```bash
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
