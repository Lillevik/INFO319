from flask_socketio import emit, send, join_room, leave_room
from app import socketio, app
from os import path
import json, sqlite3


# Send latest data when client connects
@socketio.on('connect')
def on_connect():
    emit('connected', {
        'status': 'Connected',
        'success': True
    })
    ht_file_path = path.join(app.config['APP_FOLDER'], 'hashtag_count.json')
    word_file_path = path.join(app.config['APP_FOLDER'], 'word_count.json')
    if path.isfile(ht_file_path):
        ht_json = json.load(open(ht_file_path))
        send_hashtagcount(json.dumps(ht_json['hashtag_count']))
    if path.isfile(word_file_path):
        word_json = json.load(open(word_file_path))
        send_wordcount(json.dumps(word_json['word_count']))
    conn = sqlite3.connect(path.join(app.config['APP_FOLDER'], '../../emergency_tweets.sqlite'))
    curs = conn.cursor()
    tweets = curs.execute("SELECT Tweet.id, Tweet.text, Tweet.sentiment_score, User.profile_image_url,"
                          " User.screen_name FROM Tweet JOIN User ON User.id = Tweet.user_id "
                          "ORDER BY Tweet.id DESC LIMIT 20;""").fetchall()
    conn.close()
    tweet_list = []
    for row in tweets:
        tweet_list.append({
            'id': row[0],
            'text': row[1],
            'sentiment_score': row[2],
            'profile_image_url': row[3],
            'screen_name': row[4],
        })
    send_tweet(json.dumps(tweet_list))


@socketio.on('tweet')
def send_tweet(tweet):
    socketio.emit('tweet', tweet, broadcast=True, json=True)


@socketio.on('word_count')
def send_wordcount(count):
    socketio.emit('word_count', count, broadcast=True, json=True)


@socketio.on('hashtag_count')
def send_hashtagcount(count):
    socketio.emit('hashtag_count', count, broadcast=True, json=True)
