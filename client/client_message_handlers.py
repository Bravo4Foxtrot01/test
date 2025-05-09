import os
import sys
from .client_constants import (
    CMD_JOIN, CMD_QUIT, CMD_SEND,
    CMD_LIST, CMD_WHISPER, CMD_SWITCH, CMD_BROADCAST
)
from .client_error_code import EXIT_CHANNEL_HAS_SAME_USERNAME_2, \
    EXIT_SERVER_CONNECTION_CLOSED_8
from .client_utils import check_file_exists, get_file_content

# Global flag for exit condition
should_exit = False


def receive_messages(client_socket, username, client_state):
    """
    Handle messages received from the server.
    """
    global should_exit
    server_closed = False

    while not should_exit:
        try:
            data = client_socket.recv(1024)
            if not data:
                print("Error: server connection closed.",
                      file=sys.stderr)
                server_closed = True
                break

            data = data.decode()
            for line in data.splitlines():
                # Process received messages
                if line.startswith("ERROR: Username already exists"):
                    channel_name = client_state.get("current_channel",
                                                    "")
                    print(
                        f'[Server Message] Channel "{channel_name}" already has user {username}.')
                    client_socket.close()
                    should_exit = True
                    break
                elif line.startswith("JOIN_SUCCESS"):
                    parts = line.split('"')
                    if len(parts) > 1:
                        channel_name = parts[1]
                        client_state["current_channel"] = channel_name
                        print(
                            f'[Server Message] You have joined the channel "{channel_name}".')
                elif line.startswith("[Server Message]"):
                    print(line)
                else:
                    print(line)
        except Exception as e:
            print(f"Error receiving message: {e}")
            server_closed = True
            break

    if server_closed:
        client_state['server_closed'] = True
        sys.exit(EXIT_SERVER_CONNECTION_CLOSED_8)


def send_messages(client_socket, username, client_state):
    """
    Handle sending messages and commands to the server.
    """
    global should_exit
    print(
        f"Welcome to chatclient, {username}.")  # Required welcome message

    while not should_exit:
        try:
            message = input()

            if message.startswith(CMD_JOIN):
                handle_join(client_socket, message, client_state)
            elif message == CMD_QUIT:
                handle_quit(client_socket)
                should_exit = True
                break
            elif message.startswith(CMD_SEND):
                handle_send(client_socket, message)
            elif message.startswith(CMD_LIST):
                handle_list(client_socket)
            elif message.startswith(CMD_WHISPER):
                handle_whisper(client_socket, message)
            elif message.startswith(CMD_SWITCH):
                handle_switch(client_socket, message, client_state)
            else:
                handle_default_message(client_socket, message,
                                       client_state)
        except EOFError:
            handle_quit(client_socket)
            should_exit = True
            break


def handle_join(client_socket, message, client_state):
    """
    Handle the join command: /join channel_name
    """
    parts = message.split()
    if len(parts) != 2:
        print("Error: /join requires a channel name")
        return

    channel = parts[1]
    client_state["current_channel"] = channel
    client_socket.send(
        f"{message} {client_state['username']}\n".encode())


def handle_quit(client_socket):
    """
    Handle the quit command: /quit
    """
    client_socket.send(f"{CMD_QUIT}\n".encode())
    client_socket.close()
    sys.exit(0)  # Exit with status code 0 for normal termination


def handle_send(client_socket, message):
    """
    Handle the send command: /send target_client_username file_path
    """
    parts = message.split(maxsplit=2)
    if len(parts) != 3:
        print(
            "[Server Message] Usage: /send target_client_username file_path")
        return

    target_username = parts[1]
    file_path = parts[2]

    # Check if file exists before sending request to server
    if not check_file_exists(file_path):
        print(f'[Server Message] "{file_path}" does not exist.')
        return

    # Send command to the server
    client_socket.send(f"{message}\n".encode())

    # Prepare and send file data
    file_data = get_file_content(file_path)
    file_size = len(file_data)

    client_socket.send(
        f"SEND_FILE_INFO {target_username} {os.path.basename(file_path)} {file_size}\n".encode())
    client_socket.sendall(file_data)


def handle_list(client_socket):
    """
    Handle the list command: /list
    """
    client_socket.send(f"{CMD_LIST}\n".encode())


def handle_whisper(client_socket, message):
    """
    Handle the whisper command: /whisper receiver_client_username chat_message
    """
    parts = message.split(maxsplit=2)
    if len(parts) < 3:
        print(
            "Error: /whisper requires a receiver_username and a chat_message")
        return

    client_socket.send(f"{message}\n".encode())


def handle_switch(client_socket, message, client_state):
    """
    Handle the switch command: /switch channel_name
    """
    parts = message.split()
    if len(parts) != 2:
        print("Error: /switch requires a channel name")
        return

    client_socket.send(f"{message}\n".encode())


def handle_default_message(client_socket, message, client_state):
    """
    Handle regular message (not a command)
    """
    if client_state.get("current_channel"):
        client_socket.send(f"{CMD_BROADCAST} {message}\n".encode())
    else:
        print(
            "Unknown command. Available commands: /join, /broadcast, /leave, /quit, /send, /list, /whisper, /switch")