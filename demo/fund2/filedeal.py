# coding:utf-8
import os
 
# 1, 内置函数 open() 是python读写文件的基本函数，可以生成文件对象，可以创建也可以操作文件的读写
# 用法 open(path, mode) ; path 文件路径，mode 操作模式； 返回值是文件对象
# file = open('E:\\aa.txt', 'w')
# 使用open()函数对E盘下的aa.txt文件执行写入操作，并赋值给file
 
# 文件操作的写入模式
# 模式	介绍
# w	创建文件(w为写入的操作，当文件不存在时，则会创建文件；已创建文件，则内容会被覆盖)
# w+	创建文件并读取文件
# wb	二进制形式创建文件(与 w 的功能相同，只不过 web 的写入类型为 byte )
# wb+	二进制形式创建或追加内容（如果文件存在不会覆盖原本的内容，而是以 byte 类型进行追加）
# a	在文件中追加内容，如果没有该文件则会创建文件
# a+	读写模式追加（同样是追加内容，只不过赋予了读取的功能）
# ab+	二进制形式读写追加（可以追加并读取 byte 类型的模式）
 
# 2, 文件对象的写入操作：
# 2.1 write(str) 写入信息
# 2.2 writelines(列表) 批量写入，参数是列表，列表内内必须是字符串
# 2.3 close()  关闭并保存文件
 
# 小练习
curr_dir = os.getcwd()
curr_dir
file = open(curr_dir + '\FundList.xls', 'w+', encoding='utf-8')
file.write("wwwwwwww")
file.close()
 
join_file = os.path.join(os.getcwd(), 'a.txt')
file2 = open(join_file, 'ab+')
bytes_con = "我们都是龙的传人"
encode_con = bytes_con.encode(encoding='UTF-8')
list_con = [encode_con]
file2.writelines(list_con)
file2.close()
 
 
# 自动创建包的函数
def create_package(path):
    if os.path.exists(path):
        raise Exception(f'{path}已经存在不可创建')
    else:
        os.makedirs(path)
        init_path = os.path.join(path, '__init__.py')
        init_file = open(init_path, 'w', encoding='utf-8')
        init_file.write('# coding:utf-8\n')
        init_file.close()
 
 
if __name__ == '__main__':
    curr_path = os.getcwd()
    print("curr_path:")
    print(curr_path)
    path = os.path.join(curr_path, 'test_package')
    create_package(path)