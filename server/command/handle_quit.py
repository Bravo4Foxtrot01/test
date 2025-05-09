import time

from ..constants import CLIENTS, CHANNELS, CHANNEL_QUEUES
from ..utils import check_waiting_queue

def handle_quit(client_socket, username, channel):
    """处理 /quit 命令"""
    if channel:
        # 如果客户端在频道中
        if channel in CHANNELS and client_socket in CHANNELS[channel]['clients']:
            CHANNELS[channel]['clients'].remove(client_socket)

            # 客户端仍然连接，但不在任何频道中
            CLIENTS[client_socket] = (username, None, time.time())

            # 检查等待队列
            check_waiting_queue(channel)

            # 通知频道内其他用户
            message = f"[Server Message] {username} has left the channel."
            for client in CHANNELS.get(channel, {}).get('clients', []):
                client.send(message.encode())
            print(message)
    else:
        # 如果客户端在队列中
        for queue_name, queue in CHANNEL_QUEUES.items():
            if client_socket in queue:
                queue.remove(client_socket)
                message = f"[Server Message] {username} has left the channel."
                print(message)

    # 从客户端列表中移除
    if client_socket in CLIENTS:
        del CLIENTS[client_socket]

    # 关闭套接字
    client_socket.close()