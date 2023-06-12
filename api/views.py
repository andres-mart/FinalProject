from datetime import date

from flask import (
    Blueprint,
    current_app,
    flash,
    render_template,
    request
)

from middleware import model_predict
import utils.readdata as read

router = Blueprint("app_router", __name__, template_folder="templates")

@router.route("/", methods=["GET", "POST"])
def index():
    """
    GET: Index endpoint, renders our HTML code.

    POST: Used in our frontend so we can put info about rides.
    It also calls our ML model to get and display the predictions.
    """
    pickup_zones = read.read_pickup()
    dropoff_zones = read.read_dropoff()
    pickup_zones = sorted(pickup_zones, key=lambda d: d['zone'])
    dropoff_zones = sorted(dropoff_zones, key=lambda d: d['zone'])

    if request.method == "GET":
        return render_template("index.html", pickup_zones=pickup_zones,dropoff_zones=dropoff_zones)

    if request.method == "POST":

        origin = request.form.get("origin")
        dest = request.form.get("destination")
        time_input = request.form.get("time")

        model_request = {
            "start_point": origin, 
            "dest_point": dest, 
            "time": time_input
        }

        fare, duration = model_predict(model_request)

        context = {
            "fare":fare,
            "duration":duration,
            "origin": origin,
            "destination": dest
        }

        #flash(context)

    return render_template("index.html",context=context, pickup_zones=pickup_zones,dropoff_zones=dropoff_zones, inputs=model_request)


