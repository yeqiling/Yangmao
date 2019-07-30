# -*- coding: utf-8 -*-
import json
import os
import re
import logging
import smtplib
from pyquery import PyQuery as py
from datetime import datetime
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr

# 日志格式设定
logging.basicConfig(level=logging.INFO, format='\n%(asctime)s - %(levelname)s: %(message)s')
# 存储目录
BASE_DIR = '/tmp'
# 临时文件
ZK_TMP_FILE = BASE_DIR + '/zk_monitor_%s.json'
# 请求头
REQUEST_HEADERS = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
}
# 爬虫链接
ZK_BASE_URL = 'http://www.zuanke8.com/forum.php?mod=forumdisplay&fid=15&filter=author&orderby=dateline'
# 编码
UTF8_ENCODING = 'utf-8'
GBK_ENCODING = 'gbk'
# 监控关键字
KEYWORD = {
    'include': '密令|红包|水|速度|神券|京豆',
    'exclude': '权限|水贴'
}
# 发送者
SENDER = {
    'name': '小分队',
    'email': 'youremail@126.com',
    'smtp': 'smtp.126.com',
    'pass': 'yourpass'
}
# 接受者
RECEIVERS = [
    {
        'name': 'username',
        'email': 'youremail@qq.com',
    }
]
# 全局存储数据
result = dict()


def main_handler(event, context):
    global result
    tmp_path = ZK_TMP_FILE % datetime.now().strftime('%Y%m%d')
    try:
        logging.info('临时文件：' + tmp_path)
        if not os.path.exists(tmp_path):
            logging.info('临时文件不存在')
        else:
            with open(tmp_path, 'r', encoding=UTF8_ENCODING) as f:
                result = json.load(f)
        logging.info('当前存储数据量：' + str(len(result.keys())))

        # 首页热门内容
        d = py(ZK_BASE_URL, headers=REQUEST_HEADERS, encoding=GBK_ENCODING)
        # 每个帖子
        d('#threadlisttableid tbody').each(deal_post)
        return "Success"
    except Exception as ex:
        logging.error('主任务运行异常：' + str(ex))
        raise ex
    finally:
        # 创建存储目录
        if not os.path.exists(BASE_DIR):
            os.makedirs(BASE_DIR)
        # 存储结果
        with open(tmp_path, 'w', encoding=UTF8_ENCODING) as f:
            logging.info('保存数据结果')
            json.dump(result, f)


def send_monitor_email(title, content):
    # 发送消息
    message = MIMEText(content, 'html', UTF8_ENCODING)
    # 发送者
    message['From'] = format_tofrom(SENDER)
    # 接收者
    message['To'] =  format_tofrom(RECEIVERS)
    # 标题
    message['Subject'] = Header(title, UTF8_ENCODING)
    
    try:
        logging.info('启动邮件服务')
        smtp_server = smtplib.SMTP_SSL(SENDER['smtp'])
        smtp_server.login(SENDER['email'], SENDER['pass'])
        smtp_server.sendmail(SENDER['email'], [r['email'] for r in RECEIVERS], message.as_string())
        smtp_server.quit()
        logging.info('邮件发送成功')
    except smtplib.SMTPException as ex:
        logging.error('无法发送邮件：' + str(ex))
        raise ex
    except Exception as ex:
        logging.error('发送邮件异常：' + str(ex))
        raise ex


def format_tofrom(obj):
    if isinstance(obj, list):
        headers = []
        for receiver in obj:
            headers.append(formataddr([receiver['name'], receiver['email']], UTF8_ENCODING))
        return ';'.join(headers)
    else:
        return formataddr([obj['name'], obj['email']], UTF8_ENCODING)


# 每个帖子
def deal_post(i, e):
    global result
    match = re.match('normalthread_(\d+)', str(py(e).attr('id')))
    if match is None:
        return
    # 帖子主键
    post_id = match.group(1)
    # 已存在
    if result.get(post_id) is not None:
        return
    # 帖子标题
    title = py(e).find('th').text()
    if re.match(r'.*(' + KEYWORD['include'] + ').*', title, re.I) is None \
        or re.match(r'.*' + KEYWORD['exclude'] + '.*', title, re.I) is not None:
        return
    # 帖子地址
    url = py(e).find('th a').attr('href')
    # class="by"
    time_ele = py(e).find('td:eq(1)')
    content = get_post_content(url)
    result[post_id] = {
        'url': url, 
        'title': title, 
        'time': time_ele.find('em').text(), 
        'content': content
    }
    logging.info('准备推送信息：' +  str(result[post_id]))
    title = result[post_id]['title']
    content = """
        <p>%s</p>
        <p>更多访问：
            <a href="%s">电脑版</a>&emsp;
            <a href="http://www.zuanke8.com/archiver/?tid-%s.html">简洁版</a>
        </p>
    """ % (result[post_id]['content'], result[post_id]['url'], post_id)
    send_monitor_email(title, content)


# 帖子链接内容
def get_post_content(url):
    d = py(url, headers=REQUEST_HEADERS, encoding=GBK_ENCODING)
    div = d('#postlist>div:first')
    tr = div.find('tr:first')
    content = tr.find('.t_f').text()
    return content


if __name__ == '__main__':
    main_handler(None, None)