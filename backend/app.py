from flask import Flask
from flask_socketio import SocketIO
from flask_socketio import send, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*', logger=True)


@socketio.on('push')
def handlePlace():
    message = 'Hi!'
    emit('response', message)

@socketio.on('card')
def handleCard(number):
    print('run')
    emit('card-res', number)


if __name__ == '__main__':
    socketio.run(app)