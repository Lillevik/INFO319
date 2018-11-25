from flask import jsonify, request, render_template
import sqlite3, traceback, json
from os import path
from app import app
from app import socket_events


@app.route("/incomingTweet", methods=['POST'])
def receive_tweet():
    if request.remote_addr == "127.0.0.1": # Only accept data from localhost
        form = request.form
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
            data['value'] = int(tuple[1])
            counts.append(data)
        if len(counts) > 50:
            json_out = {'hashtag_count': counts}
            open(path.join(app.config['APP_FOLDER'], 'hashtag_count.json'), 'w+') \
                .write(json.dumps(json_out))

        socket_events.send_hashtagcount(json.dumps(counts))

    return ''
