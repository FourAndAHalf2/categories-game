from flask import Flask, jsonify
from flask_cors import CORS
from cached_get import cached_get, cached_get_static
from os import getenv
from json import  loads


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


@app.route("/api/countries")
def countries():
    countries_list = get_countries()
    return jsonify(countries_list)


@app.route("/api/cities")
def cities():
    list_of_cities = cached_get_static(
        "https://raw.githubusercontent.com/FinNLP/cities-list/refs/heads/master/list.txt"
    ).split("\n")
    return jsonify(list_of_cities)


@app.route("/api/animals")
def animals():
    list_of_animals = cached_get_static(
        "https://raw.githubusercontent.com/sroberts/wordlists/refs/heads/master/animals.txt"
    ).split("\n")   

    return jsonify([i.capitalize() for i in list_of_animals])


if __name__ == "__main__":
    if getenv("RESTCOUNTRIES_API_KEY") is None:
        print("Warning: RESTCOUNTRIES_API_KEY is missing")
        exit()

    app.run(host="0.0.0.0", port=5000, debug=True)
