import json
from geventwebsocket import WebSocketError
from src.logger import get_logger
from .config import WEBSOCKET_LIST


def save_ws(ws, func_name, logger, socket_dict):

    user_id = ws.receive()
    if isinstance(user_id, str):
        temp_user = socket_dict[func_name].get(user_id)
        if temp_user is not None and not temp_user.closed:
            temp_user.send('您已在其他地方登陆')
            temp_user.close()

        socket_dict[func_name][user_id] = ws
        logger.info(socket_dict[func_name])

    return user_id


def send_msg(ws, socket_dict, websocket_config):

    notify_id_name = websocket_config['notify_id_name']
    path = websocket_config['func_name']
    message_name = websocket_config['message_name']
    success_message = websocket_config['success_message']
    fail_message = websocket_config['fail_message']
    uid_name = websocket_config['uid_name']

    data = ws.receive()
    if not ws.closed:
        data = json.loads(data)
        if isinstance(data[notify_id_name], list):
            for notify_id in data[notify_id_name]:
                notify_user = socket_dict[path].get(notify_id)
                if notify_user is not None and not notify_user.closed:
                    notify_user.send(f'{data[notify_id_name]}: {data[message_name]}')
                    ws.send(success_message)
                else:
                    ws.send(fail_message)
        else:
            notify_user = socket_dict[path].get(data[notify_id_name])
            if notify_user is not None and not notify_user.closed:
                notify_user.send(f'{data[uid_name]}: {data[message_name]}')
                ws.send(success_message)
            else:
                ws.send(fail_message)


def handle(ws, config_index, socket_dict):
    websocket_config = WEBSOCKET_LIST[config_index]

    logger = get_logger()
    user_id = save_ws(ws, websocket_config['func_name'], logger, socket_dict)

    while not ws.closed:
        try:
            send_msg(ws, socket_dict, websocket_config)

        except WebSocketError as e:
            logger.error(e)
            if not ws.closed:
                ws.send(websocket_config['fail_message'])

    save = socket_dict[websocket_config['func_name']][user_id]
    if save.closed:
        del socket_dict[websocket_config['route_path']][user_id]
