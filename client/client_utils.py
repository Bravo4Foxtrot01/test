import sys
import os
from .client_error_code import EXIT_INVALID_ARGS_3, \
    EXIT_UNABLE_TO_CREATE_SOCKET_7
from .client_error_message import COMMAND_LINE_ERROR_MESSAGE


def check_arguments():
    """
    Validates command line arguments for the client.

    Returns:
        tuple: (port_number, client_username) if valid
    """
    # Check correct number of arguments
    if len(sys.argv) != 3:
        print(COMMAND_LINE_ERROR_MESSAGE, file=sys.stderr)
        sys.exit(EXIT_INVALID_ARGS_3)

    port_number = sys.argv[1]
    client_username = sys.argv[2]

    # Check for empty arguments or spaces in username
    if not port_number or not client_username or " " in client_username:
        print(COMMAND_LINE_ERROR_MESSAGE, file=sys.stderr)
        sys.exit(EXIT_INVALID_ARGS_3)

    # Validate port number
    try:
        port = int(port_number)
        if port < 1024 or port > 65535:
            print(COMMAND_LINE_ERROR_MESSAGE, file=sys.stderr)
            sys.exit(EXIT_INVALID_ARGS_3)
        return port, client_username
    except ValueError:
        print(f"Error: Unable to connect to port {port_number}.",
              file=sys.stderr)
        sys.exit(EXIT_UNABLE_TO_CREATE_SOCKET_7)


def check_file_exists(file_path):
    """
    Check if a file exists at the given path.

    Args:
        file_path (str): Path to the file

    Returns:
        bool: True if file exists, False otherwise
    """
    return os.path.isfile(file_path)


def get_file_content(file_path):
    """
    Read and return the content of a file.

    Args:
        file_path (str): Path to the file

    Returns:
        bytes: Content of the file in binary format
    """
    with open(file_path, 'rb') as file:
        return file.read()