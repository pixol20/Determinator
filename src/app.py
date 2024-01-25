from flask import Flask, render_template
import model
app = Flask(__name__)
model.LoadModel()
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    return(model.GenerateText(), 200)
