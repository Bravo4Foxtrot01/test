import time
from ..constants import CLIENTS, CHANNELS, MUTE_LIST


def handle_mute(command_parts):
    """处理 /mute 命令"""
    if len(command_parts) < 4:
        print("Invalid /mute command. Usage: /mute <channel_name> <client_username> <duration>")
        return

    channel_name = command_parts[1]
    client_username = command_parts[2]
    try:
        duration = int(command_parts[3])
        if duration <= 0:
            raise ValueError
    except (ValueError, IndexError):
        print("[Server Message] Invalid mute duration.")
        return

    if channel_name not in CHANNELS:
        print(f"[Server Message] Channel \"{channel_name}\" does not exist.")
        return

    target_client_socket = None
    for sock, (user, chan, _) in CLIENTS.items():
        if user == client_username and chan == channel_name:
            target_client_socket = sock
            break

    if not target_client_socket:
        print(f"[Server Message] {client_username} is not in the channel.")
        return

    start_time = time.time()
    MUTE_LIST[target_client_socket] = (start_time, duration)
    print(f"[Server Message] Muted {client_username} for {duration} seconds.")

    # 通知被静音的客户端
    target_client_socket.send(f"[Server Message] You have been muted for {duration} seconds.\n".encode())

    # 通知频道内其他客户端
    for client in CHANNELS[channel_name]['clients']:
        if client != target_client_socket:
            client.send(f"[Server Message] {client_username} has been muted for {duration} seconds.\n".encode())
