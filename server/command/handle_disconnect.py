from ..constants import CLIENTS, CHANNELS, CHANNEL_QUEUES, MUTE_LIST
from ..utils import check_waiting_queue


def handle_disconnect(client_socket, username, channel):
    try:
        # 从客户端列表中移除
        if client_socket in CLIENTS:
            del CLIENTS[client_socket]

        # 如果在某个频道中，从频道中移除
        if channel and channel in CHANNELS and client_socket in CHANNELS[channel]['clients']:
            CHANNELS[channel]['clients'].remove(client_socket)
            if client_socket in MUTE_LIST:
                del MUTE_LIST[client_socket]
            # 通知频道内其他用户
            message = f"[Server Message] {username} has disconnected."
            for client in CHANNELS[channel]['clients']:
                client.send(message.encode())
            print(
                f"{username} has disconnected from channel {channel}")
            # 检查等待队列
            check_waiting_queue(channel)

        # 如果在某个等待队列中，从队列中移除
        for queue_name, queue in CHANNEL_QUEUES.items():
            if client_socket in queue:
                queue.remove(client_socket)
                print(
                    f"{username} has been removed from waiting queue for {queue_name}")

        # 关闭套接字
        client_socket.close()
    except Exception as e:
        print(f"Error during disconnect handling: {e}")
