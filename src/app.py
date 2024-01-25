from flask import Flask
import model
app = Flask(__name__)
model.LoadModel()
model.GenerateText("lorem ipsum")
@app.route("/")
def index():
    return "Hello World"