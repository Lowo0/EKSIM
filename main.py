from flask import Flask, request, render_template, jsonify
from ultralytics import YOLO
import torch
from PIL import Image
import os

app = Flask(__name__)

# Load custom YOLOv8 model for classification
model = YOLO("D:./runs/classify/train13/weights/best.pt")  # Gantilah dengan model hasil training Anda

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Route untuk Landing Page
@app.route('/')
def home():
    return render_template('lpage.html')  # Menghubungkan ke lpage.html


# Route untuk Halaman Prediksi
@app.route('/prediksi', methods=['GET', 'POST'])
def prediksi():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', error="No file part")
        
        file = request.files['file']
        if file.filename == '':
            return render_template('index.html', error="No selected file")
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        
        # Prediksi
        img = Image.open(filepath)
        results = model(img)
        
        # Ambil semua probabilitas
        probs = results[0].probs.data.cpu()  # Pastikan di CPU
        predictions = []
        for idx, conf in enumerate(probs):
            predictions.append({
                'index': idx,
                'class_name': model.names[idx],
                'confidence': round(conf.item() * 100, 2)
            })
        
        # Nilai tertinggi
        top1_index = results[0].probs.top1
        top_class = model.names[top1_index]
        top_confidence = round(probs[top1_index].item() * 100, 2)
        
        #solusi penyakit
        solutions = {
        0: {
            "title": "Atopic Dermatitis (Eksim Atopik)",
            "content": """
                <strong>Penanganan:</strong><br>
                - Gunakan pelembap intensif (ceramide, petrolatum, shea butter)<br>
                - Hindari alergen (debu, bulu hewan, makanan tertentu)<br>
                - Gunakan sabun lembut tanpa pewangi<br>
                - Kompres dingin untuk gatal<br>
                - Krim kortikosteroid/topikal non-steroid<br>
                - Antihistamin/imunosupresan jika parah
            """
        },
        1: {
            "title": "Contact Dermatitis",
            "content": """
                <strong>Penanganan:</strong><br>
                - Hindari zat pemicu (deterjen, parfum, nikel)<br>
                - Cuci area terkena dengan sabun lembut<br>
                - Krim kortikosteroid anti-inflamasi<br>
                - Antihistamin untuk reaksi alergi<br>
                - Bilas segera jika terkena bahan kimia kuat
            """
        },
        2: {
            "title": "Nummular Dermatitis (Eksim Nummular)",
            "content": """
                <strong>Penanganan:</strong><br>
                - Pelembap oklusif (petroleum jelly/minyak mineral)<br>
                - Hindari mandi air panas<br>
                - Krim kortikosteroid untuk peradangan<br>
                - Jaga kebersihan untuk mencegah infeksi<br>
                - Antibiotik jika terjadi infeksi sekunder
            """
        }
        }
        
        #mengambil solusi dari hasil prediksi index tertinggi
        solution_data = solutions.get(top1_index, {
            "title": "Solusi Umum",
            "content": "Konsultasikan ke dokter spesialis kulit untuk penanganan lebih lanjut."
        })

        # if not solution_data:
        #     return jsonify({
        #     "error": True,
        #     "message": "Harap unggah gambar sebelum mengirim formulir."
        #     }), 400

        return render_template('index.html', 
                              filename=file.filename,
                              predictions=predictions,
                              top_class=top_class,
                              top_confidence=top_confidence,
                              top_class_index=top1_index,
                              solution_title=solution_data['title'],
                              solution_content=solution_data['content'])  # Perbaikan di sini
    
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)