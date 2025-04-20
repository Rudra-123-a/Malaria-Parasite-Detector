import os
import numpy as np
import tensorflow as tf
from flask import Flask, request, render_template, redirect, url_for, send_from_directory
from tensorflow.keras.preprocessing import image
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Load the trained model
MODEL_PATH = "model/malaria_model.h5"  # Use forward slashes for cross-platform compatibility
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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)
