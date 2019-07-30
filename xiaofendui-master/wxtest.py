# -*- coding: utf-8 -*-
import json
import os
import re
import time
import logging
import itchat
import random
import requests
from urllib.parse import unquote
from pyquery import PyQuery as py
from datetime import datetime

# 日志格式设定
logging.basicConfig(level=logging.INFO, format='\n%(asctime)s - %(levelname)s: %(message)s')
# 存储目录
BASE_DIR = os.getcwd() + '/tmp'
print(BASE_DIR)
# 临时文件
ZK_TMP_FILE = BASE_DIR + '/zk_monitor.json'
# 请求头
REQUEST_HEADERS = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
}
# 爬虫链接

TUAN_BASE_URL = 'http://www.0818tuan.com/list-1-0.html'
# 任务间隔时间
ZK_TASK_INTERVAL = 300
# 请求超时设置，默认5秒
REQUEST_TIMEOUT = 5
# 编码
UTF8_ENCODING = 'utf-8'
GBK_ENCODING = 'gbk'
GB2312_ENCODING = 'gb2312'
# 监控关键字
KEYWORD = {
    'include': r'密令|红包|洪水|大水|有水|速度|神券|京豆|好价|bug|\d+元|\d+券|\d+减\d+|\d+-\d+',
    'exclude': r'权限|水.?贴|什么|怎么|怎样|不是|不能|不行|没有|反撸|求|啥|问|哪|吗|么|？'
}
# 匹配群聊名称
MATCH_ROOMS = ['测试']
# 全局存储数据
result = dict()
last_result = dict()
# 推送名单
user_names = list()


def main_handler():
    global result, last_result
    try:
        logging.info('临时文件：' + ZK_TMP_FILE)
        if not os.path.exists(ZK_TMP_FILE):
            logging.info('临时文件不存在')
        else:
            with open(ZK_TMP_FILE, 'r', encoding=UTF8_ENCODING) as f:
                result = json.load(f)
        logging.info('当前存储数据量：' + str(len(result.keys())))

        # 0818tuan
        d = py(TUAN_BASE_URL, headers=REQUEST_HEADERS, encoding=GB2312_ENCODING, timeout=REQUEST_TIMEOUT)
        d('.list-group > .list-group-item').each(deal_post_tuan)
    except Exception as ex:
        logging.exception('主任务运行异常：' + str(ex))
        raise ex
    finally:
        # 创建存储目录
        if not os.path.exists(BASE_DIR):
            os.makedirs(BASE_DIR)
        # 存储结果
        with open(ZK_TMP_FILE, 'w', encoding=UTF8_ENCODING) as f:
            # 超过数量清空
            if len(result.keys()) > 500:
                last_result.clear()
                last_result = result
                result = dict()
            logging.info('保存数据结果')
            json.dump(result, f)

