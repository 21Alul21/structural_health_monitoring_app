from app import app
from flask import render_template, request
import torch
from torchvision import transforms
from PIL import Image

# Load the model
MODEL_PATH = "model.pth"
model = torch.load(MODEL_PATH, map_location=torch.device("cpu"))
model.eval()

# Define image transformation
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
])

@app.route("/")
@app.route("/home-page", methods=["GET", "POST"])
def home():
    output = None

    if (request.method == "POST" and ("image" in request.files)):
        image_file = request.files["image"]

        if (image_file.filename == ""):
            output = "No image selected."
        else:
            try:
                image = Image.open(image_file.stream).convert("RGB")
                input_tensor = transform(image).unsqueeze(0)

                with torch.no_grad():
                    prediction = model(input_tensor)
                    predicted_class = torch.argmax(prediction, dim=1).item()

                labels = {0: "Safe", 1: "Damaged"}
                output = labels.get(predicted_class, "Unknown")

            except Exception as e:
                output = f"Error processing image: {e}"

    elif (request.method == "GET"):
        output = None

    return render_template("home.html", output=output)
