This file provides full documentation for your Malaria Parasite Detection project.

# 🦠 Malaria Parasite Detection Using Deep Learning

## 📌 Project Overview
This project is a **Flask-based web application** that detects **Malaria parasites** in blood smear images using a **CNN deep learning model**.  
It classifies images into:
✅ **"Parasitized"** (Infected with Malaria)  
✅ **"Uninfected"** (Healthy)  

By automating malaria detection, this project helps in **faster diagnosis and better healthcare outcomes**. 🚀

---

## 📂 Project Structure
/Malaria_Parasite_Detection │── app.py # Flask backend (handles requests & model inference) │── malaria_model.h5 # Trained deep learning model │── requirements.txt # Dependencies for installation │── templates/ │ └── index.html # Web frontend (UI) │── static/ │ ├── styles.css # CSS for styling │ ├── script.js # JavaScript for frontend interactions │── README.md # Project documentation

---

## 🚀 **How to Run the Project**
### **1️⃣ Install Dependencies**
Make sure you have Python installed (version 3.8+ recommended).  
Run the following command to install the required libraries:  
```bash
pip install -r requirements.txt
2️⃣ Place the Model File
Download or move your trained model file malaria_model.h5 into the project folder.
Ensure that app.py correctly points to this file:
python
MODEL_PATH = "malaria_model.h5"
3️⃣ Run the Flask App
Start the web server using:
python app.py
4️⃣ Open the Website
Once the server is running, open your web browser and go to:
http://127.0.0.1:5000/

🖼️ How It Works
1️⃣ Upload a blood smear image
2️⃣ The model processes the image and makes a prediction
3️⃣ The app displays whether the sample is Parasitized or Uninfected

📚 Technologies Used
Flask – Web framework for handling requests & rendering the UI
TensorFlow/Keras – Deep learning model for malaria detection
NumPy – Data handling & numerical computations
Pillow (PIL) – Image preprocessing
HTML, CSS, JavaScript – Frontend for the web application

🎯 Future Enhancements
🔹 Add support for real-time camera uploads
🔹 Store patient records in a database for medical history tracking
🔹 Deploy the model to the cloud for easier access

📌 Credits
Developed by: Likhitha Gogisetti & Team
Based on research paper: Malaria Parasite Detection Using Deep Learning

📧 Contact: likhithagogisetti@gmail.com