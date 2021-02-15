from flask import Flask, render_template, request, jsonify
import requests
import random

app = Flask(__name__)


@app.route("/")
def homepage():
    """Show homepage."""

    return render_template("index.html")

######### API Route #########


@app.route('/api/get-lucky-num', methods=["POST"])
def lucky_num_data():
    error = {"error": {}}
    color_list = ["red", "blue", "green", "orange"]

    # Error is no json is sent/received
    if not request.json:
        return {"error": {
            "name": "The name field is required.",
            "email": "The email field is required.",
            "year": "The year field is required.",
            "color": "The color field is required."
        }}

    # Individual errors is specific json kv is not received
    if "name" not in request.json or request.json["name"] is "":
        error["error"]["name"] = "The name field is required."
    if "email" not in request.json or request.json["email"] is "":
        error["error"]["email"] = "The email field is required."
    if "year" not in request.json or request.json["year"] is "":
        error["error"]["year"] = "The year field is required."
    elif int(request.json["year"]) < 1900 or int(request.json["year"]) > 2000:
        error["error"]["year"] = "Year must be between 1900 and 2000, inclusive."
    if "color" not in request.json or request.json["color"] is "":
        error["error"]["color"] = "The color field is required."
    elif request.json["color"].lower() not in color_list:
        error["error"]["color"] = "Invalid value, must be one of: red, green, orange, blue."

    if len(error["error"]) != 0:
        return jsonify(error)

    year = request.json["year"]
    rand_num = random.randint(1, 100)

    res_num = requests.get(f"http://numbersapi.com/{rand_num}/year")
    res_year = requests.get(f"http://numbersapi.com/{year}/year")

    return {
        "num": {
            "fact": f"{res_num.text}",
            "num": rand_num
        },
        "year": {
            "fact": f"{res_year.text}",
            "year": year
        }}
