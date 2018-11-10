from flask import Flask
from flask_socketio import SocketIO
from os import path
app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'somerandomlongstringofcharacters'
app.config['APP_FOLDER'] = path.abspath(path.dirname(__file__))
socketio = SocketIO(app, engineio_logger=True)

from app import socket_events, views
