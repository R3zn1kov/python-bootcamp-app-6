from flask import Flask, render_template
import pandas as pd

app = Flask(__name__, template_folder='templates')

# df = pd.read_csv()
stations = pd.read_csv("data_small/stations.txt", skiprows=17)
stations = stations[["STAID", "STANAME                                 "]]


@app.route("/")
def home():
    return render_template("home.html", data=stations.to_html())


@app.route("/api/v1/<station>/<date>")
def about(station, date):
    filename = "data_small/TG_STAID" + str(station).zfill(6) + "txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    temperature = df.loc[df["    DATE"] == "1860-01-05"]['   TG'].squeeze() / 10

    return {"station": station,
            "date": date,
            "temperature": temperature}


@app.route("/api/v1/<station>")
def all_data(station):
    filename = "data_small/TG_STAID" + str(station).zfill(6) + "txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    results = df.to_dict(orient="records")
    return results


@app.route("/api/v1/year/<station>/<year>")
def yearly(station, year):
    filename = "data_small/TG_STAID" + str(station).zfill(6) + "txt"
    df = pd.read_csv(filename, skiprows=20)
    df["    DATE"] = df["    DATE"].astype(str)
    results = df[df["    DATE"].str.startswith(str(year))].to_dict(orient="records")
    return results


if __name__ == "__main__":
    app.run(debug=True, port=5001)
