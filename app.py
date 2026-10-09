# app.py
from flask import Flask, request, render_template, send_file, jsonify
from PIL import Image
import io
import os
from prometheus_client import Counter, generate_latest, REGISTRY

app = Flask(__name__)

# Метрика: Счетчик посещений
REQUESTS = Counter('app_requests_total', 'Total requests to the app')

# --- Логика из твоего файла 5.2.py ---
def file_to_bits(file_data):
    size_bits = format(len(file_data), '032b')
    payload_bits = ''.join(format(byte, '08b') for byte in file_data)
    return size_bits + payload_bits

def bits_to_bytes(bits):
    byte_arr = bytearray()
    for i in range(0, len(bits), 8):
        byte_arr.append(int(bits[i:i+8], 2))
    return byte_arr

# --- Веб-роуты ---

@app.route('/')
def index():
    REQUESTS.inc() # Увеличиваем счетчик посещений
    return render_template('index.html') # Нужен простой HTML файл

@app.route('/health')
def health():
    return jsonify({"status": "ok"}), 200

@app.route('/metrics')
def metrics():
    return generate_latest(REGISTRY), 200, {'Content-Type': 'text/plain'}

@app.route('/hide', methods=['POST'])
def hide():
    REQUESTS.inc()
    exe_file = request.files['exe_file']
    img_file = request.files['img_file']
    
    if not exe_file or not img_file:
        return "Файлы не загружены", 400

    exe_data = exe_file.read()
    img = Image.open(img_file.stream).convert('RGB')
    pixels = img.load()
    width, height = img.size

    bits = file_to_bits(exe_data)
    
    if len(bits) > width * height * 3:
        return "Файл слишком велик для этой картинки!", 400

    idx = 0
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            res = [r, g, b]
            for i in range(3):
                if idx < len(bits):
                    res[i] = (res[i] & ~1) | int(bits[idx])
                    idx += 1
            pixels[x, y] = tuple(res)
            if idx >= len(bits): break
        if idx >= len(bits): break

    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    
    return send_file(img_io, mimetype='image/png', as_attachment=True, download_name='secret.png')

@app.route('/extract', methods=['POST'])
def extract():
    REQUESTS.inc()
    img_file = request.files['img_file']
    if not img_file:
        return "Файл не загружен", 400

    img = Image.open(img_file.stream).convert('RGB')
    pixels = img.load()
    
    all_bits = []
    for y in range(img.height):
        for x in range(img.width):
            r, g, b = pixels[x, y]
            all_bits.extend([str(r & 1), str(g & 1), str(b & 1)])
    
    size_bits = "".join(all_bits[:32])
    file_size = int(size_bits, 2)
    
    start = 32
    end = start + (file_size * 8)
    file_bits = "".join(all_bits[start:end])
    
    data = bits_to_bytes(file_bits)

    return send_file(io.BytesIO(data), mimetype='application/octet-stream', as_attachment=True, download_name='extracted.exe')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
