import json
from flask import Flask
from flask_sockets import Sockets


app = Flask(__name__)
socket = Sockets(app)
ADMIN_ID = 'test123'
socket_dict = {'test1': {}, 'test2': {}}


@socket.route('/test1')
def test1(ws):
    user_id = ''
    if not ws.closed:
        user_id = ws.receive()
        socket_dict['test1'][user_id] = ws
    while not ws.closed:
        data = ws.receive()
        if not ws.closed:
            data = json.loads(data)
            if data['user_id'] == ADMIN_ID:
                notify_user = socket_dict['test1'].get(data['notify_id'])
                if notify_user is not None:
                    notify_user.send(data['message'])
                    ws.send('success')
                else:
                    ws.send('fail')
    del socket_dict['test1'][user_id]


@socket.route('/test2')
def test2(ws):
    user_id = ''
    if not ws.closed:
        user_id = ws.receive()
        socket_dict['test2'][user_id] = ws
    while not ws.closed:
        data = ws.receive()
        if not ws.closed:
            data = json.loads(data)
            if data['user_id'] == ADMIN_ID:
                notify_user = socket_dict['test2'].get(data['notify_id'])
                if notify_user is not None:
                    notify_user.send(data['message'])
                    ws.send('success')
                else:
                    ws.send('fail')
    del socket_dict['test2'][user_id]
