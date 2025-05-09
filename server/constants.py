# 存储所有连接的客户端，格式为 {client_socket: (username, channel, last_active_time)}
CLIENTS = {}
# 存储所有的频道，格式为 {channel_name: {'port': port, 'capacity': capacity, 'clients': [client_socket]}}
CHANNELS = {}
# 存储所有频道的等待队列，格式为 {channel_name: [client_socket]}
CHANNEL_QUEUES = {}
# 存储所有的服务器套接字，以便关闭
SERVER_SOCKETS = {}
# AFK 时间（秒）
AFK_TIME = 100  # 默认值为 100 秒

# 新增：静音列表，键为客户端socket，值为 (开始时间, 持续时长)
MUTE_LIST = {}