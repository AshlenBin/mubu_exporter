import os
from bs4 import BeautifulSoup, Tag
from mubu_converter import MubuConverter
import sys
import re


source_dir = 'html'
target_dir = 'markdown'
delete_space = True # 是否删除公式块左右的空格


def main(source_dir, target_dir, delete_space = True ):
    if(not os.path.exists(source_dir)):
        print(f"{source_dir} 源文件夹不存在")
        sys.exit(1)
        
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            # 源文件和目标文件的路径
            file_name, file_format = os.path.splitext(file)
            # print(f'file_name: {file_name}, file_format: {file_format}')
            
            if(file_format != '.html'):   # 如果文件格式不是html就跳过
                continue

            file_html_path = os.path.join(root, file)
            
            md_dir = root.replace(source_dir, target_dir)
            os.makedirs(md_dir, exist_ok=True)
                
            file_md = os.path.join(md_dir, file_name+'.md')
            print(file_md)
            with open(file_html_path, 'r',encoding="utf-8") as f:
                print(file_html_path)
                MubuConverter().convert(f,delete_space,saveTo=file_md)


if __name__ == "__main__":
    main(source_dir, target_dir, delete_space)
            