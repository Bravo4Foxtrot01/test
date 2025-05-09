#!/usr/bin/env python3
import sys
from client.client_error_code import EXIT_SUCCESS_0
from client.client_start import start_client

if __name__ == "__main__":
    try:
        start_client()
    except KeyboardInterrupt:
        print("Client shutting down...")
        sys.exit(EXIT_SUCCESS_0)