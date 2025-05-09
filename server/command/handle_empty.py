from ..constants import CLIENTS, CHANNELS, CHANNEL_QUEUES
from ..utils import check_waiting_queue


def handle_empty(command_parts):
    """处理 /empty 命令"""
    if len(command_parts) < 2:
        print("Invalid /empty command. Usage: /empty <channel_name>")
        return

    channel_name = command_parts[1]

    # 检查频道是否存在
    if channel_name not in CHANNELS:
        print(f"[Server Message] Channel \"{channel_name}\" does not exist.")
        return

    clients_to_remove = []
    # 找出要移除的客户端
    for client_socket in CHANNELS[channel_name]['clients']:
        clients_to_remove.append(client_socket)

    # 通知频道内所有客户端并关闭连接
    for client_socket in clients_to_remove:
        try:
            client_socket.send("[Server Message] You are removed from the channel.\n".encode())
            client_socket.close()
            # 从客户端列表中移除该客户端
            if client_socket in CLIENTS:
                del CLIENTS[client_socket]
        except Exception as e:
            print(f"Error handling client during empty: {e}")

    # 清空频道内的客户端列表
    CHANNELS[channel_name]['clients'] = []

    print(f"[Server Message] \"{channel_name}\" has been emptied.")

    # 检查等待队列，将等待的客户端按 FIFO 顺序加入频道
    check_waiting_queue(channel_name)