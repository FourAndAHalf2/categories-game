from flask import Flask, jsonify, render_template
from flask_cors import CORS
from cached_get import cached_get
from os import getenv
from json import loads
from time import time
from collections import defaultdict
from functools import wraps
from category import Category


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


def get_aviable_categories():
    return [
        Category("countries", fetch_function=get_countries),
        Category(
            "cities",
            url="https://raw.githubusercontent.com/FinNLP/cities-list/refs/heads/master/list.txt",
            parser=lambda raw: [s for s in raw.split("\n") if s],
        ),
        Category(
            "animals",
            url="https://raw.githubusercontent.com/sroberts/wordlists/refs/heads/master/animals.txt",
            parser=lambda raw: [i.capitalize() for i in raw.split("\n") if i],
        ),
        Category(
            "fruits",
            url=(
                "https://gist.githubusercontent.com/lasagnaphil/7667eaeddb6ed0c565f0cb653d756942/raw/"
                "e05dbc73062aa1679b733e8f9f9b32e003c59d0e/fruits.txt"
            ),
            parser=lambda raw: [i.capitalize() for i in raw.split("\n") if i],
        ),
        Category(
            "car-brands",
            url=(
                "https://gist.githubusercontent.com/pimatco/64aec435e2a0abeeac8f30e24f918c11/raw/"
                "abaa40fd556e00cdddd7209836daf640740deaac/carbrands.json"
            ),
            parser=lambda raw: [brand["name"] for brand in loads(raw)],
        ),
        Category(
            "first-names",
            url=(
                "https://raw.githubusercontent.com/dominictarr/random-name/refs/heads/master/first-names.txt"
            ),
            parser=lambda raw: [i.strip() for i in raw.split("\n") if i.strip()],
        ),
    ]


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


@app.route("/api/all-categories")
def all_categories():
    return jsonify([c.name for c in get_aviable_categories()])


@app.route("/api/category/<category>")
def category(category):
    # find category by name
    categories = {c.name: c for c in get_aviable_categories()}
    cat = categories.get(category)
    if cat is None:
        return jsonify({"error": "category not found"}), 404

    start = time()
    try:
        items = cat.get_items()
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    stop = time()
    response_times[cat.name].append(stop - start)
    return jsonify(items)


@app.route("/")
def index():
    return render_template(
        "index.html",
        names=list(response_times.keys()),
        average_response_times=[
            round(sum(i) / len(i) * 100, 2) for i in response_times.values()
        ],
        length=len(response_times),
    )


if __name__ == "__main__":
    if getenv("RESTCOUNTRIES_API_KEY") is None:
        print("Warning: RESTCOUNTRIES_API_KEY is missing")
        exit()

    app.run(host="0.0.0.0", port=5000, debug=True)
