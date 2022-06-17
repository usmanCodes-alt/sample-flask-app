from flask import Flask,request, jsonify
from flask_cors import cross_origin
import sentiment

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello world"

@app.route('/get-sentiments', methods=['POST'])
@cross_origin(origins='*')
def sentiments():
    # key -> user review, value -> dict {polarity: '', subjectivity: ''}
    print('running controller')
    sentiment_dict = {}
    counter = 0
    json_posted = request.get_json()
    # print(json_posted)

    if json_posted is None:
        return jsonify('Please provide reviews for sentiment')

    # [{review: "", sp_id: 1}, ...]
    all_reviews = json_posted.get('reviews')

    for current_review in all_reviews:
        blob = sentiment.perform_analysis(current_review.get('review'))
        # sentiment_dict[f'review_{counter}'] = current_review.get('review')
        sentiment_dict[f'sentiment_analysis_{counter}'] = {
            'polarity': blob.sentiment.polarity, 'subjectivity': blob.sentiment.subjectivity, "sp_id": current_review.get("sp_id"), "review": current_review.get('review')}
        # sentiment_list.append(sentiment_dict)
        counter += 1
        # sentiment_dict = {}

    print("SENTIMENT DICTIONARY", sentiment_dict)
    return sentiment_dict


if __name__ == "__main__":
    app.run(debug=True)
