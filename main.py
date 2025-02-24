#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2024/10/6
# @Author      : AshlenBin

import json
import os
import re
import shutil
from playwright.sync_api import Playwright, sync_playwright
import tkinter as tk
from tkinter import PhotoImage
import time
import html2md
from bs4 import BeautifulSoup

html_dir = './html'
markdown_dir = './markdown'

with open('./get_all_documents_page.json', 'r', encoding='utf-8') as r:
    data = json.loads(r.read())['data']
if(not os.path.exists(html_dir)):  # 如果文件夹不存在则创建
    os.mkdir(html_dir)

def replace_disallowed_chars(filename):
    # 搜索字符串中不允许在文件名中出现的字符，并替换为对应的全角字符
    # 定义不允许字符及其对应的全角字符
    disallowed_chars = {
        '\\': '＼',
        '/': '／',
        ':': '：',
        '*': '＊',
        '?': '？',
        '"': '＂',
        '<': '＜',
        '>': '＞',
        '|': '｜'
    }
    for char, fullwidth_char in disallowed_chars.items():
        filename = filename.replace(char, fullwidth_char)
    return filename

def handle():
    folders_dict = {item['id']: {"name": replace_disallowed_chars(item['name']), 'old_name': item['name'], "id": item['id'], "children": []} for item in data['folders']}
    for item in data['folders']:
        parent_id = item['folderId']
        if parent_id == "0":
            continue
        if parent_id in folders_dict:
            folders_dict[parent_id]['children'].append(folders_dict[item['id']])

    tree_structure = [folders_dict[item['id']] for item in data['folders'] if item['folderId'] == "0"]
    print(json.dumps(tree_structure, ensure_ascii=False))
    folder_map = {}
    for i in tree_structure:
        folder_map.update(convert_tree_to_dict(i))
    print(folder_map)

    for k, v in folder_map.items():
        if not os.path.exists(html_dir + f"/{v}"):
            os.mkdir(html_dir + f"/{v}")

    doc_map = {}
    for document in data['documents']:
        if document['folderId'] != '0':
            doc_map[document['id']] = {
                'folderId': document['folderId'],
                'name': replace_disallowed_chars(document['name']),
            }
        if document['folderId'] == '0':
            doc_map[document['id']] = {
                'folderId': '0',
                'name': replace_disallowed_chars(document['name']),
            }
    print(json.dumps(doc_map, ensure_ascii=False, indent=2))

    for k, v in doc_map.items():
        file_name = v['name']
        if not file_name:
            file_name = '无标题'

        folderId = v['folderId']

        if folderId == '0':
            file_path = html_dir + f"/{file_name}.html"
        else:
            folder_path = folder_map[folderId]
            file_path = html_dir + f"/{folder_path}/{file_name}.html"
        v['file_path'] = file_path

    print(doc_map)
    return doc_map


def convert_tree_to_dict(node, path=""):
    current_path = f"{path}/{node['name']}" if path else node['name']
    result = {node['id']: current_path}
    for child in node['children']:
        result.update(convert_tree_to_dict(child, current_path))
    return result

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

def QR_code(image_path):
    # 创建主窗口
    root = tk.Tk()
    root.title("请扫描二维码登录")

    img = PhotoImage(file=image_path)
    label = tk.Label(root, image=img)
    label.pack()

    root.mainloop()

class MubuUI(object):
    def __init__(self, headless: bool = False):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=headless)
        self.context = self.browser.new_context(
            # viewport={'width': 1920, 'height': 1080}
        )
        self.context.set_default_timeout(1000 * 5)
        self.page = self.context.new_page()
        self.page.goto('https://mubu.com/app')
        self.page.locator('svg[type="wechat_login"]').click()
        self.page.wait_for_timeout(1000 * 1)
        self.page.screenshot(path='./mubu扫码.png')
        print('请扫描二维码登录')
        QR_code('./mubu扫码.png')
        # for i in range(10):
        #     print(f"{10-i}", end=' ')
              
        # print('扫码结束')


    def main(self, id, file_path):
        print(file_path)
        url = f'https://mubu.com/app/edit/home/{id}'
        self.page.goto(url)
        # self.save_cookies()

        self.page.wait_for_timeout(1000 * 0.5)
        
        has_password = self.page.locator('div[class="main"]').count()
        if(has_password):
            print(f"{file_path} 有密码，跳过")
            return False
        
        # 发送按键事件 "shift+alt+ctrl+."展开所有折叠节点
        is_collapsed = self.page.locator('.collapsed.outliner-node').count()
        if is_collapsed:
            self.page.keyboard.down('Control')
            self.page.keyboard.down('Alt')
            self.page.keyboard.down('Shift')
            self.page.keyboard.press('Period')
            self.page.keyboard.up('Shift')
            self.page.keyboard.up('Alt')
            self.page.keyboard.up('Control')
        
        self.page.locator('#headerbar-more-button').click()
        self.page.wait_for_timeout(1000 * 0.2)
        self.page.locator('text=导出/下载').click()
        # self.page.wait_for_timeout(1000 * 0.5)
        with self.page.expect_download() as download_info:
            self.page.locator('div[class="img-wrap html"]').click()
            self.page.wait_for_timeout(1000 * 0.05)
            download = download_info.value
            path = download.path()
            print(path)
            if(check_collapsed_div(path)): # 如果文件中存在折叠节点，发回去重新下载
                print(file_path + '下载失败，存在折叠节点')
                return 'collapsed'
            print(file_path + '下载成功')
            if(not os.path.exists(os.path.dirname(file_path))):  # 如果文件夹不存在则创建
                os.mkdir(os.path.dirname(file_path))
            shutil.move(path, file_path)
        return True

ui = MubuUI(True)



if __name__ == '__main__':
    config = handle()  # 获取目录结构并创建
    
    # 以html格式导出所有文档
    failed_list = []
    for k, v in config.items():
        if os.path.exists(v['file_path']):
            print(f"{v['file_path']} 文件已存在")
            continue
        while True:
            try:
                result = ui.main(k, v['file_path'])
                if(result == 'collapsed'):
                    continue
                if(not result):
                    failed_list.append(v['file_path'])
                break
            except Exception as e:
                print(e)
                print(f"{v['file_path']} 下载失败，正在重试")

    ui.playwright.stop()
    print("未下载的文件：")
    print(failed_list)
    # 将failed_list写入log.txt
    with open('log.txt', 'a', encoding='utf-8') as f:
        import time
        f.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+'\n')
        f.write("未下载的文件："+'\n')
        f.write('\n'.join(failed_list))
    
    # 将html文件转换为markdown文件
    html2md.main(html_dir, markdown_dir, delete_space=True)
    
