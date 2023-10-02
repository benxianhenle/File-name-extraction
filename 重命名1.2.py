import os
import re
from tqdm import tqdm

folder_path = r"需要处理的文件夹"
valid_extensions = (".mp3", ".mp4", ".wav")
files_to_process = [filename for filename in os.listdir(folder_path) if filename.lower().endswith(valid_extensions)]

progress_bar = tqdm(files_to_process, desc="处理进度", unit="文件")

processed_names = set()  # 用于跟踪已经处理过的文件名

for filename in progress_bar:
    match = re.search(r'《(.*?)》', filename)
    if match:
        new_name = match.group(1).strip() + os.path.splitext(filename)[1]  # 保留原始文件扩展名
        new_name = new_name.replace(" ", "_")  # 将空格替换为下划线，以防止文件名中有空格
        new_path = os.path.join(folder_path, new_name)
        old_path = os.path.join(folder_path, filename)

        # 如果新文件名已经存在，删除旧文件
        if os.path.exists(new_path):
            os.remove(old_path)
            progress_bar.set_postfix({"已删除": filename})
        else:
            os.rename(old_path, new_path)
            progress_bar.set_postfix({"已重命名": new_name})
            processed_names.add(new_name)
    else:
        progress_bar.set_postfix({"无需修改": filename})

# 删除重复文件（保留最后一个）
for duplicate_name in processed_names:
    duplicates = [filename for filename in files_to_process if filename.lower() == duplicate_name.lower()]
    if len(duplicates) > 1:
        for duplicate in duplicates[:-1]:
            duplicate_path = os.path.join(folder_path, duplicate)
            os.remove(duplicate_path)

progress_bar.close()
