import time
from ..constants import CLIENTS, CHANNELS, CHANNEL_QUEUES


def handle_join(client_socket, client_address, command_parts):
    """处理 /join 命令"""
    if len(command_parts) < 3:
        print(f"Invalid /join command from {client_address}: {command_parts}")
        client_socket.send("ERROR: Invalid /join command. Usage: /join <channel> <username>".encode())
        return None, None

    channel_name = command_parts[1]
    username = command_parts[2]

    # 检查频道是否存在
    if channel_name not in CHANNELS:
        print(
            f"Channel {channel_name} does not exist, client {client_address} tried to join")
        client_socket.send(
            f"ERROR: Channel {channel_name} does not exist".encode())
        return None, None

    # 检查用户名是否在指定频道中已存在
    username_exists = False
    for sock in CHANNELS[channel_name]['clients']:
        if CLIENTS.get(sock) and CLIENTS[sock][0] == username:
            username_exists = True
            break

    if username_exists:
        print(
            f"Username {username} already exists in channel {channel_name} for {client_address}")
        client_socket.send("ERROR: Username already exists".encode())
        return None, None

    # 检查等待队列中是否存在相同用户名的用户
    for sock in CHANNEL_QUEUES.get(channel_name, []):
        if CLIENTS.get(sock) and CLIENTS[sock][0] == username:
            print(
                f"Username {username} already exists in the waiting queue for channel {channel_name} for {client_address}")
            client_socket.send("ERROR: Username already exists".encode())
            return None, None

    # 检查频道容量
    if len(CHANNELS[channel_name]['clients']) >= \
            CHANNELS[channel_name]['capacity']:
        # 获取排队人数
        queue_length = len(CHANNEL_QUEUES.get(channel_name, []))
        # 将客户端放入等待队列
        CHANNEL_QUEUES[channel_name].append(client_socket)
        CLIENTS[client_socket] = (
            username, None, time.time())  # None 表示用户在队列中，不在频道中
        # 发送包含排队人数的消息
        client_socket.send(
            f"[Server Message] You are in the waiting queue and there are {queue_length} user(s) ahead of you.".encode())
        return username, None  # 用户名已确定，但频道未加入（在队列中）
    else:
        # 将客户端添加到频道
        CHANNELS[channel_name]['clients'].append(client_socket)
        CLIENTS[client_socket] = (username, channel_name, time.time())

        # 修改服务端打印格式，添加引号
        print(
            f'[Server Message] {username} has joined the channel "{channel_name}".')

        # 向当前客户端发送加入成功的确认
        client_socket.send(
            f'[Server Message] You have joined the channel "{channel_name}".'.encode())

        # 通知频道内其他用户（保持原有格式）
        message = f"[Server Message] {username} has joined {channel_name}."
        for client in CHANNELS[channel_name]['clients']:
            if client != client_socket:
                client.send(message.encode())
        return username, channel_name