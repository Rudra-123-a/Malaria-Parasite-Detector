import os
import numpy as np
import tensorflow as tf
import gdown
from flask import Flask, request, render_template, redirect, url_for, send_from_directory
from tensorflow.keras.preprocessing import image
from werkzeug.utils import secure_filename

# print("TensorFlow running on:", "GPU" if tf.config.list_physical_devices('GPU') else "CPU")

app = Flask(__name__)

MODEL_PATH = "model/malaria_model.h5"

# Ensure model directory exists
os.makedirs("model", exist_ok=True)

# Direct Google Drive download
url = "https://drive.google.com/file/d/1gxQzYWm6ChnnB8pOCfzk6uynf_digZjD/view?usp=sharing"
output = "model/malaria_model.h5"

# Check if file already exists to avoid redownload
if not os.path.exists(output):
    print("Downloading model from Google Drive...")
    gdown.download("https://drive.google.com/file/d/1gxQzYWm6ChnnB8pOCfzk6uynf_digZjD/view?usp=sharing", output, quiet=False, fuzzy=True)

# Load the trained model
# MODEL_PATH = "model/malaria_model.h5"  # Use forward slashes for cross-platform compatibility
model = tf.keras.models.load_model(MODEL_PATH)


UPLOAD_FOLDER = "static/uploads"
GRAPHS_FOLDER = "static/graphs"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Ensure the upload and graphs directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(GRAPHS_FOLDER, exist_ok=True)

def predict_image(img_path):
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
            
            # Debug: Check if the image is saved correctly
            if os.path.exists(file_path):
                print(f"Image successfully saved at: {file_path}")
            else:
                print("Error: Image was not saved correctly!")
            
            result = predict_image(file_path)
            
            return render_template("index.html", prediction=result, image_path=url_for('static', filename='uploads/' + filename))
    
    return render_template("index.html", prediction=None, image_path=None)

# Fixed route for serving graph images
@app.route('/static/graphs/<path:filename>')
def serve_graphs(filename):
    return send_from_directory(GRAPHS_FOLDER, filename)

port = int(os.environ.get("PORT", 10000))  # Render sets PORT automatically

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=os.getenv("FLASK_DEBUG") == "1")
