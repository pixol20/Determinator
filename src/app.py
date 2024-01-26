import sys
from flask import Flask, render_template, request, Response
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
    purpose = ""
    data = request.get_json()
    try:
        purpose = data["DeterminationPurpose"]
    except:
        return Response("Wrong data sent", 400)

    if purpose == "":
        return Response(model.GenerateText(), 200)
    else:
        if purpose.isascii():
            return Response(model.GenerateText(purpose), 200)
        else:
            return Response("Your input contains non english characters", 400)