from flask import Flask, request, render_template, jsonify
from ultralytics import YOLO
import torch
from PIL import Image
import os

app = Flask(__name__)

# Load custom YOLOv8 model for classification
model = YOLO("D:./runs/classify/train11/weights/best.pt")  # Gantilah dengan model hasil training Anda

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', error="No file part")
        
        file = request.files['file']
        if file.filename == '':
            return render_template('index.html', error="No selected file")
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        
        # Load image and run YOLOv8 classification
        img = Image.open(filepath)
        results = model(img)
        
        # Extract the top prediction
        pred_class = results[0].probs.top1  # Mendapatkan indeks kelas teratas
        class_name = model.names[pred_class]  # Nama kelas berdasarkan indeks
        confidence = results[0].probs.data[pred_class].item()*100
        
        return render_template('index.html', filename=file.filename, class_name=class_name, confidence=confidence)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
