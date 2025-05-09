import subprocess
import random
import string
import time

def generate_random_username(length=8):
    """生成指定长度的随机用户名"""
    characters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def start_client(port, username):
    """在后台运行 chatclient.py 脚本"""
    command = f"python3 chatclient.py {port} {username}"
    process = subprocess.Popen(command, shell=True)
    print(f"Started client: {username} (PID: {process.pid})")
    return process

if __name__ == "__main__":
    server_port = 9999  # 指定连接的端口
    num_users = 5      # 指定要生成的随机用户数量
    processes = []

    print(f"Generating and starting {num_users} random users...")

    for i in range(num_users):
        username = generate_random_username()
        process = start_client(server_port, username)
        processes.append(process)
        time.sleep(0.5)  # 可选：稍微延迟启动，避免瞬间大量连接

    input("Press Enter to terminate all clients...")
    for process in processes:
        process.terminate()
        process.wait()
        print(f"Terminated client with PID: {process.pid}")

    print("All clients terminated.")