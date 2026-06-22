from flask import Flask, jsonify, render_template
from flask_cors import CORS
from cached_get import cached_get, cached_get_static
from os import getenv
from json import loads
from time import time
from collections import defaultdict
from functools import wraps


app = Flask(__name__)
CORS(app)


def get_countries():
    countries = []
    for offset in range(0, 301, 100):
        response = cached_get(
            f"https://api.restcountries.com/countries/v5?response_fields=names.common&limit=100&offset={offset}",
            headers={"Authorization": f"Bearer {getenv('RESTCOUNTRIES_API_KEY')}"},
            cache_duration=24 * 60,  # Cache for a day
        )
        countries.extend(
            [
                country["names"]["common"]
                for country in loads(response)["data"]["objects"]
            ]
        )

    return countries


response_times = defaultdict(list)


def calculate_average_response_time(fn):
    @wraps(fn)
    def wrapper():
        start = time()
        result = fn()
        stop = time()
        response_times[fn].append(stop - start)
        return result

    return wrapper


@app.route("/api/countries")
@calculate_average_response_time
def countries():
    countries_list = get_countries()
    return jsonify(countries_list)


@app.route("/api/cities")
@calculate_average_response_time
def cities():
    list_of_cities = cached_get_static(
        "https://raw.githubusercontent.com/FinNLP/cities-list/refs/heads/master/list.txt"
    ).split("\n")
    return jsonify(list_of_cities)


@app.route("/api/animals")
@calculate_average_response_time
def animals():
    list_of_animals = cached_get_static(
        "https://raw.githubusercontent.com/sroberts/wordlists/refs/heads/master/animals.txt"
    ).split("\n")

    return jsonify([i.capitalize() for i in list_of_animals])


@app.route("/api/fruits")
@calculate_average_response_time
def fruits():
    list_of_fruits = cached_get_static(
        "https://gist.githubusercontent.com/lasagnaphil/7667eaeddb6ed0c565f0cb653d756942/raw/e05dbc73062aa1679b733e8f9f9b32e003c59d0e/fruits.txt"
    ).split("\n")

    return jsonify([i.capitalize() for i in list_of_fruits])


@app.route("/api/car-brands")
@calculate_average_response_time
def car_brands():
    list_of_car_brands = cached_get_static(
        "https://gist.githubusercontent.com/pimatco/64aec435e2a0abeeac8f30e24f918c11/raw/abaa40fd556e00cdddd7209836daf640740deaac/carbrands.json"
    )
    list_of_car_brands = loads(list_of_car_brands)
    list_of_car_brands = [brand["name"] for brand in list_of_car_brands]
    return jsonify(list_of_car_brands)

@app.route("/api/first-names")
@calculate_average_response_time
def first_names():
    list_of_first_names = [i.strip() for i in cached_get_static("https://raw.githubusercontent.com/dominictarr/random-name/refs/heads/master/first-names.txt").split("\n")]
    return list_of_first_names

@app.route("/")
def index():
    return render_template(
        "index.html",
        names=[i.__name__ for i in response_times],
        average_response_times=[round(sum(i) / len(i)*100,2) for i in response_times.values()],
        length=len(response_times),
    )


if __name__ == "__main__":
    if getenv("RESTCOUNTRIES_API_KEY") is None:
        print("Warning: RESTCOUNTRIES_API_KEY is missing")
        exit()

    app.run(host="0.0.0.0", port=5000, debug=True)
