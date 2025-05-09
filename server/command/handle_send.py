import time
from ..constants import CLIENTS, MUTE_LIST


def handle_send(client_socket, client_address, command_parts,
                username, channel):
    if client_socket in MUTE_LIST:
        start_time, mute_duration = MUTE_LIST[client_socket]
        remaining_time = mute_duration - (time.time() - start_time)
        if remaining_time > 0:
            client_socket.send(f"[Server Message] You are still in mute for {remaining_time:.0f} seconds.\n".encode())
            return

    if not channel:
        print(
            f"{client_address} tried to send a file without joining a channel")
        client_socket.send(
            "ERROR: You must join a channel first".encode())
        return

    if len(command_parts) != 3:
        print(f"Invalid /send command from {client_address}: {command_parts}")
        client_socket.send("ERROR: Invalid /send command. Usage: /send <user> <file_path>".encode())
        return

    # 更新最后活动时间
    CLIENTS[client_socket] = (username, channel, time.time())

    target_username = command_parts[1]
    file_path = command_parts[2]

    # 服务端需要等待客户端发送 SEND_FILE_INFO 命令
    client_socket.send("READY_FOR_FILE_INFO".encode())
    return True, {'target_username': target_username, 'file_path': file_path}
