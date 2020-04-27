from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
from src.auto_write import AutoWrite
from src.config import *
from src.logger import get_logger, PATH

auto_write = AutoWrite(ADMIN_NAME, WEBSOCKET_LIST)


logger = get_logger(f'{PATH}/gevent.log')
err_logger = get_logger(f'{PATH}/gevent-err.log')


if __name__ == '__main__':
    from src.websocket import app
    from src.view import *

    ssl_parm = {}
    if SSL_KEY_PATH != '':
        ssl_parm = {
            'keyfile': SSL_KEY_PATH,
            'certfile': SSL_CRT_PATH
        }
    server = WSGIServer(('0.0.0.0', PORT), backlog=1024, log=logger, error_log=err_logger, application=app, handler_class=WebSocketHandler, **ssl_parm)
    print("服务已启动")
    server.serve_forever()
