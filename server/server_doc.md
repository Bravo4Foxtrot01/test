服务端

第一步各项检查
1，进行各项检查

然后是启动服务
- 启动成功后先flush消息，Channel "channel_name" is created on port channel_port, with a capacity of 317
channel_capacity. 打印的顺序可能是不同的，因为是多线程

- 然后打印 Welcome to chatserver.

- 开始接受客户端的请求

- 客户端连接后，服务端日志打印[Server Message] client_username has joined the channel "channel_name".

- 达到上限之后开启队列服务，打印消息 [Server Message] You are in the waiting queue and there are X user(s) ahead of you.

- 等待中的客户端不应该接受到公屏信息和私信

- 等待的客户端中的/send  and /whisper会被忽略，但是可以用其它的命令

- 客户端AFK被踢出去之后，公平和服务端都会打印[Server Message] client_username went AFK in channel "channel_name".

# Server – Handling Standard Input 服务端对于自己的command和消息的处理

- 区分command和普通输入

- 对于command，要先判断参数数量是否正确。

可用命令如下


踢人命令 /kick channel_name client_username
如果此时频道不存在，则打印[Server Message] Channel "channel_name" does not exist.
如果人不在频道中（这里不检查队列，只检查频道），打印[Server Message] client_username is not in the channel.
这个检查具有优先级，如果频道也不存在，人也不存在，那么只打印[Server Message] Channel "channel_name" does not exist.

被踢出去的人，在自己的客户端内显示[Server Message] You are removed from the channel.

被踢出去的人会断开链接，但是没有消息打印。The client will exit and 399 will not print a message about the connection being closed.

服务端是会有打印的chatserver prints a message (terminated by 400 a newline) to its stdout: 401
[Server Message] Kicked client_username.

频道中的其他人是会收到这个人被踢走的消息的[Server Message] client_username has left the channel.

关闭命令  /shutdown
客户端是不知道服务端要关机的
服务端是要打印[Server Message] Server shuts down.

服务端的退出码是0  the chatserver process will exit normally with exit status 0.

禁言命令 /mute channel_name client_username duration

频道名称不存在的话打印[Server Message] Channel "channel_name" does not exist.

人如果不存在的话打印[Server Message] client_username is not in the channel.

duration必须是大于0的整数，格式不对的打印[Server Message] Invalid mute duration.

频道名称，人和时间的校验是有顺序的。如果一个错误之后，就打印，不再往后校验了。

处于禁言中的用户只能使用whisper和send命令。用户只能收到服务端的消息

禁言成功后，服务端会打印[Server Message] Muted client_username for duration seconds.
被禁言的用户会收到[Server Message] Muted client_username for duration seconds.
频道中的其它用户会收到此人被禁言的消息[Server Message] client_username has been muted for duration seconds. 456

已经被禁言的人如果想进行公屏发言，或者whisper或者send的话，会收到消息
[Server Message] You are still in mute for duration seconds.

这个应该是已经被禁言的情况下，离开后会取消禁言，重新进就可以了。
If the client leaves the channel then the mute is cancelled, even if they immediately rejoin the channel.

禁言如果没有结束的时候继续禁言，刷新新的禁言时间，而不是叠加
If a mute operation is performed on a client whilst they are muted, then the mute period is restarted with
the new duration and messages are sent as above.

重复一遍，禁言的没法发出去消息，没办法使用whiser和send，但是别的都可以用
Except broadcasting message, /whisper and /send, all other client commands are usable during the mute.

清人命令  /empty channel_name
频道不存在 [Server Message] Channel "channel_name" does not exist.

频道中的所有人都会收到消息[Server Message] You are removed from the channel.

这个理解起来稍微麻烦一点，如果所有人都被清空了，那么我该如何处理队列中排队的人呢。
Then all connection(s) in this channel will be closed. Note: this /empty command does not close the 478 connection(s) for clients waiting in the queue. Hence, the client or clients waiting in the queue of this 479 channel will be moved into the channel in the FIFO order until it reaches the channel’s capacity.












