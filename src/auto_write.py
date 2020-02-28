import os
from collections import defaultdict


class AutoWrite(object):

    def __init__(self, admin_uid, websocket_list):

        self._repeat_check(websocket_list)

        import_package = 'from flask import Flask\n' \
                         'from flask_sockets import Sockets\n' \
                         'from .base import handle'

        create_app = '\n\napp = Flask(__name__)\n' \
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
        for idx, websocket in enumerate(websocket_list):
            self.write_func(idx=idx, **websocket)

    def write_func(self, route_path, func_name, idx, **args):
        """
        :param idx: 配置文件索引
        :param route_path: 路由
        :param func_name: 函数名
        :return:
        """
        code = '\n'*2
        code += f"@socket.route('{route_path}')\n"
        code += f'def {func_name}(ws):\n'
        code += ' '*4 + f'handle(ws, {idx}, socket_dict)\n'
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
