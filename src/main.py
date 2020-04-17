from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
from src.auto_write import AutoWrite
from src.config import *

auto_write = AutoWrite(ADMIN_NAME, WEBSOCKET_LIST)

if __name__ == '__main__':
    from src.websocket import app
    from src.view import *

    ssl_parm = {}
    if SSL_KEY_PATH != '':
        ssl_parm = {
            'keyfile': SSL_KEY_PATH,
            'certfile': SSL_CRT_PATH
        }

    server = WSGIServer(('0.0.0.0', PORT), app, handler_class=WebSocketHandler, **ssl_parm)
    print("服务已启动")
    server.serve_forever()
