# Command Line Arguments 命令行参数规定

# Client Port Checking 脚本启动端口检查

# Client Username Checking 客户端名称检查

# Client Runtime Behaviour 运行行为

- 成功启动客户端之后打印消息Welcome to chatclient, client_username.
  注意，这个时候只是成功启动，但是并没有连接频道或者什么的会成功

- 成功加入频道之后会打印[Server Message] You have joined the channel "channel_name". 

- 频道人满了之后会打印排队消息，[Server Message] You are in the waiting queue and there are X user(s) ahead of you. 

- 客户端会发送用户输入的消息到服务器，也会接受服务器的消息打印在客户端。需要用哦那个多线程处理这个

# Client – Handling Standard Input

- 首先就是公屏消息broadcast messages。服务端和频道内的其他人都能看到这条消息。

- 命令错误的话，就需要打印正确的命令格式

- 处于排队中的client只有quit，list和switch命令可以用

## 客户端命令

### /send target_client_username file_path
- 不在同一个频道的用户不能发送文件，[Server Message] target_client_username is not in the channel.

- 文件不存在提示[Server Message] "file_path" does not exist.

- 如果频道中既不包括这个用户，也不包括文件。需要展示**两个错误信息** 优先检查用户是否存在

- 文件发送成功后，另外一个用户会把它保存在自己的当前目录并且提示[Server Message] 
 发送者显示Sent "file_path" to target_client_username.
 服务端显示[Server Message] sender_client_username sent "file_path" to target_client_username.

- 文件大小的要求是File sizes up to 232 − 1 = 4294967295 bytes are to be supported.
- 文件名不能包含空格
- 接受的文件会进行覆盖
- 保存不成功的话，发送者会打印[Server Message] Failed to send "file_path" to sender_client_username

### quit
- 退出之后，服务端和其它用户会打印下面的日志 [Server Message] client_username has left the channel.
- 但是，如果是排队情况下退出，那么只有服务端会打印[Server Message] client_username has left the channel.
- 退出的客户端不会打印消息，并且以 exit status 0进行退出
- 这个还不清楚是什么意思EOF on the client's stdin, should be treated the same as if the / quit command was entered. Termination
by signal will be treated similarly (other than the client exit status - there is no need for the client to
catch SIGINT, SIGQUIT, etc.).

### list
- 这里打印的频道就是config_file定义的内容，格式如下
[Channel] channel_name channel_port Capacity: current /channel_capacity, in_queue

### /whisper receiver_client_username chat_message
- 频道中不包含这个用户会打印[Server Message] client_username is not in the channel.

- 收到私信的人会以下面格式展示消息[sender_client_username whispers to you] chat_message

- 私信成功后，服务端会展示[sender_client_username whispers to receiver_client_username ] chat_message

- 私信是允许给自己的It is permissible for a client to /whisper to itself. 212

### /switch channel_name

- 切换到不存在的频道会显示[Server Message] Channel "channel_name" does not exist. 

- 如果另一个频道中存在和自己同名的人，那么客户端会打印[Server Message] Channel "channel_name" already has user client_username.

- 频道存在并且没有同名的情况下，会先离开当前频道。如果这个人确实是在频道中，而不是在频道中排队，那么频道中的其它人会收到消息
[Server Message] client_username has left the channel. 并且此时，服务端也会打印**同一个消息**。

### Client – Handling Messages from Server
- 客户端需要打印收到服务端的消息

- 如果服务端崩溃了，需要打印Error: server connection closed. 并且exit with status 8. 

- 这个暂时还是不是很理解Your client must not exit abnormally due to SIGPIPE. A SIGPIPE when writing to the server will be
treated as the connection to the server being closed - see line 246.




