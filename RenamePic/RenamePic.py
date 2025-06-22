import os
import sys
import glob
from datetime import datetime

def rename_images_to_numbers(directory):
    # 支持的图片扩展名
    extensions = ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.bmp', '*.tiff', '*.webp']
    image_files = []
    
    # 收集所有匹配的图片文件
    for ext in extensions:
        image_files.extend(glob.glob(os.path.join(directory, ext), recursive=False))
    
    # 检查是否找到图片文件
    if not image_files:
        print(f"在目录 {directory} 中未找到图片文件")
        return
    
    # 获取文件修改时间并排序
    files_with_mtime = []
    for file_path in image_files:
        mtime = os.path.getmtime(file_path)
        files_with_mtime.append((file_path, mtime))
    
    # 按修改时间排序（从旧到新）
    files_with_mtime.sort(key=lambda x: x[1])
    
    # 重命名文件为数字序列
    for index, (file_path, _) in enumerate(files_with_mtime, start=1):
        # 获取文件扩展名
        filename = os.path.basename(file_path)
        ext = os.path.splitext(filename)[1].lower()  # 统一转换为小写扩展名
        
        # 构建新文件名 (纯数字)
        new_filename = f"{index}{ext}"
        new_path = os.path.join(directory, new_filename)
        
        # 处理文件名冲突（避免覆盖）
        temp_path = file_path
        conflict_counter = 1
        while os.path.exists(new_path) or new_path == file_path:
            # 如果新文件名与现有文件冲突，使用临时名称
            temp_name = f"temp_{conflict_counter}_{filename}"
            temp_path = os.path.join(directory, temp_name)
            os.rename(file_path, temp_path)
            conflict_counter += 1
            file_path = temp_path
        
        # 执行重命名
        os.rename(file_path, new_path)
        print(f"重命名: {filename} -> {new_filename}")

if __name__ == "__main__":
    # 检查命令行参数
    if len(sys.argv) != 2:
        print("使用方法: python main.py [目录]")
        print("示例: python main.py /path/to/your/images")
        sys.exit(1)
    
    target_dir = sys.argv[1]
    
    # 检查目录是否存在
    if not os.path.isdir(target_dir):
        print(f"错误: 目录 '{target_dir}' 不存在")
        sys.exit(1)
    
    # 执行重命名操作
    rename_images_to_numbers(target_dir)
    print(f"已完成! 共重命名 {len(os.listdir(target_dir))} 张图片。")