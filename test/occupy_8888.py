import socket
import threading
import tkinter as tk
from tkinter import messagebox

# 占用8888和7777端口的代码

class PortListenerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("我的端口监听器")  # 更明确的窗口标题
        self.sockets = []
        self.listening_ports = [7777, 8888, 9999]  # 监听的端口列表
        self.is_listening = True

        self.create_widgets()
        self.start_listening()

    def create_widgets(self):
        self.exit_button = tk.Button(self.root, text="退出", command=self.on_exit)
        self.exit_button.pack(pady=20)

    def start_listening(self):
        for port in self.listening_ports:
            thread = threading.Thread(target=self.listen_on_port, args=(port,))
            thread.daemon = True
            thread.start()
            print(f"[我的监听器] 开始监听端口 {port}...")  # 更明确的输出

    def listen_on_port(self, port):
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 设置 SO_REUSEADDR
            server_socket.bind(('localhost', port))
            server_socket.listen(1)
            self.sockets.append(server_socket)
            print(f"[我的监听器] 成功绑定并监听端口 {port}")  # 更明确的输出
            while self.is_listening:
                conn, addr = server_socket.accept()
                print(f"[我的监听器] 接收到来自 {addr} 的连接 (端口 {port})")  # 更明确的输出
                conn.close()
        except OSError as e:
            print(f"[我的监听器] 端口 {port} 绑定失败: {e}")  # 更明确的输出
        finally:
            if 'server_socket' in locals():
                server_socket.close()
                print(f"[我的监听器] 端口 {port} 已关闭")  # 更明确的输出

    def on_exit(self):
        self.is_listening = False
        print("[我的监听器] 尝试关闭所有监听端口...")  # 更明确的输出
        for sock in self.sockets:
            try:
                sock.shutdown(socket.SHUT_RDWR)
                sock.close()
            except OSError as e:
                print(f"[我的监听器] 关闭套接字时发生错误: {e}")  # 更明确的输出
        self.root.destroy()
        print("[我的监听器] 应用程序已退出")  # 更明确的输出

if __name__ == "__main__":
    root = tk.Tk()
    app = PortListenerApp(root)
    root.mainloop()