import subprocess
import unittest

from client.client_error_code import EXIT_INVALID_ARGS_3, \
    EXIT_UNABLE_TO_CREATE_SOCKET_7


class TestChatClient(unittest.TestCase):
    def run_chatclient(self, args, test_description):
        print(test_description)
        result = subprocess.run(['python3', '/Users/zjc/PycharmProject/UQCourses/2025Sem1/COMS3200_Computer_Networks_I/assignment/code/chatclient.py'] + args,
                                capture_output=True, text=True)
        print(f"标准输出: {result.stdout}")
        print(f"标准错误输出: {result.stderr}")
        return result
# ----- Command Line Arguments中的测试用例

    # No arguments are present (i.e., there is no port_number argument).
    def test_missing_username(self):
        test_description = "缺少用户名参数"
        result = self.run_chatclient(['9999'], test_description)
        self.assertEqual(result.returncode, EXIT_INVALID_ARGS_3)
        self.assertEqual(result.stderr.strip(), "Usage: chatclient port_number client_username")

    # An unexpected argument is present (i.e., too many arguments).
    def test_too_many_arguments(self):
        test_description = "参数过多"
        result = self.run_chatclient(['test01', '9999', 'test02'], test_description)
        self.assertEqual(result.returncode, EXIT_INVALID_ARGS_3)
        self.assertEqual(result.stderr.strip(), "Usage: chatclient port_number client_username")

    # Any argument is an empty string.
    # test_empty_port和test_empty_username是为了覆盖空字符串的情况
    def test_empty_port(self):
        test_description = "端口号为空字符串"
        result = self.run_chatclient(['', 'test_user'],
                                     test_description)
        self.assertEqual(result.returncode, EXIT_INVALID_ARGS_3)
        self.assertEqual(result.stderr.strip(),
                         "Usage: chatclient port_number client_username")


    def test_empty_username(self):
        test_description = "用户名为空字符串"
        result = self.run_chatclient(['9999', ''], test_description)
        self.assertEqual(result.returncode, EXIT_INVALID_ARGS_3)
        self.assertEqual(result.stderr.strip(),
                         "Usage: chatclient port_number client_username")



    def test_missing_port(self):
        test_description = "缺少端口参数"
        result = self.run_chatclient(['test01'], test_description)
        self.assertEqual(result.returncode, EXIT_INVALID_ARGS_3)
        self.assertEqual(result.stderr.strip(), "Usage: chatclient port_number client_username")
    def test_no_arguments(self):
        test_description = "没有传递参数"
        result = self.run_chatclient([], test_description)
        self.assertEqual(result.returncode, EXIT_INVALID_ARGS_3)
        self.assertEqual(result.stderr.strip(), "Usage: chatclient port_number client_username")

    # 下面几个检查时关于端口号合法性的
    # Checking whether the port_number is a valid port is not part of the usage checking (other than checking
    # that the value is not empty). The validity of the port is checked after command line validity as described next.
    def test_port_less_than_1024(self):
        test_description = "端口号小于1024"
        result = self.run_chatclient(['1023', 'test01'], test_description)
        self.assertEqual(result.returncode, EXIT_INVALID_ARGS_3)
        self.assertEqual(result.stderr.strip(), "Usage: chatclient port_number client_username")

    def test_port_greater_than_65535(self):
        test_description = "端口号大于65535"
        result = self.run_chatclient(['65536', 'test01'], test_description)
        self.assertEqual(result.returncode, EXIT_INVALID_ARGS_3)
        self.assertEqual(result.stderr.strip(), "Usage: chatclient port_number client_username")

    def test_port_not_integer(self):
        test_description = "端口参数不是整数"
        port = "abc"  # 非整数端口参数
        username = "test_user"
        result = self.run_chatclient([port, username], test_description)
        expected_error_msg = f"Error: Unable to connect to port {port}."
        self.assertEqual(result.returncode, 7)
        self.assertEqual(result.stderr.strip(), expected_error_msg)

    # ---------------Client Port Checking 中的测试用例

    # 端口号占用
    # If the port_number argument is not an integer or chatclient is unable to create a socket and connect to the
    # server on the specified port of host localhost, it shall print the following message (terminated by a newline) to stderr and exit with exit status 7:

    # def test_unable_to_connect(self):
    #     test_description = "无法连接到指定端口（假设端口已被占用或不可用）"
    #     port = "9999"  # 假设这个端口不可用
    #     username = "test_user"
    #     result = self.run_chatclient([port, username], test_description)
    #     expected_error_msg = f"Error: Unable to connect to port {port}."
    #     self.assertEqual(result.returncode, EXIT_UNABLE_TO_CREATE_SOCKET)
    #     self.assertEqual(result.stderr.strip(), expected_error_msg)

    # ---------------Client Username Checking 中的测试用例

    #频道或者队列有相同用户名的情况下，需要以2退出，这个目前是手动测试的

    # ---------------Client Runtime Behaviour 测试用例

    # 成功加入频道提示，Welcome to chatclient, client username.
    # 手动检查

    # 成功加入频道提示，注意保留双引号 [Server Message] You have joined the channel "channel_name".
    # 手动检查

    # 排队的提示检查 [Server Message] You are in the waiting queue and there are X user(s) ahead of you.
    # 手动检查
    # todo 这里的问题是，x的数量如何确认，需要对比一下服务端

    # Client - Handling Standard Input

    # 正常发消息
    # 手动检查

    # 输入命令的检查
    # 不能有前导空格，     /join是不行的
    # 结尾也不能有空格 /quit    也不行
    # 允许多参数之间的空格，例如/join             a1

    # send命令，#todo 未实现

    # quit命令 检查频道内其余的人和服务端都会打印[Server Message] client_username has left the channel.
    # 如果是排队中quit的话，只有服务端打印，频道内的别人不会看到。
    # todo quit的客户端的退出值应该是0

    # list命令
    # 检查频道名称，容量和排队数量是否正确

    # whisper 命令
    # 私信不存在的人。[Server Messagel client_username is not in the channel.

    # 收到私信的人会显示[sender_client_ username whispers to youl chat_message

    # 发送私信的人会显示[sender_client_username whispers to receiver_ client_username] chat_message
    # 服务端会显示[sender_client_username whispers to receiver_ client_username] chat_message

    # switch 命令
    # 要切换的频道不存在，打印[Server Message] Channel "channel_name" does not exist.

    # 如果目标频道已经存在了与自己同名的用户，则自己会打印[Server Message] Channel "channel_name" already has user client_username.
    # 注意，此时，自己应该留在频道中
    # todo，客户端应该打印，服务端应该不打印，目前可能有点问题。

    # ---------------Other Client Requirements中的测试用例
    # 客户端检测服务端断开之后会有提示Error: server connection closed.
    # todo 这里客户端会以8退出，之后需要测试














    def test_username_with_space(self):
        test_description = "用户名包含空格"
        result = self.run_chatclient(['9999', 'test 01'], test_description)
        self.assertEqual(result.returncode, EXIT_INVALID_ARGS_3)
        self.assertEqual(result.stderr.strip(), "Usage: chatclient port_number client_username")




if __name__ == '__main__':
    print("测试错误的启动客户端参数，以下所有的输出都应该是chatclient port_number client_username")
    unittest.main()