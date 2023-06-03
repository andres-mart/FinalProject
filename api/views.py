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
    if request.method == "GET":

        zones = read_json()
        return render_template("index.html", zones=zones)

    if request.method == "POST":
        flash("POST method")
        flash(request)
        model_request = {
            "point_from": 1, 
            "point_to": 2, 
            "time":date.today()
        }
        fair, time = model_predict(model_request)
        context = {
            "fair":fair,
            "time":time
        }
        return render_template("index.html",context=context)


@router.route("/predict", methods=["POST"])
def predict():
    """
    Endpoint used to get predictions without need to access the UI.

    Parameters
    ----------
    file : str
        Input image we want to get predictions from.

    Returns
    -------
    flask.Response
        JSON response from our API having the following format:
            {
                "success": bool,
                "prediction": str,
                "score": float,
            }

        - "success" will be True if the input file is valid and we get a
          prediction from our ML model.
        - "prediction" model predicted class as string.
        - "score" model confidence score for the predicted class as float.
    """
    request = {"point_from": 1, "point_to": 2, "time":date.today()}
    fair, time = model_predict(request)
    return jsonify({"fair":fair,"time":time})
