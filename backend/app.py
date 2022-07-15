from random import shuffle
from flask import Flask, jsonify
from flask_socketio import SocketIO
from flask_socketio import send, emit

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
def connect(sid):
    print(sid)
    print(clients)
    if not clients['p1']:
        clients['p1'] = sid
    
    elif not clients['p2']:
        clients['p2'] = sid
    
    else:
        return


@socketio.on('push')
def handlePlace():
    message = 'Hi!'
    emit('response', message)

@socketio.on('card')
def handleCard(number):
    print('run')
    emit('card-res', number)

@socketio.on('reset')
def reset_game():
    cards = []
    for card in total_cards:
        cards.append(card)
    shuffle(cards)
    print(cards)
    player1_cards = cards[:25]
    player2_cards = cards[25:51]
    sides = cards[51:]
    emit('reset', player1_cards)


if __name__ == '__main__':
    socketio.run(app)