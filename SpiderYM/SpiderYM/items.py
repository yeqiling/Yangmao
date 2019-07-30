# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html


from scrapy import Field,Item

class SpiderymItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    #开始页面
    url_begin = Field()
    #第一个页面
    url_one = Field()

    #判断是否输出(采集)  yes_or_no
    yon = Field()

    cts_0818 = Field()  #contents文本内容
    title_0818 = Field()    #标题
    time_0818 = Field()     #时间
    urls_0818 = Field()      #链接    列表，可能有多个
    imgs_0818 = Field()     #图片    列表，可能有多个
    

'''
class tuan0818test(Item):
    content_test = Field()
    title_test = Field()
'''