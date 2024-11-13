from flask import Flask, render_template, request
import mbta_helper

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/nearest_mbta", methods=["POST"])
def nearest_mbta():
    location = request.form["location"]
    try:
        # Get the nearest station details, including weather
        result = mbta_helper.find_stop_near(location)
        
        return render_template(
            "mbta_station.html",
            location=location,
            stop_name=result["station_name"],
            wheelchair_accessible=result["wheelchair_accessible"],
            weather=result["weather"]  # Pass weather data to the template
        )
    except Exception as e:
        return render_template("error.html", error_message=str(e))

if __name__ == "__main__":
    app.run(debug=True)
