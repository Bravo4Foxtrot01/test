import time
from .constants import CLIENTS, CHANNELS, CHANNEL_QUEUES
from .utils import check_waiting_queue
from .server_command import (CMD_QUIT, CMD_LIST, CMD_JOIN,
                             CMD_WHISPER, CMD_SEND, CMD_SWITCH,
                             CMD_BROADCAST, CMD_KICK)
from .command.handle_join import handle_join
from .command.handle_broadcast import handle_broadcast
from .command.handle_send import handle_send
from .command.handle_list import handle_list
from .command.handle_whisper import handle_whisper
from .command.handle_switch import handle_switch
from .command.handle_disconnect import handle_disconnect
from .command.handle_quit import handle_quit

def handle_client(client_socket, client_address):
    """处理客户端连接和通信"""
    username = None
    channel = None
    receiving_file_info = False
    file_info = {}
    receiving_file_data = False
    file_data_buffer = b''



    try:
        while True:
            data = client_socket.recv(4096).decode()
            if not data:
                print(f"Client {client_address} disconnected")
                break

            lines = data.splitlines()
            for line in lines:
                command_parts = line.split()
                if not command_parts:
                    continue

                command = command_parts[0]

                # print(f"Received command '{command}' from {client_address}: {command_parts}")

                if command == CMD_JOIN:  # '/join'
                    username, channel = handle_join(client_socket,
                                                    client_address,
                                                    command_parts)

                elif command == CMD_SEND:  # '/send'
                    receiving_file_info, file_info = handle_send(client_socket, client_address,
                                                                 command_parts, username, channel)
                    if receiving_file_info:
                        receiving_file_data = True
                        file_data_buffer = b''
                elif receiving_file_data and command == 'SEND_FILE_INFO':
                    if len(command_parts) == 4:
                        file_info['file_name'] = command_parts[2]
                        file_info['file_size'] = int(command_parts[3])
                        client_socket.send("READY_TO_RECEIVE_FILE".encode())
                        # 准备接收文件内容
                    else:
                        client_socket.send("ERROR: Invalid file info format".encode())
                        receiving_file_data = False
                        file_info = {}
                elif receiving_file_data and file_info.get('file_size'):
                    remaining = file_info['file_size'] - len(file_data_buffer)
                    file_chunk = client_socket.recv(min(4096, remaining))
                    if not file_chunk:
                        receiving_file_data = False
                        file_info = {}
                        file_data_buffer = b''
                        print(f"Error receiving file chunk from {client_address}")
                        continue
                    file_data_buffer += file_chunk
                    if len(file_data_buffer) == file_info['file_size']:
                        target_client = None
                        for sock, (user, chan, _) in CLIENTS.items():
                            if user == file_info['target_username'] and chan == channel:
                                target_client = sock
                                break
                        if target_client:
                            try:
                                target_client.send(f"FILE_TRANSFER {username} {file_info['file_name']} {file_info['file_size']}\n".encode())
                                target_client.sendall(file_data_buffer)
                                client_socket.send(f"[Server Message] Forwarded \"{file_info['file_name']}\" to {file_info['target_username']}".encode())
                                print(f"[Server Message] Forwarded \"{file_info['file_name']}\" from {username} to {file_info['target_username']}")
                            except Exception as e:
                                client_socket.send(f"[Server Message] Error forwarding file: {e}".encode())
                        else:
                            client_socket.send(f"[Server Message] User {file_info['target_username']} not found in channel.".encode())
                        receiving_file_data = False
                        file_info = {}
                        file_data_buffer = b''
                elif command == CMD_LIST:  # '/list'
                    handle_list(client_socket)
                elif command == CMD_WHISPER:  # '/whisper'
                    handle_whisper(client_socket, client_address,
                                   command_parts, username, channel)
                elif command == CMD_SWITCH:  # '/switch'
                    channel = handle_switch(client_socket, client_address,
                                            command_parts, username,
                                            channel)
                elif command == CMD_QUIT:  # '/quit'
                    handle_quit(client_socket, username, channel)
                    break
                elif command == CMD_BROADCAST:  # '/broadcast'
                    handle_broadcast(client_socket, client_address, command_parts, username, channel)
                else:
                    print(
                        f"Unknown command '{command}' from {client_address}")
                    if client_socket in CLIENTS:
                        old_username, old_channel, _ = CLIENTS[
                            client_socket]
                        CLIENTS[client_socket] = (
                            old_username, old_channel, time.time())

    except Exception as e:
        print(f"Error handling client {client_address}: {e}")

    finally:
        if username:
            handle_disconnect(client_socket, username, channel)
        else:
            try:
                client_socket.close()
            except:
                pass