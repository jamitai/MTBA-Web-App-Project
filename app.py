from flask import Flask, render_template, request
import mbta_helper


app = Flask(__name__)


@app.route("/")
def index():
    """
    Render the homepage with a form for the user to input a location.
    """
    return render_template("index.html")  


@app.route("/nearest_mbta", methods=["POST"])
def nearest_mbta():
    """
    Process the form input, call `find_stop_near`, and display the results.
    """
    try:
        # Get the user input from the form
        location = request.form["location"]

        # Use mbta_helper to find the nearest MBTA stop and wheelchair accessibility
        stop_name, wheelchair_accessible = mbta_helper.find_stop_near(location)

        # Render the result page with the MBTA stop information
        return render_template(
            "mbta_station.html",
            location=location,
            stop_name=stop_name,
            wheelchair_accessible=wheelchair_accessible
        )
    except Exception as e:
        error_message = str(e)
        return render_template("error.html", error_message=error_message)


if __name__ == "__main__":
    app.run(debug=True)
