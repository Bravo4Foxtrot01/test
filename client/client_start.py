import socket
import threading
import sys
import signal
from .client_utils import check_arguments
from .client_message_handlers import send_messages, receive_messages, should_exit
from .client_error_code import (
    EXIT_SUCCESS_0,
    EXIT_CHANNEL_HAS_SAME_USERNAME_2,
    EXIT_UNABLE_TO_CREATE_SOCKET_7,
    EXIT_SERVER_CONNECTION_CLOSED_8
)

def create_socket_connection(host, port):
    """
    Create and connect a socket to the server.
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Try to set SO_NOSIGPIPE on macOS
    if hasattr(socket, 'SO_NOSIGPIPE'):
        try:
            client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_NOSIGPIPE, 1)
        except OSError as e:
            print(f"Warning: Failed to set SO_NOSIGPIPE: {e}", file=sys.stderr)

    # Ignore SIGPIPE on Unix/Linux systems
    if hasattr(signal, "SIGPIPE"):
        signal.signal(signal.SIGPIPE, signal.SIG_IGN)

    server_address = (host, port)
    try:
        client_socket.connect(server_address)
        return client_socket
    except (ConnectionRefusedError, OSError):
        print(f"Error: Unable to connect to port {port}.", file=sys.stderr)
        sys.exit(EXIT_UNABLE_TO_CREATE_SOCKET_7)

def start_client():
    """
    Main client function that initiates the connection and message handling.
    """
    port, username = check_arguments()
    client_socket = create_socket_connection('localhost', port)

    # Create client state dictionary
    client_state = {
        "current_channel": None,
        "username": username,
        "server_closed": False
    }

    # Create and start message handling threads
    receive_thread = threading.Thread(
        target=receive_messages,
        args=(client_socket, username, client_state)
    )

    send_thread = threading.Thread(
        target=send_messages,
        args=(client_socket, username, client_state)
    )

    receive_thread.daemon = True
    send_thread.daemon = True

    receive_thread.start()
    send_thread.start()

    # Wait for threads to complete or exit when should_exit is True
    try:
        while receive_thread.is_alive() and send_thread.is_alive() and not should_exit:
            receive_thread.join(0.1)  # Check every 100ms
    except KeyboardInterrupt:
        # Handle Ctrl+C as a /quit command
        sys.exit(EXIT_SUCCESS_0)

    # Set exit status based on condition
    if client_state.get('server_closed', False):
        sys.exit(EXIT_SERVER_CONNECTION_CLOSED_8)
    else:
        sys.exit(EXIT_CHANNEL_HAS_SAME_USERNAME_2)