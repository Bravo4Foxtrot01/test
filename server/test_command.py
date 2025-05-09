from .constants import CHANNELS, CLIENTS

def handle_listall():
    """处理 LISTALL 命令，返回所有频道、容量和用户信息的字符串"""
    response = ""
    for channel_name, channel_info in CHANNELS.items():
        capacity = channel_info['capacity']
        response += f"[Channel] {channel_name} Capacity: {capacity}\n"
        clients_in_channel = []
        for sock, (username, chan, _) in CLIENTS.items():
            if chan == channel_name:
                clients_in_channel.append(username)
        response += f"  Users: {', '.join(clients_in_channel) if clients_in_channel else 'No users'}\n"

    if not response:
        response = "[Server Message] No active channels."

    return response