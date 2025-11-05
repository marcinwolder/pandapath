from flask import Flask, request, jsonify
from flask_cors import CORS

from src.nlp_operations.main import AspectBasedSentimentAnalyzer


app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:4201"}})


# ab = AspectBasedSentimentAnalyzer()


@app.route('/get_place', methods=['POST'])
def get_place():
    """Check if loc exist in firebase db."""
    data = request.json

    # place = data['place']
    # print(place, type(place))
    subcategories = data['subcategories']
    reviews = [review['text'] for review in data['reviews']]
    subcat = ab.get_preferences_from_reviews(reviews)
    print(subcat)
    print(subcategories)

    return jsonify({
        "status": "success",
        "received_data": subcat
    })


def run_debug(data):
    place = data['place']
    # function to get reviews from place
    subcategories = data['subcategories']
    # ab = AspectBasedSentimentAnalyzer()
    # ab.get_preferences_from_text_data("text")
    print(place.placeInfo.displayName, place.placeInfo.name, place.placeInfo.id)
    print(subcategories)


if __name__ == '__main__':
    app.run(debug=True, port=5001)
    # pl = PlaceInfo(id=1, name="museum", displayName="Muzeum")
    # place = Place(placeInfo=pl)
    # run_debug({
    #     "subcategories": ["museum", "park", "zoo", "church",
    #                       "amusement_park", "aquarium", "art_gallery", "hindu_temple"],
    #     "place": place
    # })
