# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class SpiderymPipeline(object):
    def process_item(self, item, spider):
        if item['yon']:
            #如果筛选器是True，打印
            print('----------标题：----------',item['title_0818'])
            #print('----------时间：----------',item['time_0818'])
            print('----------内容：----------',item['cts_0818'])
            print('----------链接：----------',item['urls_0818'])
            print('----------图片：----------',item['imgs_0818'])
        else:
            print(item['title_0818'],'----------不打印：----------')
    #1 内容超过 N个，就不显示后面的？ 那如果是多个的那种呢
    #2 把链接转换成短链接。如果链接在内容里，则先转换成段落，再替换内容里的链接
    #3 图片，下载后发送
    #标题不用显示了，因为已经加入到内容里了

