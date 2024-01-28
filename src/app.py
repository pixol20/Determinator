import csv
import sys
from pathlib import Path
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

# DON'T FORGET TO CHANGE ON DEPLOYMENT!
app.secret_key = "£<0Bu_k+£yj/SM[WvQf&HD.k<£j8[pHkY$sMBs+GwKr4=!e;22DETERMINATION"
model.LoadModel()


# CSV to create dataset for fine-tuning
CSVpath = "../GenerationsLog/generations.csv"
LogExists = Path(CSVpath).is_file()
header = ["purpose", "output", "rating"]
if not LogExists:
    with open(CSVpath, 'w') as file:
        writer = csv.writer(file, delimiter="|")
        writer.writerow(header)

def WriteLog(purpose, output, rating):
    with open(CSVpath, 'a', newline='') as file:
        writer = csv.writer(file, delimiter="|")
        writer.writerow([purpose, output, rating])

@app.route("/")
@limiter.exempt()
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    output = ""
    data = request.get_json()
    purpose = data["DeterminationPurpose"]
    if len(purpose) > 250:
        return Response("too long, maximum 250 characters", 400)

    if purpose == "":
        session["LastPurpose"] = purpose
        session["LastOutput"] = output
        session["AlreadyRated"] = False
        return Response(model.GenerateText(), 200)
    else:
        if purpose.isascii():
            output = model.GenerateText(purpose)

            # Save data to session to write that and rating later into CSV file
            session["LastPurpose"] = purpose
            session["LastOutput"] = output
            session["AlreadyRated"] = False
            return Response(output, 200)
        else:
            return Response("Your input contains non english characters", 400)



@app.route("/preferences", methods=["POST"])
@limiter.exempt()
def preferences():
    # SendData is false by default
    SendData = False
    data = request.get_json()

    # There can be get and set intents.
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


@app.route("/rate", methods=["POST"])
@limiter.exempt()
def rate():
    data = request.get_json()
    if not ("AlreadyRated" in session):
        session["AlreadyRated"] = False

    if not ("LastPurpose" in session):
        session["LastPurpose"] = None

    if not ("LastOutput" in session):
        session["LastOutput"] = None


    if not session["AlreadyRated"]:
        # Why are we doing this? Because potential attacker can send something weird in rate
        rate = ""
        if data["rate"] == "like":
            rate = "like"
        elif data["rate"] == "dislike":
            rate = "dislike"
        else:
            return Response("wrong data sent", 400)

        if (session["LastPurpose"] is None) or (session["LastOutput"] is None):
            return Response("didn't generate", 400)
        if session["SendData"] == True:
            WriteLog(session["LastPurpose"], session["LastOutput"], rate)
            session["AlreadyRated"] = True
        return Response("", 204)
    return Response("Something went wrong", 500)