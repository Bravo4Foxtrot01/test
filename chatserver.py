import signal
import sys
import server.constants  # 改为导入整个模块
from server.config import validate_config_file
from server.server_main import start_all_servers

def signal_handler(sig, frame):
    """处理SIGINT信号（Ctrl+C），安全关闭服务器"""
    print('Shutting down server safely...')
    # 这里可以添加关闭服务器套接字和客户端连接的代码
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, signal_handler)

    if len(sys.argv) < 2:
        print("Usage: chatserver [afk_time] config_file",
              file=sys.stderr)
        sys.exit(4)

    if len(sys.argv) == 2:
        config_file = sys.argv[1]
    elif len(sys.argv) == 3:
        try:
            afk_time = int(sys.argv[1])
            if afk_time < 1 or afk_time > 1000:
                print("Usage: chatserver [afk_time] config_file",
                      file=sys.stderr)
                sys.exit(4)
            server.constants.AFK_TIME = afk_time
        except ValueError:
            print("Usage: chatserver [afk_time] config_file",
                  file=sys.stderr)
            sys.exit(4)
        config_file = sys.argv[2]
    else:
        print("Usage: chatserver [afk_time] config_file",
              file=sys.stderr)
        sys.exit(4)

    if not validate_config_file(config_file):
        print("Error: Invalid configuration file.",
              file=sys.stderr)
        sys.exit(5)

    # print(f"Server starting with AFK timeout of {server.constants.AFK_TIME} seconds")

    start_all_servers()

if __name__ == "__main__":
    main()