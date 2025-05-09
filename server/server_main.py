import socket
import sys
import threading
import time
from .constants import SERVER_SOCKETS, CHANNELS, CLIENTS
from .handlers import handle_client
from .utils import check_afk_clients
from .test_command import handle_listall
from .command.handle_kick import handle_kick
from .command.handle_empty import handle_empty
from .command.handle_mute import handle_mute  # 导入 handle_mute 函数

DEBUG = False
EXIT_FLAG = False
# 用于标记是否有服务器启动失败
STARTUP_FAILED = False
# 存储成功启动的服务器信息
SUCCESSFUL_SERVERS = []


def start_channel_server(channel_name, port, capacity):
    global EXIT_FLAG, STARTUP_FAILED
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_address = ('localhost', port)

        server_socket.bind(server_address)
        server_socket.listen(10)
        SERVER_SOCKETS[channel_name] = server_socket
        SUCCESSFUL_SERVERS.append((channel_name, port))
        print(
            f'Channel "{channel_name}" is created on port {port}, with a capacity of {capacity}.')

        while True:
            client_socket, client_address = server_socket.accept()



            client_thread = threading.Thread(target=handle_client,
                                             args=(client_socket,
                                                   client_address))
            client_thread.daemon = True
            client_thread.start()

    except (OSError, socket.error) as e:
        print(f"Error: unable to listen on port {port}. Details: {e}",
              file=sys.stderr)
        EXIT_FLAG = True
        STARTUP_FAILED = True
    except Exception as e:
        print(
            f"Unexpected error in start_channel_server for {channel_name}: {e}",
            file=sys.stderr)
        EXIT_FLAG = True
        STARTUP_FAILED = True
    finally:
        if channel_name in SERVER_SOCKETS:
            SERVER_SOCKETS[channel_name].close()
            del SERVER_SOCKETS[channel_name]


def afk_checker():
    """定期检查AFK客户端的后台线程"""
    while True:
        try:
            check_afk_clients()
        except Exception as e:
            print(f"Error in AFK checker: {e}")
        time.sleep(5)  # 每5秒检查一次


def handle_server_commands():
    """处理服务端的命令输入"""
    while True:
        command = input("")
        if command.startswith("/"):
            print("你输入了一个命令")
            if command == "/ll" and DEBUG:
                # 这里可以添加 /ll 命令的具体处理逻辑
                print("测试命令，显示所有频道信息和在线用户")
                print(handle_listall())
            elif command == "/shutdown":
                channel_names = list(SERVER_SOCKETS.keys())
                for channel_name in channel_names:
                    server_socket = SERVER_SOCKETS.get(channel_name)
                    if server_socket:
                        try:
                            server_socket.close()
                        except Exception as e:
                            print(
                                f"Error closing server socket for {channel_name}: {e}")
                    # 检查键是否存在于字典中
                    if channel_name in SERVER_SOCKETS:
                        del SERVER_SOCKETS[channel_name]
                print("[Server Message] Server shuts down.")
                break
            elif command.startswith("/kick"):
                command_parts = command.split()
                if len(command_parts) < 3:
                    print(
                        "Invalid /kick command. Usage: /kick <channel_name> <client_username>")
                else:
                    # 模拟一个客户端套接字，这里可以根据实际情况修改
                    # 由于是服务端命令，没有实际的客户端套接字，我们可以传入 None
                    handle_kick(None, command_parts)
            elif command.startswith("/empty"):
                command_parts = command.split()
                handle_empty(command_parts)
            elif command.startswith("/mute"):
                command_parts = command.split()
                handle_mute(command_parts)
            else:
                print(f"未知命令: {command}")


def start_all_servers():
    global EXIT_FLAG, STARTUP_FAILED, SUCCESSFUL_SERVERS
    if len(CHANNELS) == 0:
        print("No channels to start. Exiting...")
        sys.exit(6)

    afk_thread = threading.Thread(target=afk_checker)
    afk_thread.daemon = True
    afk_thread.start()

    channel_threads = []
    for channel_name, channel_info in CHANNELS.items():
        thread = threading.Thread(target=start_channel_server,
                                  args=(channel_name, channel_info['port'], channel_info['capacity']))
        thread.daemon = True
        channel_threads.append(thread)
        thread.start()

    # 检查是否有服务器启动失败
    time.sleep(1)  # 稍微等待一下，确保异常信息能被正确捕获
    if not STARTUP_FAILED:
        print('Welcome to chatserver.')
    else:
        sys.exit(6)

    command_thread = threading.Thread(target=handle_server_commands)
    command_thread.daemon = False
    command_thread.start()

    while not EXIT_FLAG:
        pass

    sys.exit(6)
