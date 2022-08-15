import re
import eventlet
eventlet.monkey_patch()
from random import shuffle
from flask import request
from flask import Flask
from flask_socketio import SocketIO
from flask_socketio import emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins = '*')

clients = {}

#
rooms = {}

#Set to hash user rooms
users = set()

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

@socketio.on('room_list')
def roomsList():
    rooms_list = list(clients.keys())
    emit('room_list', rooms_list)
    
@socketio.on('create_room')
def createRoom(num):
    clients[num] = {'p1': None, 'p2': None}

@socketio.on('join')
def connect(roomno):
    if (clients[roomno]['p1'] and clients[roomno]['p2']) or roomno not in clients.keys():
        emit('rejection', room=request.sid)
        return 

    users.add(request.sid)
    rooms[request.sid] = roomno
    if not clients[roomno]['p1']:
        clients[roomno]['p1'] = request.sid
    
    elif not clients[roomno]['p2']:
        clients[roomno]['p2'] = request.sid
    
    if clients[roomno]['p1'] and clients[roomno]['p2']:
        emit("connection", room = clients[roomno]['p1'])
        emit("connection", room = clients[roomno]['p2'])
    
@socketio.on('disconnect')
def disconnect():
    if request.sid not in users:
        return
    room = rooms[request.sid]
    users.remove(request.sid)
    del rooms[request.sid]
    if request.sid == clients[room]['p1']:
        if clients[room]['p2']:
            clients[room]['p1'] = clients[room]['p2']
            emit('disconnection', room = clients[room]['p1'])
            clients[room]['p2'] = None

        else:
            del clients[room]
    
    else:
        clients[room]['p2'] = None
        emit('disconnection', room = clients[room]['p1'])

@socketio.on('card')
def handleCard(number):
    emit('card-res', number)

@socketio.on('reset')
def reset_game(room):
    deck_tops = [{'color': '', 'number': '', 'selected': False}, {'color': '', 'number': '', 'selected': False}]
    cards = [card for card in total_cards]
    shuffle(cards)
    player1_cards = cards[:21]
    player2_cards = cards[21:42]
    sides = cards[42:]
    emit('reset', player1_cards, room=clients[room]['p1'])
    emit('reset', player2_cards, room=clients[room]['p2'])
    emit('tops-change', deck_tops, room=clients[room]['p1'])
    emit('tops-change', deck_tops, room=clients[room]['p2'])
    emit('side-deck', [sides[:5], sides[5:]], room =clients[room]['p1'])
    emit('side-deck', [sides[:5], sides[5:]], room =clients[room]['p2'])

@socketio.on('place')
def changeTops(data):
    elements = data['elements']
    room = data['room']
    if request.sid == clients[room]['p1']:
        emit('tops-change', elements, room = clients[room]['p2'])
    else:
        emit('tops-change', elements, room = clients[room]['p1'])

@socketio.on('update-opp')
#optimize this, creates slight delays
def updateOppHandLength(data):
    room = data['room']
    if request.sid == clients[room]['p1']:
        emit('update-opp', data['reduce'], room = clients[room]['p2'])
    
    elif request.sid == clients[room]['p2']:
        emit('update-opp', data['reduce'], room=clients[room]['p1'])

    else:
        return

@socketio.on('noplace')
def noPlace(room):
    if request.sid == clients[room]['p1']:
        emit('noplace', room = clients[room]['p2'])
    
    elif request.sid == clients[room]['p2']:
        emit('noplace', room = clients[room]['p1'])
    
    else:
        return

@socketio.on('noplacemutual')
def noPlaceMutual (data):
    sides = data['sides']
    room = data['room']
    if len(sides[0]) == 0 or len(sides[1]) == 0:
        emit('winner', 'tie', broadcast = True)
    left = sides[0]
    right = sides[1]
    deck_tops = [{'color': left[0][1], 'number': left[0][0], 'selected': False}, 
    {'color': right[0][1], 'number': right[0][0], 'selected': False}]
    emit('tops-change', deck_tops, room = clients[room]['p1'])
    emit('tops-change', deck_tops, room = clients[room]['p2'])
    emit('side-deck', [left[1:], right[1:]], room = clients[room]['p1'])
    emit('side-deck', [left[1:], right[1:]], room = clients[room]['p2'])


@socketio.on('winner')
def winner(room):
    if request.sid == clients[room]['p1']:
        emit('winner', True, room = clients[room]['p1'])
        emit('winner', False, room = clients[room]['p2'])
    elif request.sid == clients[room]['p2']:
        emit('winner', False, room = clients[room]['p1'])
        emit('winner', True, room = clients[room]['p2'])
    else:
        return

@socketio.on('resetplace')
def canPlace(room):
    if request.sid == clients[room]['p1']:
        emit('resetplace', room = clients[room]['p2'])
        
    if request.sid == clients[room]['p2']:
        emit('resetplace', room = clients[room]['p1'])

if __name__ == '__main__':
    socketio.run(app)
