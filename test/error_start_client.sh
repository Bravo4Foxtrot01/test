echo "测试错误的启动客户端参数，以下所有的输出都应该是chatclient port_number client_username"

# 缺少用户名
echo "缺少用户名参数"
python3 /Users/zjc/PycharmProject/UQCourses/2025Sem1/COMS3200_Computer_Networks_I/assignment/code/chatclient.py 9999
echo "Exit status: $?"

# 缺少端口
echo "缺少端口参数"
python3 /Users/zjc/PycharmProject/UQCourses/2025Sem1/COMS3200_Computer_Networks_I/assignment/code/chatclient.py test01
echo "Exit status: $?"

# 参数过多
echo "参数过多"
python3 /Users/zjc/PycharmProject/UQCourses/2025Sem1/COMS3200_Computer_Networks_I/assignment/code/chatclient.py test01 9999 test02
echo "Exit status: $?"

# 没有传递参数
echo "没有传递参数"
python3 /Users/zjc/PycharmProject/UQCourses/2025Sem1/COMS3200_Computer_Networks_I/assignment/code/chatclient.py
echo "Exit status: $?"

# 用户名空字符串
echo "用户名为空字符串"
python3 /Users/zjc/PycharmProject/UQCourses/2025Sem1/COMS3200_Computer_Networks_I/assignment/code/chatclient.py 9999 ""
echo "Exit status: $?"

# 用户名包含空格
echo "用户名包含空格"
python3 /Users/zjc/PycharmProject/UQCourses/2025Sem1/COMS3200_Computer_Networks_I/assignment/code/chatclient.py 9999 "test 01"
echo "Exit status: $?"

# 端口号边界测试，小于1024
echo "端口号小于1024"
python3 /Users/zjc/PycharmProject/UQCourses/2025Sem1/COMS3200_Computer_Networks_I/assignment/code/chatclient.py 1023 "test01"
echo "Exit status: $?"

# 端口号边界测试，大于65535
echo "端口号大于65535"
python3 /Users/zjc/PycharmProject/UQCourses/2025Sem1/COMS3200_Computer_Networks_I/assignment/code/chatclient.py 65536 "test01"
echo "Exit status: $?"


echo "端口号占用"
python3 /Users/zjc/PycharmProject/UQCourses/2025Sem1/COMS3200_Computer_Networks_I/assignment/code/chatserver.py 100 /Users/zjc/PycharmProject/UQCourses/2025Sem1/COMS3200_Computer_Networks_I/assignment/code/config_file
echo "Exit status: $?"