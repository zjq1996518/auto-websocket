import os
from collections import defaultdict


class AutoWrite(object):

    def __init__(self, admin_uid, websocket_list):

        self._repeat_check(websocket_list)

        import_package = 'import json\n' \
                         'from flask import Flask\n' \
                         'from flask_sockets import Sockets\n' \
                         'from flask_cors import *\n'

        create_app = '\n\napp = Flask(__name__)\n' \
                     'CORS(app, supports_credentials=True)\n' \
                     'socket = Sockets(app)\n'

        set_admin_id = f"ADMIN_ID = '{admin_uid}'\n"

        set_socket_dict = self._set_socket_dict(websocket_list)

        self.code_file_path = os.path.join(os.path.dirname(__file__), 'websocket.py')
        with open(self.code_file_path, 'w+', encoding='utf-8') as f:
            # 导入socket
            f.write(import_package)
            f.write(create_app)
            f.write(set_admin_id)
            f.write(set_socket_dict)

        # 创建websocket
        for websocket in websocket_list:
            self.write_func(**websocket)

    def write_func(self, route_path, func_name, uid_name='user_id', notify_id_name='notify_id',
                   message_name='message', success_message='success', fail_message='fail'):
        """
        :param route_path: 路由
        :param func_name: 函数名
        :param uid_name: 全局id名字
        :param notify_id_name: 通知的id参数名
        :param message_name: 消息名字
        :param success_message: 通知成功消息
        :param fail_message: 通知失败消息
        :return:
        """
        code = '\n'*2
        code += f"@socket.route('{route_path}')\n"
        code += f'def {func_name}(ws):\n'
        code += ' '*4 + f"{uid_name} = ''\n"
        code += ' '*4 + 'if not ws.closed:\n'
        code += ' '*8 + f'{uid_name} = ws.receive()\n'
        code += ' '*8 + f"socket_dict['{func_name}'][{uid_name}] = ws\n"
        code += ' '*8 + f"print(f\"{{socket_dict['{func_name}']}}\")\n"
        code += ' '*4 + 'while not ws.closed:\n'
        code += ' '*8 + 'data = ws.receive()\n'
        code += ' '*8 + 'if not ws.closed:\n'
        code += ' '*12 + 'data = json.loads(data)\n'

        code += ' '*12 + f"if isinstance(data['{notify_id_name}'], list):\n"
        code += ' '*16 + f"for notify_id in data['{notify_id_name}']:\n"
        code += ' '*20 + f"notify_user = socket_dict['{func_name}'].get({notify_id_name})\n"
        code += ' '*20 + 'if notify_user is not None:\n'
        code += ' '*24 + f"notify_user.send(f\"{{data['{uid_name}']}}: {{data['{message_name}']}}\")\n"
        code += ' '*24 + f"ws.send('{success_message}')\n"
        code += ' '*24 + f"ws.send('{fail_message}')\n"

        code += ' '*12 + 'else:\n'
        code += ' '*16 + f"notify_user = socket_dict['{func_name}'].get(data['{notify_id_name}'])\n"
        code += ' '*16 + 'if notify_user is not None:\n'
        code += ' '*20 + f"notify_user.send(f\"{{data['{uid_name}']}}: {{data['{message_name}']}}\")\n"
        code += ' '*20 + f"ws.send('{success_message}')\n"
        code += ' '*16 + 'else:\n'
        code += ' '*20 + f"ws.send('{fail_message}')\n"
        code += ' '*4 + f"del socket_dict['{func_name}'][{uid_name}]\n"
        with open(self.code_file_path, 'a+', encoding='utf-8') as f:
            f.write(code)

    @staticmethod
    def _set_socket_dict(websocket_list):
        socket_dict_count = len(websocket_list)

        set_socket_dict = 'socket_dict = {'
        for i in range(socket_dict_count):
            set_socket_dict += f"'{websocket_list[i]['func_name']}': {{}}"
            if i != socket_dict_count - 1:
                set_socket_dict += ', '
        set_socket_dict += '}\n'

        return set_socket_dict

    @staticmethod
    def _repeat_check(websocket_list):
        check_dict = defaultdict(int)
        for websocket in websocket_list:

            check_dict[websocket['func_name']] += 1
            if check_dict[websocket['func_name']] == 2:
                raise NameError('func_name重复，请检查配置文件')

            check_dict[websocket['route_path']] += 1
            if check_dict[websocket['route_path']] == 2:
                raise NameError('route_path重复，请检查配置文件')
