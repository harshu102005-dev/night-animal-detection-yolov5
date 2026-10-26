from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import io
from PIL import Image
import numpy as np
import torch
import cv2
from model_utils import enhance

app = Flask('__name__')
CORS(app)

device = "cuda" if torch.cuda.is_available() else "cpu"
model = torch.hub.load("ultralytics/yolov5", "yolov5s", pretrained=True).to(device)
names = model.names

@app.route("/predict", methods=["POST"])
def predict():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]
    img = Image.open(file.stream).convert("RGB")
    img_np = np.array(img)

    enhanced = enhance(img_np)

    results = model(enhanced, size=640)
    rendered = results.render()[0]
    rendered = cv2.cvtColor(rendered, cv2.COLOR_BGR2RGB)

    output_pil = Image.fromarray(rendered)
    buf = io.BytesIO()
    output_pil.save(buf, format="JPEG")
    buf.seek(0)

    return send_file(buf, mimetype="image/jpeg")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)