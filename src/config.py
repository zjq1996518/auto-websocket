# 管理员uid 用于通知信息
ADMIN_NAME = 'test123'

# 服务端口
PORT = 5000

# 创建websocket服务的字典表
WEBSOCKET_LIST = [
    {
        # websocket路由地址 全局唯一即可必须以/开头
        'route_path': '/test1',
        # 函数，全局唯一即可
        'func_name': 'test1',
        # 全局用户id变量名 默认为user_id,这里定义什么，前端就传递什么
        'uid_name': 'user_id',
        # 前端websocket发送数据时通知的uid变量名，这里定义什么，前端就传递什么
        'notify_id_name': 'notify_id',
        # 前端websocket发送数据时消息变量名，这里定义什么，前端就传递什么
        'message_name': 'message',
        # 消息发送成功时，管理员获得的通知
        'success_message': '消息发送成功',
        # 消息发送失败时，管理员获得的通知
        'fail_message': '消息发送失败'
    },
    {
        # websocket路由地址 全局唯一即可
        'route_path': '/test2',
        # 方法名，全局唯一即可
        'func_name': 'test2',
        # 全局用户id变量名 默认为user_id,这里定义什么，前端就传递什么
        'uid_name': 'user_id',
        # 前端websocket发送数据时通知的uid变量名，这里定义什么，前端就传递什么
        'notify_id_name': 'notify_id',
        # 前端websocket发送数据时消息变量名，这里定义什么，前端就传递什么
        'message_name': 'message',
        # 消息发送成功时，管理员获得的通知
        'success_message': 'success',
        # 消息发送失败时，管理员获得的通知
        'fail_message': 'fail'
    },

]

