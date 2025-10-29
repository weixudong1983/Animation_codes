import os
import sys
import glob

# words_per_second越大,速度越快
def generate_lrc_file(input_file, words_per_second=5):
    """
    根据输入的文本文件内容生成带递增编号的LRC格式字幕文件
    :param input_file: 输入的文件名（包含路径）
    :param words_per_second: 每秒语速，默认4个字
    """
    # 确保输入文件存在
    if not os.path.isfile(input_file):
        print(f"错误：文件 {input_file} 不存在。")
        return

    # 读取输入文件内容
    with open(input_file, "r", encoding="utf-8") as file:
        text = file.read()

    # 分割文本为行
    lines = text.split("\n")
    #去掉空行,如果一行为空则跳过
    #lines = [line for line in lines if line.strip() != ""]
    lrc_content = []
    current_time = 0.0  # 当前时间，单位：秒

    for line in lines:
        num_words = len(line)
        # 如果是时间戳，直接忽略   
        # 计算当前行的字数和时间
        if line == "" :
            current_time += 2  # 空行间隔0.5秒
            continue
        
        duration = num_words / words_per_second  # 每行文本的时长
        minutes, seconds = divmod(int(current_time), 60)
        milliseconds = int((current_time - int(current_time)) * 100)
        
        # 格式化时间戳 [mm:ss.xx]
        timestamp = f"[{minutes:02}:{seconds:02}.{milliseconds:02}]"
        lrc_content.append(f"{timestamp} {line}")
        
        # 累加时间
        current_time += duration

    # 生成带递增编号的输出文件名
    dir_name = os.path.dirname(input_file)
    base_name = os.path.basename(input_file)
    base_name_without_ext = os.path.splitext(base_name)[0]
    output_file = os.path.join(dir_name, f"{base_name_without_ext}_1.lrc")

    counter=0
    output_counter = 1
    # 遍历从1到10000的计数器
    while counter <= 10000 :
        counter += 1
        output_file = os.path.join(dir_name, f"{base_name_without_ext}_{counter}.lrc")
        if os.path.exists(output_file):
            output_counter =counter+ 1
            os.remove(output_file)

    

    # 写入LRC文件
    new_file_name = os.path.join(dir_name, f"{base_name_without_ext}_{output_counter}.lrc")
    with open(new_file_name, "w", encoding="utf-8") as file:
        file.write("\n".join(lrc_content))

    print(f"LRC字幕文件生成成功，文件名为：{new_file_name}")


# 主程序
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python generate_lrc.py <输入文件路径>")
        sys.exit(1)

    input_file = sys.argv[1]
    words_per_second = 4.5  # 可以根据需要调整语速
    if len(sys.argv) >= 3:
        try:
            words_per_second = float(sys.argv[2])
        except ValueError:
            print("语速参数无效，使用默认值 4.5 字/秒。")
    
    generate_lrc_file(input_file,words_per_second)