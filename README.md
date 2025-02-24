# mubu_exporter
幕布是一款很好的笔记软件，然而它不提供文档的批量导出功能。本人使用幕布长达4年，在其中记录了大量含有latex数学公式的笔记，但其编辑效率和排版功能越来越难以满足我的需求，于是在几个月前我决定更换平台，便有了批量导出文档的问题。

本项目基于python，通过模拟用户点击的方式批量下载幕布里的所有文档，相当于替你一个个点开文档并点击导出。

本项目导出的文档格式为`html`，而后可以通过`html2md.py`将其转为`markdown`格式。如果你想导出`pdf`或`doc`格式，网上已有插件`Mubu Dumper`可用。

## 使用方式
文件有很多个，但你只需打开`main.py`

### 获取`get_all_documents_page.json`（需手动获取）
- 先在网页端打开幕布，登录账号，进入“我的文档”界面
- F12打开开发者工具，点到“网络”选项卡，**刷新页面**
- `Ctrl+F`打开查找，查找`get_all_documents_page`
- 在`get_all_documents_page`里点到“预览”，`Ctrl+A`全选，`Ctrl+C`复制，然后自己新建一个`get_all_documents_page.json`文件，粘贴进去
- 如果文档很多，会有两个`get_all_documents_page`，两个都要复制。往往第一个里有`folders`和`documents`字段，第二个里只有`documents`字段，把第二个的`documents`字段合并到第一个的`documents`字段里即可。
![image](https://github.com/user-attachments/assets/8734c7f0-a0f9-4d89-86fc-4ade83bbd0f9)

- 保存`get_all_documents_page.json`文件，放在和`main.py`同一目录下

### 导出所有幕布文档为`html`文件
- 运行`main.py`
- `output_dir = './output'`可以设置`html`文件保存目录
- 在终端输出“请扫描二维码登录”的时候，同级目录下会出现一个“mubu扫码.png”，打开图片扫码登录
- 注意请在10秒内扫码登录，如果不慎超时了，请把python程序关掉，重新运行
- 接下来等待下载即可，大概一秒下载一个。

### 检查是否有文档被折叠
- 如果文档中有节点被折叠，那么折叠过的节点不会展开，被折叠的内容不会被导出
- 虽然我已经试图在每次下载前检查折叠并全部展开，但不知为什么还是会有一些文档被折叠
- （因为我是用快捷键展开折叠的，所以原先完全展开的节点反而有可能被折叠）
- 所以在转为md前务必先用`collapsed_check.py`检查一下

### 将`html`转换为`markdown`
- 该功能已写于`main.py`的最后一行，会在`html`全部下载完毕后自动执行
- 你也可以注释掉这一行，然后通过运行`html2md.py`来转换格式
- `source_dir = 'output'`可以设置`html`文件所在目录
- `target_dir = 'markdown'`可以设置`markdown`文件输出目录
- `delete_space = True`可以设置是否删除公式块左右的空格

### 注意
- 有密码的文件不会下载
- 可通过`log.txt`文件查看哪些文件下载失败
