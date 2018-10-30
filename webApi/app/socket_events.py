from flask_socketio import emit, send, join_room, leave_room
from app import socketio

clients = []


@socketio.on('message')
def message(message):
    emit('message', message)


@socketio.on('connect')
def on_connect():
    emit('connected', {
        'data': 'Connected',
        'success': 'true'
    })
    # TODO: Handle success handling


@socketio.on('disconnect', namespace='/chat')
def test_disconnect():
    # TODO: Handle disconnect event on the client side
    print('Client disconnected')


# Custom Events Below
@socketio.on('tweet')
def send_tweet(tweet):
    print("Sending tweet")
    socketio.emit('tweet', tweet, broadcast=True, json=True)
