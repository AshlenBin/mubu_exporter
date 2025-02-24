import os
from bs4 import BeautifulSoup, Tag
from mubu_converter import MubuConverter
import sys
import re

file_html_path = r"C:\Users\pc\Documents\WeChat Files\wxid_vi7dvf0s7zox22\FileStorage\File\2025-01\SwimFish.html"


def main(file_html_path):   # 输出md文件到源文件夹
    if(not os.path.exists(file_html_path)):
        print(f"{file_html_path} 源文件夹不存在")
        sys.exit(1)

    # 源文件和目标文件的路径
    file_dir, file_name = os.path.split(file_html_path)
    file_name, file_format = os.path.splitext(file_name)

    if(file_format != '.html'):   # 如果文件格式不是html就跳过
        print("文件格式不是html")
        return

    file_md = os.path.join(file_dir, file_name+'.md')
    print(file_md)
    with open(file_html_path, 'r',encoding="utf-8") as f:
        MubuConverter().convert(f,saveTo=file_md)

if __name__ == "__main__":
    main(file_html_path)
            