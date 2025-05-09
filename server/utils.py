import time
from .constants import CLIENTS, CHANNELS, CHANNEL_QUEUES
import server.constants

def check_afk_clients():
    """检查并断开闲置时间过长的客户端"""
    current_time = time.time()
    to_disconnect = []

    # print("当前设置的AFK时间为:", server.constants.AFK_TIME)

    for client_socket, (
    username, channel_name, last_active_time) in list(
            CLIENTS.items()):
        if current_time - last_active_time > server.constants.AFK_TIME:
            print(
                f"User {username} in channel {channel_name} has been idle for too long, disconnecting")
            to_disconnect.append(
                (client_socket, username, channel_name))

    for client_socket, username, channel_name in to_disconnect:
        # 发送断开消息给客户端
        try:
            client_socket.send(
                f"[Server Message] You have been disconnected due to inactivity ({server.constants.AFK_TIME} seconds).".encode())
        except:
            pass

        # 处理断开连接
        from .handlers import handle_disconnect
        handle_disconnect(client_socket, username, channel_name)

        # 从队列中移除客户端并添加等待队列中的下一个客户端（如果有）
        check_waiting_queue(channel_name)


def check_waiting_queue(channel_name):
    """检查等待队列，并将等待的客户端添加到频道（如果有空间）"""
    if channel_name not in CHANNELS or channel_name not in CHANNEL_QUEUES:
        return

    channel = CHANNELS[channel_name]
    queue = CHANNEL_QUEUES[channel_name]

    while queue and len(channel['clients']) < channel['capacity']:
        # 从队列中获取下一个客户端
        client_socket = queue.pop(0)

        # 确保客户端仍然连接
        if client_socket not in CLIENTS:
            continue

        username, _, _ = CLIENTS[client_socket]

        # 将客户端添加到频道
        channel['clients'].append(client_socket)
        CLIENTS[client_socket] = (username, channel_name, time.time())

        # 通知客户端已加入频道
        try:
            client_socket.send(
                f'[Server Message] You have been moved from the waiting queue to channel "{channel_name}".'.encode())

            # 通知频道内其他用户
            message = f"{username} has joined {channel_name} from the waiting queue"
            for client in channel['clients']:
                if client != client_socket:
                    client.send(message.encode())
        except:
            # 如果发送失败，可能客户端已断开连接
            from .handlers import handle_disconnect
            handle_disconnect(client_socket, username, channel_name)