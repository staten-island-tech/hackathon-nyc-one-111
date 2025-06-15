from flask import Flask, render_template, request
import requests

app = Flask(__name__)

NYC_API_URL = "https://data.cityofnewyork.us/resource/5zhs-2jue.json"

@app.route("/", methods=["GET", "POST"])
def index():
    building_data = None
    error = None
    bin_input = ""

    if request.method == "POST":
        bin_input = request.form.get("bin")
        if bin_input:
            try:
                response = requests.get(NYC_API_URL, params={"bin": bin_input})
                response.raise_for_status()
                data = response.json()
                if data:
                    building_data = data[0]  # Use the first record if multiple exist
                else:
                    error = f"No data found for BIN {bin_input}."
            except Exception as e:
                error = f"Error fetching data: {e}"
        else:
            error = "Please enter a BIN number."

    return render_template("index.html", bin_input=bin_input, data=building_data, error=error)

if __name__ == "__main__":
    app.run(debug=True)
