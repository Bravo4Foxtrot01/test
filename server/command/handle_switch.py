import time
from ..constants import CLIENTS, CHANNELS, CHANNEL_QUEUES, MUTE_LIST
from ..utils import check_waiting_queue


def handle_switch(client_socket, client_address, command_parts,
                  username, channel):
    if len(command_parts) < 2:
        print(f"Invalid /switch command from {client_address}: {command_parts}")
        client_socket.send("ERROR: Invalid /switch command. Usage: /switch <channel>".encode())
        return channel

    # 更新最后活动时间
    if channel:
        CLIENTS[client_socket] = (username, channel, time.time())

    new_channel_name = command_parts[1]

    if new_channel_name not in CHANNELS:
        client_socket.send(
            f'[Server Message] Channel "{new_channel_name}" does not exist.'.encode())
        return channel

    # 检查目标频道中是否存在相同用户名的用户
    for sock in CHANNELS[new_channel_name]['clients']:
        if CLIENTS.get(sock) and CLIENTS[sock][0] == username:
            client_socket.send(
                f'[Server Message] Channel "{new_channel_name}" already has user {username}.\n'.encode())
            return channel

    # 如果客户端当前在一个频道中，先离开该频道
    if channel and channel in CHANNELS and client_socket in CHANNELS[channel]['clients']:
        CHANNELS[channel]['clients'].remove(client_socket)
        if client_socket in MUTE_LIST:
            del MUTE_LIST[client_socket]
        # 通知频道内其他用户
        message = f"[Server Message] {username} has left the channel."
        for client in CHANNELS[channel]['clients']:
            client.send(message.encode())
        print(
            f"{username} has left channel {channel}")
        # 检查等待队列，如果有客户端在等待，让他们加入
        check_waiting_queue(channel)

    # 尝试加入新频道
    if len(CHANNELS[new_channel_name]['clients']) >= \
            CHANNELS[new_channel_name]['capacity']:
        # 将客户端放入等待队列
        CHANNEL_QUEUES[new_channel_name].append(client_socket)
        CLIENTS[client_socket] = (
            username, None, time.time())
        client_socket.send(
            f"[Server Message] You are in the waiting queue for channel {new_channel_name}".encode())
        return None
    else:
        # 将客户端添加到新频道
        CHANNELS[new_channel_name]['clients'].append(client_socket)
        CLIENTS[client_socket] = (
            username, new_channel_name, time.time())
        print(
            f"{username} has joined channel {new_channel_name} from {client_address}")
        # 通知客户端已加入新频道
        client_socket.send(
            f'[Server Message] You have joined the channel "{new_channel_name}".'.encode())
        # 通知频道内其他用户
        message = f"[Server Message] {username} has joined {new_channel_name}."
        for client in CHANNELS[new_channel_name]['clients']:
            if client != client_socket:
                client.send(message.encode())
        return new_channel_name