import sys
from flask import Flask, render_template, request, Response, session
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
app.secret_key = "£<0Bu_k+£yj/SM[WvQf&HD.k<£j8[pHkY$sMBs+GwKr4=!e;22DETERMINATION"
model.LoadModel()



@app.route("/")
@limiter.exempt()
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    purpose = data["DeterminationPurpose"]


    if purpose == "":
        return Response(model.GenerateText(), 200)
    else:
        if purpose.isascii():
            return Response(model.GenerateText(purpose), 200)
        else:
            return Response("Your input contains non english characters", 400)



@app.route("/preferences", methods=["POST"])
@limiter.exempt()
def preferences():
    SendData = False
    data = request.get_json()
    intent = data["intent"]


    if intent == "get":
        if "SendData" in session:
            SendData = session["SendData"]
        else:
            session["SendData"] = False
        return Response(str(SendData), 200)
    else:
        PreferenceData = data["sendData"]
        session["SendData"] = PreferenceData
        return Response("", 204)
    return Response("", 500)