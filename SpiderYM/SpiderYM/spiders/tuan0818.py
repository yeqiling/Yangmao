# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.http import Request

import re
from SpiderYM.items import SpiderymItem
#import logging

#logger = logging.getLogger(__name__)
#全局变量，用于读取的本地存储信息，判断是否读取过地址
'''
def read_local():
    global result
    #读取本地Json
    #文件路径
    file_path = ''
    try:
        if not os.path.exists(file_path):
            print('临时文件不存在')
        else:
            with open(file_path, 'r', encoding=UTF8_ENCODING) as f:
                result = json.load(f)
    except Exception as ex:
        print('读取临时文件异常：' + str(ex))
        raise ex
    #finally:
'''


class Tuan0818Spider(CrawlSpider):
    name = 'tuan0818'
    allowed_domains = ['0818tuan.com']
    start_urls = 'http://www.0818tuan.com'
    #start_urls = ['list-1-0.html','list-2-0.html','list-3-0.html','list-4-0.html']
    #http://www.0818tuan.com/list-1-0.html  最新活动线报  //div[@class='col-md-8'][2]
    #http://www.0818tuan.com/list-2-0.html  本站实测线报  //div[@class='col-md-8'][1]
    #http://www.0818tuan.com/list-3-0.html  优惠卷       //div[@class='col-md-4'][1]
    #http://www.0818tuan.com/list-4-0.html  最新促销活动 //div[@class='col-md-8'][3]
    url_base = 'http://www.0818tuan.com'
    result = dict()

    # 判断是否符合关键字
    def is_keyword_valid(self,text,check_type=False):
        '''默认模式：标题，只匹配 不包含的关键字
        其他：匹配 包含与不包含的关键字
        '''
        KEYWORD = {
                'include': r'密令|兑换|红包|洪水|大水|有水|速度|神券|京豆|好价|bug|\d+元|\d+券|\d+减\d+|\d+-\d+',
                'exclude': r'APP发布|直播|权限|水.?贴|什么|怎么|怎样|不是|不能|不行|没有|反撸|求|啥|问|哪|吗|么|？'
            }


        if check_type:
            if len(re.findall(KEYWORD['include'], text, re.I)) == 0 \
                or len(re.findall(KEYWORD['exclude'], text, re.I)) > 0:
                print('没找到关键字，或者含有禁忌关键字')
                return False
            else:
                return True
        else:
            #return False if len(re.findall(KEYWORD['exclude'], text, re.I)) > 0 else True
            if len(re.findall(KEYWORD['exclude'], text, re.I)) > 0:
                print('含有禁忌关键字')
                return False
            else:
                return True

    def start_requests(self):
        url_new = self.url_base + '/list-1-0.html'  #最新活动线报
        url_huodong = self.url_base + '/list-4-0.html'    #最新促销活动
        lscs_onepage = False  #开启关闭临时测试 一个网页
        if lscs_onepage:
            url_ls = 'http://www.0818tuan.com/xbhd/237424.html'
            yield Request(url=url_ls,meta={'title':None,'time':None},callback=self.parse_new_ok)
        else:
            yield Request(url=url_new,callback=self.parse_new)
            #yield Request(url=url_new,meta={"url_begin":url_new},callback=parse_new)
            #yield Request(url=url_huodong,meta={"url_begin":url_huodong},callback=parse_huodong)
            #yield Request(url=url_huodong,callback=self.parse_huodong)
            #return [Request(self.start_urls,callback=self.parse_yi)] 

    def zh_url(self,str):
        '''转换url，去掉 前缀
        '''
        if '=http' in str:
            print('去掉没用的')
            a = str.replace('=http','@#@')
            url_ls = 'http' + a.split('@#@')[1]  #切割
        else:
            url_ls = str  #原网址，则不切割
        return url_ls

    def zh_text(self,text_list):
        ''' 去除列表中任意空白符和逗号,还要空白的
        删除列表中的'/r/n' '/n/t' 和空格   
        带有...的网页链接不能删！！
        '''
        #text_list2 = [x for x in text_list if x.strip().strip('\n\t').strip('\r\n')]
        bb = list()
        #print('原有--------------',)
        for x in text_list:
            #b = re.sub(' ','',x) #去除空格
            #b = re.sub('\t','',b) #去除\t
            #b = re.sub('\n','',b)#去除\n
            #b = re.sub('\r','',b)#去除\r
            #b = re.sub(',','',b)#去除 ,
            #b = b.strip()
            r1 = re.compile('\s|,')  #去除任意空白符，和 逗号  \t???
            b = re.sub(r1,'',x)
            
            if b == '':
                continue
            #if '...' in b:
                #continue
            bb.append(b)

        #bb = list(set(bb))
        num = len(text_list) - len(bb)
        #print('去除了--------------',str(num) + '个无用空白符，逗号等')
        #print(bb[:-7])
        return bb

    def zh_cts(self,ctss,P_1=True):
        '''转换文本
        先删除没用的，再去掉后面固定7个
        分2种情况，一种是只取P1下的，还有一个是全部标签获取的。
        P1就不去除，全部标签则去掉后面固定7个
        '''
        #删除空格和没用的
        cts1 = self.zh_text(ctss)
        #print('删除没用项后~~~~~~~~~~~~再删后8个',cts1)

        num_cts = len(cts1)  #共N个文本
        cts2 = list()
        if P_1:
            return cts1
        else:
            cts2 = cts1[:-8]  #去掉后面8个
            return cts2

    def zh_cf(self,text_list):
        '''去除列表重复项'''
        new_list = list()
        for x in text_list:
            if x not in new_list:
                new_list.append(x)
        return new_list

    def zh_url_mapping(self,xpath_a):
        '''传递a的xpath，获取块下的所有a标签，
        a标签下的链接和链接文本 生成一个字典，
        链接是value，链接文本是key。
        '''
        url_mapping = dict()  #字典
        #a = xpath_a.xpath('./a') #获取块所有a标签
        for x in xpath_a:
            #每有一个 a标签，寻找一次
            a_href = x.xpath('./@href').extract_first()  #value
            print('a下的原始链接---------------',a_href)
            a_text = x.xpath('./text()').extract_first()  #key
            print('a下的链接文本---------------',a_text)
            #if re.match(r'https?.+\.\..+|.*链接.*', a_text) is None \
                #or a_text is None:
                #continue
            if a_text is None or '>>' in a_text:
                #链接文本空的，则退出转换。
                #本来re.match(r'http', a_text) is None or \  计算链接文本是否含http，但是有时链接文本是中文，所以删掉
                print('链接文本是空,或者删掉没用项')
                continue
            if 'tao/taoke.php?item_id' in a_href:
                #原始链接是/tao/taoke.php?item_id=580003475920  这样的链接,需要把id取出来，并且合并链接文本前面的链接地址
                if 'item_id' in a_text:
                    #链接文本是https://detail.ju.taobao.com/home.htm?item_id... 如果是这种含有item_id的缩略链接，则替换
                    ls_id =  a_href.split('=')[1]  #去后面id号
                    ls_qz = a_text.split('item_id')[1] #取前缀
                    url_mapping[a_text] = ls_qz + ls_id
                    continue  
                else:
                    #如果没有这种，则跳过，不要了，因为是tuan0818网站的自己的链接
                    continue   
                #需要把
            if 'xbhd' in a_href or 'list-1-0.html' in a_href:
                continue      #如果是   /xbhd/235097.html，这样的，最后2个必会找到的（上一篇，下一篇）  #还有一种返回列表
            if '0818tuan' in a_href and '?u=' in a_href:
                url_mapping[a_text] = a_href.split('?u')[1]
            elif '=http' in a_href:
                url_mapping[a_text] = 'http' + a_href.split('=http')[1]
            else:
                url_mapping[a_text] = a_href
            #print('a下的原始链接---------------',a_href)
            #print('a下的链接文本---------------',a_text)
        #print(url_mapping)
        return url_mapping

            


    def parse_new(self,response):
        ''' 抓取 最新活动线报http://www.0818tuan.com/list-1-0.html的url地址；
        或者打开本地json数据，判断是url否被抓取过
        '''
        page_one = Selector(response)  
        #全部内容,并且 用 /a分成一行一行  （必须是多行才行，如果不分行，一整块肯定是不行的）
        contents = page_one.xpath('//*[@id="redtag"]/a')   #这个后面不需要加extract，因为后面的 cc 还要调用
        #print(contents)
        #因为爬取是相同类型的数据，所以用循环处理
        for cc in contents:
            print('第-----xx-----行',cc)
            item = SpiderymItem()      
            #再次调用 xpath 匹配时，  加一个  。   就会在之前的基础上找
            url_one = cc.xpath('./@href').extract_first() #完整的网址
            #print(url_one)
            #title = ''
            title  = cc.xpath('./@title').extract_first() #标题
            print('标题--------------------',title)
            time  = cc.xpath('./span/text()').extract_first() #时间
            if url_one == '/xbhd/234233.html':
                #无用的网址，会出错,因为不再title里，所以直接检测网页
                continue
            if title == '' or title == None:
                #标题为空时，跳过
                continue
            #各种判断
            #if title.find('APP发布') != -1:
             #排除第一个  0818团线报网APP发布 推送、分享、交流互助都有。。。  -1是没有找到的意思
               #continue
            #判断是否符合关键字，包含或不包含
            if not self.is_keyword_valid(title):
                continue

            '''    
            if self.result.get(url[i]):
            #如果网页已存在与json文件中，跳过
                return
            '''
            yield Request(url=self.url_base + url_one,meta={'title':title,'time':time},callback=self.parse_new_ok)

    def parse_new_ok(self,response):
        #访问网页
        page_ok = Selector(response)
        #建立item
        item = SpiderymItem()
        imgs = list()
        urls = list()
        content_text = list()
        yes_or_no = True
        #--------------------------------------------------------标题
        if response.meta['title'] != None:
            #如果有标题
            title = response.meta['title']
            #print('title-------------------',title)
            item['title_0818'] = title
            content_text.append(title) #放入title，后面可以转换成元组然后把重复的删除掉，以防标题和内容重复
        else:
            #如果没有标题，再次获取标题(为了临时调试网页用，直接输入网页可直接调用parse_new_ok)
            title = page_ok.xpath('//div[@class="post-head"]/h1[@class="text-center"]/text()').extract_first()
            item['title_0818'] = title
            content_text.append(title)
        #--------------------------------------------------------时间，没什么用
        time = response.meta['time']
        if time:
            #如果有时间
            item['time_0818'] = time


        #-----------------------------------------------------------整个内容大块，全部内容
        contents = page_ok.xpath('//div[@class="post-content"]')
        content_ss = contents.xpath('./descendant-or-self::*')   #注意，这里除了P还有其他的节点，比如div

        #num_2 = len(content_ss.extract())
        #print('-----------共有',num_2,'个节点')
        content_cst = contents.xpath('./descendant-or-self::text()')  #获取全部内容
        content_text = content_cst.extract()
        #处理内容的文本列表
        #print('找到的-----原文本--------------------------',content_text)
        cts = self.zh_cts(content_text,False)  #去除文本中没用的,必须先这个，再去除重复，否则顺序会错乱
        #cts = list(set(cts))  #去除文本中重复项,去重复会顺序错乱
        cts = self.zh_cf(cts)  #这样去重复，没问题
        #print('找到的------改后文本--------------------------',cts)
        urls_text = list()  #链接文本
        for content in content_ss:
            #找图片和链接
            #ls_text = content.xpath('./descendant::text()').extract() #文本内容
            #print('文本内容数量---------',len(content.xpath('./text()').extract()))
            #ls_url = content.xpath('./a/@href').extract_first() #链接
            #ls_url = content.xpath('./a') 
            ls_url_a = content.xpath('./a')
            ls_urls = self.zh_url_mapping(ls_url_a) #字典，获取a标签，方便后面获取链接和链接的文本，转换，也可以去重复
            #print('链接内容数量---------',len(content.xpath('./a/@href').extract()))
            #ls_url_text = content.xpath('./a/text()').extract_first()  #链接文本
            ls_img = content.xpath('./img/@src').extract() #图片

            #难点
            #1、ls_url也要设置成列表！！！否则一些P1下的链接获取不到比如http://www.0818tuan.com/xbhd/235344.html
            #链接替换原本的文本中的 链接
            #2、怎么按顺序排列  P1下的 文字、链接、文字、链接。 现在是一整块的 文字，和一整块的链接
            
            #BUG
            #1、有时候，内容里的链接没有替换到
            #2、删除一些长的文本

            if ls_urls:
                 for ls_url in ls_urls:
                    #ls_url是字典的key
                    #content_ls = content_ls.replace(ls_url,'----'+ls_urls[ls_url])   #替换掉文本中的链接文本 
                    urls.append(ls_urls[ls_url]) #把真实链接存入链接列表
                    urls_text.append(ls_url)

                

            if ls_img:
                #如果有图片
                #print('img------------',ls_img)
                for ls_1 in ls_img:
                    imgs.append(ls_1)


        #print('链接文本----------------',urls_text)
        #print('真实链接----------------',urls)
        for x in range(len(cts)):
            for i in range(len(urls_text)):
                #清除链接中的空格，a下链接文本有的网址，莫名其妙竟然有空格
                urls_text[i] = re.sub('\s','',urls_text[i])
                if urls_text[i] == cts[x] and cts[x] != urls[i]:
                    print(cts[x],'替换成---------',urls[i])
                    cts[x] = urls[i] 
                #如果内容在链接文本里出现 ，替换成 原始链接 

        
        
        num_urls = len(urls)
        num_imgs = len(imgs)
        #num_cts = len(content_text)

        if num_imgs == 0 and num_urls == 0:
            #如果图片和链接都没有(只有文字)，则不采集
            yes_or_no = False
        if self.is_keyword_valid(title,True):
            #但是如果含有标题 关键字，则采集
            yes_or_no = True
            
        #print('yes_or_no-------------',yes_or_no)        
        print('原链接个数--------------',num_urls)
        print('图片个数--------------',num_imgs)
        #print('原文本个数--------------',num_cts)
        #print('原文本内容--------------',content_text)
        
        
        
        cts = self.zh_cf(cts)  #去掉文本中重复项
        urls = self.zh_cf(urls)  #去掉链接中重复项
        #----------------------------查找完所有图片/文本/链接，放入item
        item['cts_0818'] =  cts
        item['urls_0818'] = urls
        item['imgs_0818'] = imgs
        item['yon'] = yes_or_no

        yield item


        '''
        #print(contents)
        #-----------------------------------------------------------所有div节点 （少部分有），给链接
        #这种链接好像都带有0818tuan，自己的链接。考虑是否删掉
        div = contents.xpath('./div')
        if div:
            #如果有div
            print('有div------------',div.extract())
            #临时url  
            url_ls = div.xpath('./a/@href')
            if url_ls:
                #如果有链接，一般有div就有链接
                urls.append('div中的链接--' + url_ls.extract_first())
        #------------------------------------------------------------整个内容大块的text,给内容
        #全部文本
        all_ct = contents.xpath('string(.)').extract()
        print(type(all_ct))
        print('全部1---------',all_ct)
        print(len(all_ct),'个----------------')
        print(len(all_ct[:-4]),'个----------------')
        for i in all_ct[:-5]:
            all_ct2 = ''.join(i.split())
            print('全部2---------',all_ct2)

        text = contents.xpath('./text()')
        for i in text.extract():
            #去除 '\r\n                '这样的文本
            #b_ls = i.replace('\n','').replace('\r','').replace(' ','')
            b_ls = "".join(i.split())
            if b_ls != '':
                #如果有内容，  
                print('大块中的文本 ------------',b_ls)
                content_text += b_ls

        #-------------------------------------------------------查找所有段落，找链接、图片
        p = contents.xpath('./p')
        #临时P_ls,全部展开,删除后5个P段落
        p_ls = p.extract()[:-5]
        for i in range(len(p_ls)):  #---------------------------遍历所有段落
            #如果到了P 段，如何写 xpath 续写后面的，？
            str_1 = './p[{}]/text()'.format(i+1) #----------------查找段落中的文本
            text_1 = contents.xpath(str_1).extract_first()  #文本给内容
            if text_1:
                #如果有内容，内容先不记录，再看如何判断放入哪些文本进去
                c_ls = "".join(text_1.split())
                content_text += c_ls
                print('P 中的 文本----------',c_ls)
            #--------------------------------------------------------查找段落的是否有链接
            str_2 = './p[{}]/a/@href'.format(i+1) #获取P段落下a节点的href，一般是链接,有下面两种链接
            #http://m.0818tuan.com/jd/?u=https%3A%2F%2Fitem.jd.com%2F51501863225.html
            #http://m.0818tuan.com/suning/?visitUrl=https%3A%2F%2Fproduct.suning.com%2F0000000000%2F10310212467.html
            text_2 = contents.xpath(str_2).extract()  #给链接,也要给内容,可能有多个链接
            if text_2:
                #如果找到了 链接，则放入 url列表
                for x in text_2:
                    url_ls = self.url_zh(x)
                    print('链接----------',url_ls)
                    urls.append('P段落中的链接--' + url_ls)
                #给内容
                    content_text = content_text + url_ls + '\n'
            #-------------------------------------------------------查找段落是否有图片内容
            str_3 = './p[{}]/img/@src'.format(i+1)  #获取图片链接
            text_3 = contents.xpath(str_3).extract_first()
            if text_3:
                #如果有图片
                imgs.append(text_3)
                print('图片地址-----------',text_3)


        #----------------------------查找完所有图片/文本/链接，放入item
        item['content_0818'] = content_text
        item['url_0818'] = urls
        item['imgs_0818'] = imgs
        
        if len(p) > 6:
            #去掉后面5个 P段落
            print('警告-----------大于6个段落')
            for i in range(len(p[:-5])):
                cc_1 = './p[{}]/text()'.format(i)
                print('cc_1-------------',cc_1)
                cc_2 = contents.xpath(cc_1).extract_first()
                print('cc_2-------------',cc_2)
                #如果有内容
                if cc_2:
                    cc_a = re.sub(r'(<br/?>\s*\n?)+', '@#@',cc_2)
                    cc_b = cc_a.replace('@#@','\n')
                    print('大于6个段落里的内容有---------------',cc_b)
                    #先不管图片
                    item['content_0818'] = cc_b
            yield item

            src = contents.xpath('./p[1]/img/@src').extract()
            if len(src) > 0:
                #找图片，如果没有，则跳出循环，如果有，则存入列表，因为可能有多张图片
                for i in range(len(src)):
                    imgs.append(src[i])
                print(imgs)
                item['imgs_0818'] = imgs
            else:
                print('没有图片')
        
        '''



        '''    
        #文本内容
        content_text1 = contents.xpath('./p[1]')
        print('获取所有文本--------------',content_text1.xpath('string(.)'))
        content_text = contents.xpath('./p[1]/text()').extract_first()
        #print(content_text)
        if content_text:
            #有的页面不是再第一个P 字节下，奇怪。比如 http://www.0818tuan.com/xbhd/233885.html
            # b  <br/> 用@#@ 代替
            b = re.sub(r'(<br/?>\s*\n?)+', '@#@',content_text)
            c = b.replace('@#@','\n')
            print('content_text-------------',c)
            #如果有为文本，则传给item
            item['content_0818'] = c
        #内容回车时，是空的。怎么解决，字符串替换！

        #文中的链接  /a/text()
        #for i in contents.find('a'):
            #href = i.xpath('/')
            #print('链接-------------->',i)
            #待写
        '''
        

    def parse_huodong():
        ''' 抓取 最新促销活动 '''
        pass

