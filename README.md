# auto-websocket
自动创建websocket服务，目前仅支持通知发送模式

# 通过src下config文件进行配置

## 参数说明如下
```
# 管理员uid 用于通知信息
ADMIN_NAME = 'test123'

# 服务端口
PORT = 5000

# 创建websocket服务的字典表
# WEBSOCKET_LIST 中每一个dict 会启动一个websocket服务
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
        'success_message': 'success',
        # 消息发送失败时，管理员获得的通知
        'fail_message': 'fail'
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


```

# 前端如下
```
<script type="text/javascript">

function getUrlKey(key) {
    let url = location.href;
    let params = url.split('?')[1];

    if (!params) {
        return undefined;
    }

    let startIndex = params.search(`${name}/ig`);
    let endIndex = params.substring(startIndex).search(/[&]/ig);
    endIndex = endIndex === -1 ? params.length : endIndex;
    return params.substring(startIndex, endIndex).split('=')[1]

}


const socket = new WebSocket('ws://localhost:5000/ttt');
// 这里的admin_name 与 配置文件中保持一致ADMIN_NAME 
const admin_name = 'test123';

// 获取url参数
let userId = getUrlKey('user_id');

socket.onopen = () => {

    // 第一次将一个全局的uid发给服务端
    socket.send(userId);

    if (userId === admin_name) {
        // 这里的user_id设置为管理员id，notify_id设置为要通知的用户，message为通知信息，变量名与配置文件中保持一致
        socket.send(JSON.stringify({'user_id': userId, 'notify_id': '1', 'message': '管理员通知你一些消息'}));}

    };
    socket.onmessage = (ev) => {
        alert(ev.data)
    }
</script>
```

# 效果
访问自己的页面，加上参数 user_id = 1

访问自己的页面，加上参数 user_id = test123

![image](https://github.com/zjq1996518/auto-websocket/blob/master/1.jpg)

![image](https://github.com/zjq1996518/auto-websocket/blob/master/2.jpg)
