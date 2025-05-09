import time
from ..constants import CLIENTS, CHANNELS, CHANNEL_QUEUES

def handle_list(client_socket):
    """处理 /list 命令"""
    if client_socket in CLIENTS:
        # 更新最后活动时间
        username, channel, _ = CLIENTS[client_socket]
        CLIENTS[client_socket] = (username, channel, time.time())

    response = ""
    for channel_name, channel_info in CHANNELS.items():
        current = len(channel_info['clients'])
        capacity = channel_info['capacity']
        queue_length = len(CHANNEL_QUEUES.get(channel_name, []))
        port = channel_info['port']
        response += f"[Channel] {channel_name} {port} Capacity: {current}/{capacity}, Queue: {queue_length}\n"

    if not response:
        response = "[Server Message] No active channels."

    client_socket.send(response.encode())