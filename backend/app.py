import eventlet
eventlet.monkey_patch()
from random import shuffle
from flask import request
from flask import Flask
from flask_socketio import SocketIO
from flask_socketio import emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*', logger=True)

clients = {
    'p1': None,
    'p2': None
}
total_cards = [
    ['one', 'red'],
    ['one', 'black'],
    ['two', 'red'],
    ['two', 'black'],
    ['three', 'red'],
    ['three', 'black'],
    ['four', 'red'],
    ['four', 'black'],
    ['five', 'red'],
    ['five', 'black'],
    ['six', 'red'],
    ['six', 'black'],
    ['seven', 'red'],
    ['seven', 'black'],
    ['eight', 'red'],
    ['eight', 'black'],
    ['nine', 'red'],
    ['nine', 'black'],
    ['ten', 'red'],
    ['ten', 'black'],
    ['eleven', 'red'],
    ['eleven', 'black'],
    ['twelve', 'red'],
    ['twelve', 'black'],
    ['thirteen', 'red'],
    ['thirteen', 'black'],
    ['one', 'red'],
    ['one', 'black'],
    ['two', 'red'],
    ['two', 'black'],
    ['three', 'red'],
    ['three', 'black'],
    ['four', 'red'],
    ['four', 'black'],
    ['five', 'red'],
    ['five', 'black'],
    ['six', 'red'],
    ['six', 'black'],
    ['seven', 'red'],
    ['seven', 'black'],
    ['eight', 'red'],
    ['eight', 'black'],
    ['nine', 'red'],
    ['nine', 'black'],
    ['ten', 'red'],
    ['ten', 'black'],
    ['eleven', 'red'],
    ['eleven', 'black'],
    ['twelve', 'red'],
    ['twelve', 'black'],
    ['thirteen', 'red'],
    ['thirteen', 'black']
]


@socketio.on('connect')
def connect():
    print(clients)
    print(request.sid)
    if not clients['p1']:
        clients['p1'] = request.sid
    
    elif not clients['p2']:
        clients['p2'] = request.sid
    
    else:
        return

@socketio.on('disconnect')
def disconnect():
    print(clients)
    if request.sid == clients['p1']:
        clients['p1'] = clients['p2']
        clients['p2'] = None
    
    else:
        clients['p2'] = None
    print('disconnected')
    print(clients)
@socketio.on('push')
def handlePlace():
    message = 'Hi!'
    emit('response', message)

@socketio.on('card')
def handleCard(number):
    emit('card-res', number)

@socketio.on('reset')
def reset_game():
    cards = [card for card in total_cards]
    shuffle(cards)
    player1_cards = cards[:25]
    player2_cards = cards[25:51]
    sides = cards[51:]
    emit('reset', player1_cards, room=clients['p1'])
    emit('reset', player2_cards, room=clients['p2'])


if __name__ == '__main__':
    socketio.run(app)