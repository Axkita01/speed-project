import eventlet
eventlet.monkey_patch()
from random import shuffle
from flask import request
from flask import Flask
from flask_socketio import SocketIO
from flask_socketio import emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins = '*')

clients = {
    'p1': None,
    'p2': None
}

deck_tops = [['', ''], ['', '']]

total_cards = [
    ['1', 'red', 1],
    ['1', 'black', 2],
    ['2', 'red', 3],
    ['2', 'black', 4],
    ['3', 'red', 5],
    ['3', 'black', 6],
    ['4', 'red', 7],
    ['4', 'black', 8],
    ['5', 'red', 9],
    ['5', 'black', 10],
    ['6', 'red', 11],
    ['6', 'black', 12],
    ['7', 'red', 13],
    ['7', 'black', 14],
    ['8', 'red', 15],
    ['8', 'black', 16],
    ['9', 'red', 17],
    ['9', 'black', 18],
    ['10', 'red', 19],
    ['10', 'black', 20],
    ['11', 'red', 21],
    ['11', 'black', 22],
    ['12', 'red', 23],
    ['12', 'black', 24],
    ['13', 'red', 25],
    ['13', 'black', 26],
    ['1', 'red', 27],
    ['1', 'black', 28],
    ['2', 'red', 29],
    ['2', 'black', 30],
    ['3', 'red', 31],
    ['3', 'black', 32],
    ['4', 'red', 33],
    ['4', 'black', 34],
    ['5', 'red', 35],
    ['5', 'black', 36],
    ['6', 'red', 37],
    ['6', 'black', 38],
    ['7', 'red', 39],
    ['7', 'black', 40],
    ['8', 'red', 41],
    ['8', 'black', 42],
    ['9', 'red', 43],
    ['9', 'black', 44],
    ['10', 'red', 45],
    ['10', 'black', 46],
    ['11', 'red', 47],
    ['11', 'black', 48],
    ['12', 'red', 49],
    ['12', 'black', 50],
    ['13', 'red', 51],
    ['13', 'black', 52]
]


@socketio.on('connect')
def connect():
    if clients['p1'] and clients['p2']:
        emit('rejection', room=request.sid)
        return 

    if request.sid in clients.values():
        return
        
    if not clients['p1']:
        clients['p1'] = request.sid
    
    elif not clients['p2']:
        clients['p2'] = request.sid
    
    if clients['p1'] and clients['p2']:
        emit("connection", broadcast = True)
    
@socketio.on('disconnect')
def disconnect():
    if request.sid not in clients.values():
        return
    emit('disconnection', broadcast = True)
    if request.sid == clients['p1']:
        clients['p1'] = clients['p2']
        clients['p2'] = None
    
    else:
        clients['p2'] = None
    print('disconnected')

@socketio.on('card')
def handleCard(number):
    emit('card-res', number)

@socketio.on('reset')
#FIXME: make sure reset signal send from one of connected players
def reset_game():
    #prevents double reset
    if request.sid != clients['p1']:
        return
    deck_tops = [{'color': '', 'number': ''}, {'color': '', 'number': ''}]
    cards = [card for card in total_cards]
    shuffle(cards)
    player1_cards = cards[:21]
    player2_cards = cards[21:42]
    sides = cards[42:]
    emit('reset', player1_cards, room=clients['p1'])
    emit('reset', player2_cards, room=clients['p2'])
    emit('tops-change', deck_tops, broadcast=True)
    emit('side-deck', [sides[:5], sides[5:]], broadcast = True)

@socketio.on('place')
def changeTops(element):
    elements = element
    emit('tops-change', elements, broadcast = True)

@socketio.on('update-opp')
#optimize this, creates slight delays
def updateOppHandLength(hand_length):
    opp = [0] * hand_length
    if request.sid == clients['p1']:
        emit('update-opp', opp, room = clients['p2'])
    
    elif request.sid == clients['p2']:
        emit('update-opp', opp, room=clients['p1'])

    else:
        return

@socketio.on('noplace')
def noPlace():
    if request.sid == clients['p1']:
        emit('noplace', room = clients['p2'])
    
    elif request.sid == clients['p2']:
        emit('noplace', room = clients['p1'])
    
    else:
        return

@socketio.on('noplacemutual')
def noPlaceMutual (sides):
    if len(sides[0]) == 0 or len(sides[1]) == 0:
        emit('winner', 'tie', broadcast = True)
    left = sides[0]
    right = sides[1]
    deck_tops = [{'color': left[0][1], 'number': left[0][0]}, {'color': right[0][1], 'number': right[0][0]}]
    emit('tops-change', deck_tops, broadcast = True)
    emit('side-deck', [left[1:], right[1:]], broadcast = True)


@socketio.on('winner')
def winner():
    if request.sid == clients['p1']:
        emit('winner', True, room = clients['p1'])
        emit('winner', False, room = clients['p2'])
    elif request.sid == clients['p2']:
        emit('winner', False, room = clients['p1'])
        emit('winner', True, room = clients['p2'])
    else:
        return

@socketio.on('resetplace')
def canPlace():
    print('success')
    if request.sid == clients['p1']:
        emit('resetplace', room = clients['p2'])
        
    if request.sid == clients['p2']:
        emit('resetplace', room = clients['p1'])

if __name__ == '__main__':
    socketio.run(app)