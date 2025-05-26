import os
import uuid
import sys

def rename_png_files(directory='.'):
    # 获取所有PNG文件
    png_files = [f for f in os.listdir(directory) if f.lower().endswith('.png')]
    total_files = len(png_files)
    
    if total_files == 0:
        print("目录中没有PNG文件")
        return

    # 检查是否已经是连续编号
    expected_files = {f"{i}.png" for i in range(1, total_files+1)}
    actual_files = set(png_files)
    
    if actual_files == expected_files:
        print("文件已经是连续编号，无需修改")
        return

    # 需要重命名操作
    # 先按文件名排序，可根据需求改为按修改时间排序
    sorted_files = sorted(png_files, key=lambda x: x.lower())

    # 第一步：重命名到临时文件
    temp_files = []
    for filename in sorted_files:
        src = os.path.join(directory, filename)
        while True:
            temp_name = f"temp_{uuid.uuid4().hex}.png"
            dst = os.path.join(directory, temp_name)
            if not os.path.exists(dst):
                break
        os.rename(src, dst)
        temp_files.append(dst)

    # 第二步：重命名为目标编号
    for index, temp_path in enumerate(temp_files, 1):
        new_name = os.path.join(directory, f"{index}.png")
        os.rename(temp_path, new_name)

    print(f"成功重命名 {total_files} 个文件")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target_dir = sys.argv[1]
        rename_png_files(target_dir)
    else:
        rename_png_files()