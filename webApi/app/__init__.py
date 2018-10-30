from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'somerandomlongstringofcharacters'
socketio = SocketIO(app, engineio_logger=True)

from app import socket_events, views
