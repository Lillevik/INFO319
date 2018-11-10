from flask_socketio import emit, send, join_room, leave_room
from app import socketio, app
from os import path
import json

clients = []


@socketio.on('message')
def message(message):
    emit('message', message)


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


@socketio.on('disconnect', namespace='/chat')
def test_disconnect():
    # TODO: Handle disconnect event on the client side
    print('Client disconnected')


# Custom Events Below
@socketio.on('tweet')
def send_tweet(tweet):
    print("Sending tweet")
    socketio.emit('tweet', tweet, broadcast=True, json=True)


# Custom Events Below
@socketio.on('word_count')
def send_wordcount(count):
    print("Sending word count")
    socketio.emit('word_count', count, broadcast=True, json=True)


# Custom Events Below
@socketio.on('hashtag_count')
def send_hashtagcount(count):
    print("Sending hashtag count")
    socketio.emit('hashtag_count', count, broadcast=True, json=True)
