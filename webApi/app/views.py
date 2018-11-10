from flask import jsonify, request, render_template
import sqlite3, traceback, json
from os import path
from app import app
from app import socket_events

conf = app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
dir = path.abspath(path.dirname(__file__))

db_file = path.join(dir, "Tweets_db.sqlite")


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
    if request.remote_addr == "127.0.0.1": # Only accept data from localhost
        form = request.form
        print(form)
        tweet = form['tweet']
        socket_events.send_tweet(tweet)
    return ''


@app.route("/incomingWordCount", methods=['POST'])
def receive_wordcount():
    if request.remote_addr == "127.0.0.1":  # Only accept data from localhost
        form = request.form
        count = json.loads(form['count'])

        counts = []
        for tuple in count[:100]:
            data = {}
            data['text'] = tuple[0]
            data['value'] = int(tuple[1])
            counts.append(data)
        if len(counts) > 50:
            json_out = {'word_count':counts}
            open(path.join(app.config['APP_FOLDER'], 'word_count.json'), 'w+')\
                .write(json.dumps(json_out))
        socket_events.send_wordcount(json.dumps(counts))
    return ''


@app.route("/incomingHashtagCount", methods=['POST'])
def receive_hashtag_count():
    if request.remote_addr == "127.0.0.1":  # Only accept data from localhost
        form = request.form
        count = json.loads(form['count'])

        counts = []
        for tuple in count[:100]:
            data = {}
            data['text'] = tuple[0]
            data['value'] = int(tuple[1]) * 10 # So few #hastags so we need to up the value for visualization
            counts.append(data)
        if len(counts) > 50:
            json_out = {'hashtag_count': counts}
            open(path.join(app.config['APP_FOLDER'], 'hashtag_count.json'), 'w+') \
                .write(json.dumps(json_out))

        socket_events.send_hashtagcount(json.dumps(counts))

    return ''
