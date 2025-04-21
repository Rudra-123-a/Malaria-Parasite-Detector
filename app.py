import os
import numpy as np
import tensorflow as tf
import gdown
from flask import Flask, request, render_template, redirect, url_for, send_from_directory
from tensorflow.keras.preprocessing import image
from werkzeug.utils import secure_filename

app = Flask(__name__)

MODEL_PATH = "model/malaria_model.h5"
model = None  # We'll load this lazily later

UPLOAD_FOLDER = "static/uploads"
GRAPHS_FOLDER = "static/graphs"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Ensure necessary directories exist
os.makedirs("model", exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(GRAPHS_FOLDER, exist_ok=True)

# Download model from Google Drive if not present
if not os.path.exists(MODEL_PATH):
    print("Downloading model from Google Drive...")
    gdown.download("https://drive.google.com/uc?id=1gxQzYWm6ChnnB8pOCfzk6uynf_digZjD", MODEL_PATH, quiet=False)

def load_model():
    global model
    if model is None:
        print("Loading model into memory...")
        model = tf.keras.models.load_model(MODEL_PATH)

def predict_image(img_path):
    load_model()  # Ensure model is loaded only when needed
    
    img = image.load_img(img_path, target_size=(150, 150))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    prediction = model.predict(img_array)

    label = "Parasitized" if prediction[0][0] < 0.5 else "Uninfected"
    return label

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        if "file" not in request.files:
            return redirect(request.url)

        file = request.files["file"]
        if file.filename == "":
            return redirect(request.url)

        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(file_path)

            if os.path.exists(file_path):
                print(f"Image saved at: {file_path}")
            else:
                print("Error saving image!")

            result = predict_image(file_path)

            return render_template("index.html", prediction=result, image_path=url_for('static', filename='uploads/' + filename))

    return render_template("index.html", prediction=None, image_path=None)

@app.route('/static/graphs/<path:filename>')
def serve_graphs(filename):
    return send_from_directory(GRAPHS_FOLDER, filename)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))  # Render will inject this
    app.run(host="0.0.0.0", port=port, debug=True)