def deal_post_tuan(i, e):
    global result
    #print(type(e))
    info = dict()
    #获取标题
    info['title'] = py(e).attr('title')
    #获取网址
    url = py(e).attr('href')
    #获取时间
    info['time'] = py(e).find('.badge-success').text()
    info['images'] = list()
    #print(info)
    # 排除置顶
    if info['title'] is None or info['time'] == '':
        print('跳出，时间标题不对')
        return
    # 排除非权限贴以及标题非关键字
    #if len(re.findall(r'\[权\d*\]', info['title'])) == 0:
        #print(i,':',info['title'],end='')
        #print('--------权限问题')
        #return
    if is_result_include(url):
        print(i,':',info['title'],end='')
        print('----------此网址已读取过')
        return
    #if not is_keyword_valid(info['title']):
        #print(i,':',info['title'],end='')
        #print('-----------无关键字')
        #return
    #完整网址   http://www.0818tuan.com  + url
    info['url'] = os.path.dirname(TUAN_BASE_URL) + url
    logging.info('爬取链接：' + info['url'])

    #进入帖子，爬取内容
    d = py(info['url'], headers=REQUEST_HEADERS, encoding=GB2312_ENCODING, timeout=REQUEST_TIMEOUT)
    # 区块元素，clone获取一个节点的拷贝
    #class="post-content" 下的第一个 p 节点，里面就是全部内容，标题，内容，图片
    ele = d('.post-content>p:first').clone()

    for img in ele.find('img'):
        #获取  img 的  src，也就是图片网址
        src = py(img).attr('src')
        if len(re.findall('.jpg|.jpeg|.png', src, re.I)) == 0:
            #如果不是jpg,jpeg,png格式，则下一个图片
            continue
        info['images'].append(src)

    #print(info['images'])
    #html() 获取相应的HTML块   text() 获取相应的文本块，
    ee = ele.html
    print('ee--------------',end='')
    print(ee)
    # a 取出 img 块
    a = ele.remove('img').html()
    print('a--------------',end='')
    print(a)
    # b  <br/> 用@#@ 代替
    b = py(re.sub(r'(<br/?>\s*\n?)+', '@#@', a))
    #print('b--------------',end='')
    #print(b)
    #只获取文本块，并且删除@#@
    info['content'] = b.text().replace('@#@', '\n')

    mapping = get_url_mapping(ele)
    for href in mapping:
        info['content'] = info['content'].replace(href, mapping[href])
    result[url] = info
    print('content:-------------------------',end='')
    print(info['content'])
    # 内容非关键字
    if not is_keyword_valid(info['content'], 'content'):
        logging.info('内容关键字过滤：' + str(info))
        return
    logging.info('准备推送信息：' + str(info))
    #send_msg(info)

# 判读结果是否包含
def is_result_include(key):
    global result, last_result
    # 已存在
    if result.get(key) is not None or last_result.get(key) is not None:
        return True
    else:
        return False

# 判断是否符合关键字
def is_keyword_valid(text, check_type='title'):
    if check_type == 'title':
        if len(re.findall(KEYWORD['include'], text, re.I)) == 0 \
            or len(re.findall(KEYWORD['exclude'], text, re.I)) > 0:
            return False
        else:
            return True
    else:
        return False if len(re.findall(KEYWORD['exclude'], text, re.I)) > 0 else True

# 发送消息
def send_msg(info):
    # 推送用户名单
    global user_names
    files = list()
    content = '%s\n\n%s\n\n电脑版：%s' % (info['title'], info['content'], info['url'])
    for name in user_names:
        itchat.send_msg(content, toUserName=name)
        # 发送图片
        for url in info['images']:
            path = os.path.join(BASE_DIR, os.path.basename(url))
            files.append(path)
            f = open(path, 'wb')
            f.write(requests.get(url).content)
            f.close()
            itchat.send_image(path, toUserName=name)
        time.sleep(random.randint(2, 5))
    # 删除临时文件
    for path in files:
        if os.path.exists(path):
            os.remove(path)

# 获取要替换的链接
def get_url_mapping(ele):
    url_mapping = dict()
    for i in ele.find('a'):
        href = py(i).attr['href']
        url = py(i).text()
        if re.match(r'https?.+\.\..+|.*链接.*', url) is None \
            or href is None:
            continue
        if '0818tuan' in href and '?u=' in href:
            url_mapping[url] = unquote(href.split('?u=')[1])
        else:
            url_mapping[url] = unquote(href)
    return url_mapping


if __name__ == '__main__':
    '''
    logging.info('请扫描二维码登录')
    itchat.auto_login(hotReload=True, enableCmdQR=True)
    logging.info('登录成功')
    chatrooms = itchat.get_chatrooms(contactOnly=True)
    for room in chatrooms:
        logging.info('获取群聊通讯：' + room['NickName'] + '|' + room['UserName'])
        if room['NickName'] in MATCH_ROOMS:
            user_names.append(room['UserName'])
    '''
    # 定时循环
    while True:
        try:
            main_handler()
        except Exception as ex:
            logging.exception('主线程异常：' + str(ex))
        time.sleep(ZK_TASK_INTERVAL)
    # 退出登录
    #itchat.logout()