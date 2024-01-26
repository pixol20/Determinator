from flask import Flask, render_template
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import model
app = Flask(__name__)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["2 per minute"],
    storage_uri="memory://",
)
model.LoadModel()
@app.route("/")
@limiter.exempt()
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    return(model.GenerateText(), 200)
