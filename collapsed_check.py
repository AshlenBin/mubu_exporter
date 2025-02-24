import os
from bs4 import BeautifulSoup
import sys

# 检查并删除所有存在折叠的文档

dir_path = 'output'

def check_collapsed_div(file_path):    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        soup = BeautifulSoup(content, 'html.parser')
        
        # 查找类名为 'collapsed' 的 div 控件
        collapsed_divs = soup.find_all('li', class_='collapsed')
        
        if collapsed_divs:
            return True
        else:
            return False

if __name__ == '__main__':
    if(not os.path.exists(dir_path)):
        print(f"{dir_path} 源文件夹不存在")
        sys.exit(1)
    list_files = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            # 源文件和目标文件的路径
            file_name, file_format = os.path.splitext(file)
            if(file_format != '.html'):
                continue
            file_path = os.path.join(root, file)
            print(file_path)
            if(check_collapsed_div(file_path)):
                list_files.append(file_path)
                print(f'{file_path} 中存在折叠')
                # 删除该文件
                os.remove(file_path)
    print('存在折叠的文档')
    print(list_files)