import time
from ..constants import CLIENTS, MUTE_LIST


def handle_whisper(client_socket, client_address, command_parts,
                   username, channel):
    if client_socket in MUTE_LIST:
        start_time, mute_duration = MUTE_LIST[client_socket]
        remaining_time = mute_duration - (time.time() - start_time)
        if remaining_time > 0:
            client_socket.send(f"[Server Message] You are still in mute for {remaining_time:.0f} seconds.\n".encode())
            return

    if not channel:
        print(
            f"{client_address} tried to whisper without joining a channel")
        client_socket.send(
            "ERROR: You must join a channel first".encode())
        return

    if len(command_parts) < 3:
        print(f"Invalid /whisper command from {client_address}: {command_parts}")
        client_socket.send("ERROR: Invalid /whisper command. Usage: /whisper <user> <message>".encode())
        return

    # 更新最后活动时间
    CLIENTS[client_socket] = (username, channel, time.time())

    receiver_username = command_parts[1]
    chat_message = " ".join(command_parts[2:])

    receiver_found = False
    for sock, (user, chan, _) in CLIENTS.items():
        if user == receiver_username and chan == channel:
            receiver_found = True
            sock.send(
                f"[{username} whispers to you] {chat_message}\n".encode())
            client_socket.send(
                f"[{username} whispers to {receiver_username}] {chat_message}\n".encode())
            # 新增：在服务端打印私聊信息
            print(f"{username} whispers to {receiver_username} {chat_message}")
            break

    if not receiver_found:
        client_socket.send(
            f"[Server Message] {receiver_username} is not in the channel.\n".encode())