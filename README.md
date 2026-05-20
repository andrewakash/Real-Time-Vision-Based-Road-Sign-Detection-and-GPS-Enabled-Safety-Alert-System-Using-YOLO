# README.md

````markdown
# 🚦 Real-Time Vision-Based Road Sign Detection and GPS-Enabled Safety Alert System using YOLO

An AI-powered intelligent transportation safety system that performs **real-time road sign detection**, **GPS tracking**, and **driver safety alerts** using **YOLO (You Only Look Once)** and Flask-based web technologies.

---

## 📌 Project Overview

This project is designed to improve road safety by detecting traffic signs in real time using computer vision and providing GPS-based safety alerts.

The system:
- Detects road signs using YOLO
- Tracks live GPS coordinates
- Displays route and map visualization
- Sends zone-based alerts
- Provides a web dashboard using Flask

---

## 🚀 Features

✅ Real-time road sign detection  
✅ YOLO-based object detection  
✅ Live GPS coordinate tracking  
✅ Interactive map visualization  
✅ Speed and zone alert system  
✅ Flask web application  
✅ JSON route history support  
✅ Safety notification system  

---

## 🛠️ Technologies Used

### Programming Language
- Python

### AI / Machine Learning
- YOLO
- OpenCV

### Web Technologies
- HTML
- CSS
- JavaScript
- Flask

### Other Tools
- GPS Integration
- JSON
- Ngrok

---

## 📂 Project Structure

```bash
├── gps_project/
├── sign_Board/
│   ├── best.pt
│   └── detect.py
├── static/
│   ├── app.js
│   ├── map.html
│   └── style.css
├── templates/
│   ├── gps.html
│   └── index.html
├── detect_web.py
├── gps_server.py
├── start_ngrok.py
├── zone_alert.py
├── route.json
└── README.md
````

---

## ⚙️ Installation

### 1️⃣ Clone Repository

```bash
git clone https://github.com/andrewakash/Real-Time-Vision-Based-Road-Sign-Detection-and-GPS-Enabled-Safety-Alert-System-Using-YOLO.git
```

### 2️⃣ Navigate to Project Folder

```bash
cd Real-Time-Vision-Based-Road-Sign-Detection-and-GPS-Enabled-Safety-Alert-System-Using-YOLO
```

### 3️⃣ Create Virtual Environment

```bash
python -m venv .venv
```

### 4️⃣ Activate Environment

#### Windows

```bash
.venv\Scripts\activate
```

#### Linux / Mac

```bash
source .venv/bin/activate
```

### 5️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Project

### Start Flask Server

```bash
python gps_server.py
```

### Start YOLO Detection

```bash
python detect_web.py
```

### Start Ngrok (Optional)

```bash
python start_ngrok.py
```

---

## 🌐 Web Dashboard

After running the server:

```bash
http://127.0.0.1:5000
```

---

## 🧠 How It Works

1. Camera captures live road video
2. YOLO detects traffic signs
3. GPS module sends coordinates
4. Flask server processes data
5. Web dashboard displays:

   * Live map
   * Speed
   * Alerts
   * Route tracking

---

## 📸 System Modules

### 🔹 Road Sign Detection

Detects:

* Speed limits
* Stop signs
* Warning signs
* Traffic instructions

### 🔹 GPS Tracking

Tracks:

* Latitude
* Longitude
* Route history

### 🔹 Safety Alert System

Generates alerts for:

* Restricted zones
* Overspeed conditions
* Dangerous areas

---

## 📈 Future Enhancements

* Mobile application integration
* Voice alert system
* Cloud database support
* Real-time analytics dashboard
* Emergency notification system

---

## 👨‍💻 Author

### Akash S

Computer Science and Engineering

---

## 📜 License

This project is developed for educational and research purposes.




