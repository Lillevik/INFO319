from app import app, socketio

if __name__ == '__main__':
    app.host = '0.0.0.0'
    app.debug = False
    socketio.run(app)




