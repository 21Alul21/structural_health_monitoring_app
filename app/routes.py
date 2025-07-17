from app import app
from flask import render_template

@app.route("/")
@app.route("/home-page", methods=["GET", "POST"])
def home():
    if (request.method == "GET"):
        return render_template("home.html")

    if (request.method == "POST"):
        image = request.file["image"]
        // perform transformation on image
        // load model
        // use image on the model and store the output

        output = result from model prediction

        return render_template("home.html", output = output)

