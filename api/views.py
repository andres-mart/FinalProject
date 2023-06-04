import os
import settings
from datetime import date

from flask import (
    Blueprint,
    current_app,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)

from middleware import model_predict
from utils.readdata import read_json

router = Blueprint("app_router", __name__, template_folder="templates")

@router.route("/", methods=["GET", "POST"])
def index():
    """
    GET: Index endpoint, renders our HTML code.

    POST: Used in our frontend so we can put info about rides.
    It also calls our ML model to get and display the predictions.
    """
    zones = read_json()
    zones = sorted(zones, key=lambda d: d['zone'])

    if request.method == "GET":
        return render_template("index.html", zones=zones)

    if request.method == "POST":

        origin = request.form.get("origin")
        dest = request.form.get("destination")
        time_input = request.form.get("time")

        model_request = {
            "start_point": origin, 
            "dest_point": dest, 
            "time": time_input
        }

        fare, time = model_predict(model_request)
        context = {
            "fare":fare,
            "time":time
        }

    return render_template("index.html",context=context, zones=zones, inputs=model_request)


