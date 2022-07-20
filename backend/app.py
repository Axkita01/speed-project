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

deck_tops = [[None, None], [None, None]]

total_cards = [
    ['one', 'red', 1],
    ['one', 'black', 2],
    ['two', 'red', 3],
    ['two', 'black', 4],
    ['three', 'red', 5],
    ['three', 'black', 6],
    ['four', 'red', 7],
    ['four', 'black', 8],
    ['five', 'red', 9],
    ['five', 'black', 10],
    ['six', 'red', 11],
    ['six', 'black', 12],
    ['seven', 'red', 13],
    ['seven', 'black', 14],
    ['eight', 'red', 15],
    ['eight', 'black', 16],
    ['nine', 'red', 17],
    ['nine', 'black', 18],
    ['ten', 'red', 19],
    ['ten', 'black', 20],
    ['eleven', 'red', 21],
    ['eleven', 'black', 22],
    ['twelve', 'red', 23],
    ['twelve', 'black', 24],
    ['thirteen', 'red', 25],
    ['thirteen', 'black', 26],
    ['one', 'red', 27],
    ['one', 'black', 28],
    ['two', 'red', 29],
    ['two', 'black', 30],
    ['three', 'red', 31],
    ['three', 'black', 32],
    ['four', 'red', 33],
    ['four', 'black', 34],
    ['five', 'red', 35],
    ['five', 'black', 36],
    ['six', 'red', 37],
    ['six', 'black', 38],
    ['seven', 'red', 39],
    ['seven', 'black', 40],
    ['eight', 'red', 41],
    ['eight', 'black', 42],
    ['nine', 'red', 43],
    ['nine', 'black', 44],
    ['ten', 'red', 45],
    ['ten', 'black', 46],
    ['eleven', 'red', 47],
    ['eleven', 'black', 48],
    ['twelve', 'red', 49],
    ['twelve', 'black', 50],
    ['thirteen', 'red', 51],
    ['thirteen', 'black', 52]
]


@socketio.on('connect')
def connect():
    if not clients['p1']:
        clients['p1'] = request.sid
    
    if not clients['p2']:
        clients['p2'] = request.sid

@socketio.on('disconnect')
def disconnect():
    if request.sid == clients['p1']:
        clients['p1'] = clients['p2']
        clients['p2'] = None
    
    else:
        clients['p2'] = None
@socketio.on('push')
def handlePlace():
    message = 'Hi!'
    emit('response', message)

@socketio.on('card')
def handleCard(number):
    emit('card-res', number)

@socketio.on('reset')
#FIXME: make sure reset signal send from one of connected players
def reset_game():
    if request.sid not in clients.keys():
        return
    deck_tops = [{'color': 'empty', 'number': 'empty'}, {'color': 'empty', 'number': 'empty'}]
    cards = [card for card in total_cards]
    shuffle(cards)
    player1_cards = cards[:25]
    player2_cards = cards[25:51]
    sides = cards[51:]
    emit('reset', player1_cards, room=clients['p1'])
    emit('reset', player2_cards, room=clients['p2'])
    emit('tops-change', deck_tops)

@socketio.on('place')
def changeTops(element):
    elements = element
    emit('tops-change', elements)

if __name__ == '__main__':
    socketio.run(app)