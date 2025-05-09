import re
import sys
from .constants import CHANNELS, CHANNEL_QUEUES
from .errors import ConfigFileError

def validate_config_file(config_file):
    """验证配置文件的有效性"""
    channel_names = set()
    channel_ports = set()

    try:
        with open(config_file, 'r') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                # 如果检测到空行，返回 False
                if not line:
                    return False

                parts = line.split()
                if len(parts) < 4:
                    return False

                if len(parts) > 4:
                    return False

                if parts[0] != "channel":
                    return False

                channel_name = parts[1]
                if not re.match(r'^[a-zA-Z0-9_]+$', channel_name):
                    return False

                if channel_name in channel_names:
                    return False

                try:
                    port = int(parts[2])
                    if port < 1024 or port > 65535:
                        return False
                except ValueError:
                    return False

                if port in channel_ports:
                    return False

                try:
                    capacity = int(parts[3])
                    if capacity < 1 or capacity > 8:
                        return False
                except ValueError:
                    return False

                channel_names.add(channel_name)
                channel_ports.add(port)

                # 添加频道配置
                CHANNELS[channel_name] = {
                    'port': port,
                    'capacity': capacity,
                    'clients': []
                }
                CHANNEL_QUEUES[channel_name] = []

            # 确保至少有一个频道
            if not CHANNELS:
                return False

            return True
    except Exception as e:
        return False