from flask import jsonify, request, render_template
import os, sqlite3, traceback
from app import app
from app import socket_events

conf = app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
dir = os.path.abspath(os.path.dirname(__file__))

db_file = os.path.join(dir, "Tweets_db.sqlite")


@app.route("/twitter", methods=["GET"])
def get_tweets_from_period():
    """
    :param from_time: Example: 20181024140000
    :param to_time: 20181024141000
    :return: Json
    TODO: Limit the output of this
    """
    try:
        params = request.args
        if 'from_time' not in params and 'to_time' not in params:
            return jsonify({'error': 'missing arguments: from_time, to_time'})
        limit = 20
        if 'limit' in params:
            l = int(params['limit'])
            if 20 >= l > 0:
                limit = l

        from_time = params['from_time']
        to_time = params['to_time']

        query = "SELECT * FROM Tweet where created_at >= ? and created_at <= ? limit ?;"
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        tweets = cursor.execute(query, (from_time, to_time, limit)).fetchall()
        tweet_objects = []
        table_columns = list(map(lambda x: x[0], cursor.description))
        for i in range(len(tweets)):
            tweet = tweets[i]
            tweet_object = {}
            for j in range(len(table_columns)):
                tweet_object[table_columns[j]] = tweet[j]
            tweet_objects.append(tweet_object)
        json = {'tweets': tweet_objects, 'count': len(tweet_objects)}
        conn.close()
        return jsonify(json)
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({"Error": "An unknown error occurred, please contact developer."})


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route("/incomingTweet", methods=['POST'])
def receive_tweet():
    form = request.form
    tweet = form['tweet']
    socket_events.send_tweet(tweet)
    return ''
