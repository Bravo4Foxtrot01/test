import time
from ..constants import CLIENTS, CHANNELS, MUTE_LIST


def handle_broadcast(client_socket, client_address, command_parts,
                     username, channel):

    if client_socket in MUTE_LIST:
        start_time, mute_duration = MUTE_LIST[client_socket]
        remaining_time = mute_duration - (time.time() - start_time)
        if remaining_time > 0:
            client_socket.send(f"[Server Message] You are still in mute for {remaining_time:.0f} seconds.\n".encode())
            return

    if not channel:
        print(
            f"{client_address} tried to send a message without joining a channel")
        client_socket.send(
            "ERROR: You must join a channel first".encode())
        return

    if len(command_parts) < 2:
        print(f"Empty /broadcast received from {client_address}")
        client_socket.send("ERROR: Empty message".encode())
        return

    # 更新最后活动时间
    CLIENTS[client_socket] = (username, channel, time.time())

    message = " ".join(command_parts[1:])
    full_message = f"[{username}] {message}"
    print(
        f"Received message from {username} in channel {channel}: {message}")

    # 发送消息给频道内的所有用户（包括发送者自己，这样发送者可以看到自己的消息）
    for client in CHANNELS[channel]['clients']:
        client.send(full_message.encode())
