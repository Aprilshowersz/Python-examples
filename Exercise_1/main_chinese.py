import os

# 输入文件和输出文件的路径
input_file_path = "Exercise_1/file_to_read.txt"
output_file_path = "Exercise_1/result.txt"

# 打开输入文件进行读取
with open(input_file_path, "r") as input_file:
    # 读取文件的内容
    content = input_file.read()
    
    # 统计 "terrible" 的出现次数
    terrible_count = content.lower().count("terrible")
    
    # 初始化一个空列表来存储修改后的单词
    modified_words = []
    
    # 遍历单词
    replace_flag = False
    for word in content.split():
        # 检查单词是否是 "terrible"
        if word.lower() == "terrible":
            replace_flag = not replace_flag  # 切换替换状态
            if replace_flag:
                # 偶数次出现，替换为 "pathetic"
                modified_word = "pathetic"
            else:
                # 奇数次出现，替换为 "marvellous"
                modified_word = "marvellous"
        else:
            modified_word = word
        
        # 将修改后的单词添加到列表中
        modified_words.append(modified_word)
    
    # 将修改后的单词重新连接成字符串
    modified_content = " ".join(modified_words)

# 获取输出文件的文件夹路径
output_folder = os.path.dirname(output_file_path)

# 如果输出文件夹不存在，创建它
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 打开结果文件进行写入
with open(output_file_path, "w") as output_file:
    # 将修改后的内容写入结果文件
    output_file.write(modified_content)

# 显示 "terrible" 的总计数
print("总计 'terrible' 出现次数：", terrible_count)
