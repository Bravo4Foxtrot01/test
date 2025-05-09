# 1 端口检查还没有做，尤其是已经被占用的端口无法启动的情况。
Server Port Checking

If chatserver is unable to create a socket and listen to the specified port, it shall print the following message
(terminated by a newline) to stderr and exit with exit status 6:
Error: unable to listen on port N.
where N should be replaced by the argument given in the configuration file. chatserver shall print this line
X number of times if there are X number of ports that chatserver cannot listen to. For example, if there are
5 channels specified in the config file, and 3 out of 5 channels have ports that chatserver cannot create a
socket and listen on, then chatserver will print this message 3 times (terminated by a new line for each time)
with each port number correspondingly. The order of the messages shall match the order in which the ports
are mentioned in the config_file.

# Client Port Checking
If the port_number argument is not an integer or chatclient is unable to create a socket and connect to the
server on the specified port of host localhost, it shall print the following message (terminated by a newline)
to stderr and exit with exit status 7:
Error: Unable to connect to port N.
where N should be replaced by the port number argument given on the command line.
这个检查有点问题，就是现在可以检查服务端的端口占用，客户端如何检查。

# a4 has joined a3 from the waiting queue
# 现在频道中的人会收到这个消息，在测试到队列的时候检查一下

