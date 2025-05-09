import time

from ..constants import CLIENTS, CHANNELS, CHANNEL_QUEUES
from ..utils import check_waiting_queue

def handle_kick(client_socket, command_parts):
    """处理 /kick 命令"""
    if len(command_parts) < 3:
        print(f"Invalid /kick command: {command_parts}")
        return

    channel_name = command_parts[1]
    client_username = command_parts[2]

    # 检查频道是否存在
    if channel_name not in CHANNELS:
        print(f"[Server Message] Channel \"{channel_name}\" does not exist.")
        return

    # 检查客户端是否在频道中
    target_client = None
    for sock, (user, chan, _) in CLIENTS.items():
        if user == client_username and chan == channel_name:
            target_client = sock
            break

    if not target_client:
        print(f"[Server Message] {client_username} is not in the channel.")
        return

    # 执行踢人操作
    # 从频道中移除客户端
    CHANNELS[channel_name]['clients'].remove(target_client)
    # 客户端不再属于任何频道
    CLIENTS[target_client] = (client_username, None, time.time())

    # 通知被踢客户端
    target_client.send("[Server Message] You are removed from the channel.\n".encode())
    # 关闭与被踢客户端的连接
    target_client.close()

    print(f"[Server Message] Kicked {client_username}.")

    # 通知频道内其他用户
    message = f"[Server Message] {client_username} has left the channel.\n"
    for client in CHANNELS[channel_name]['clients']:
        client.send(message.encode())

    # 检查等待队列
    check_waiting_queue(channel_name)