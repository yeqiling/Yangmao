# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.http import Request

import re
from SpiderYM.items import SpiderymItem

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
    def is_keyword_valid(text,check_type='lala'):
        ''' 
        不符合，返回假
        符合，返回真
        lala 为备用，后面再用
        '''
        # 监控关键字
        KEYWORD = {
            'include': r'密令|红包|洪水|大水|有水|速度|神券|京豆|好价|bug|\d+元|\d+券|\d+减\d+|\d+-\d+',
            'exclude': r'权限|水.?贴|什么|怎么|怎样|不是|不能|不行|没有|反撸|求|啥|问|哪|吗|么|？'
        }

        if check_type == 'lala':
            if len(re.findall(KEYWORD['include'], text, re.I)) == 0 \
                or len(re.findall(KEYWORD['exclude'], text, re.I)) > 0:
                print(title,"----------关键字不对，排除")
                return False
            else:
                return True
        else:
            print('text-------------------',text)
            print('check_type----------------',check_type)
            return False if len(re.findall(KEYWORD['exclude'], text, re.I)) > 0 else True

    def start_requests(self):
        url_new = self.url_base + '/list-1-0.html'  #最新活动线报
        url_huodong = self.url_base + '/list-4-0.html'    #最新促销活动
        #yield Request(url=url_new,meta={"url_begin":url_new},callback=parse_new)
        yield Request(url=url_new,callback=self.parse_new)
        #yield Request(url=url_huodong,meta={"url_begin":url_huodong},callback=parse_huodong)
        #yield Request(url=url_huodong,callback=self.parse_huodong)
        #return [Request(self.start_urls,callback=self.parse_yi)] 

    def url_zh(self,str):
        #转换url，去掉 前缀
        if '=http' in str:
            print('去掉没用的')
            a = str.replace('=http','@#@')
            url_ls = 'http' + a.split('@#@')[1]  #切割
        else:
            url_ls = str  #原网址，则不切割
        return url_ls

    def cts_zh(self,ctss):
        '''转换文本
        如果文本列表，大于5个，则只取前5个
        然后，删除列表中的'/r/n' '/n/t' 和空格
        '''
        num_cts = len(ctss)
        cts = list()
        if num_cts > 5:
            #如果有很多内容，只取前5个.删掉一些没用的
            cts = ctss[:5]
        else:
            cts = ctss
        #删除空格和没用的
        cts = [x for x in cts if x.strip().strip('\n\t').strip('\r\n')]
        
        return cts

    def parse_new(self,response):
        ''' 抓取 最新活动线报 '''
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
            title = ''
            title  = cc.xpath('./@title').extract_first() #标题
            time  = cc.xpath('./span/text()').extract_first() #时间
            if url_one == '/xbhd/234233.html':
                #无用的网址，会出错
                continue
            if title == '':
                #标题为空时，跳过
                continue
            #各种判断
            if title.find('APP发布') != -1:
             #排除第一个  0818团线报网APP发布 推送、分享、交流互助都有。。。  -1是没有找到的意思
                continue

            '''    
            #判断是否符合关键字，包含或不包含
            if not self.is_keyword_valid(title,check_type='lala'):
                continue  
                    
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
        title = response.meta['title']
        if title:
            #如果有标题
            #print('title-------------------',title)
            item['title_0818'] = title
        #--------------------------------------------------------时间，没什么用
        time = response.meta['time']
        if time:
            #如果有时间
            item['time_0818'] = time


        #-----------------------------------------------------------整个内容大块，全部内容
        contents = page_ok.xpath('//div[@class="post-content"]')
        num = contents.xpath('./p').extract()   #有多少个P
        if len(num) <= 6:    #------------------------------------------------如果小于等于6个P，则只取第一个P内容
            content_ss = contents.xpath('./p[1]/descendant-or-self::*')  #把P1下的所有切割，选取下面所有子节点和本身节点
        else:
            #-----------------------------------------------------------------如果大于6个P，分解下面所有节点
            print('大于6个P--------------------------',len(num),'个')
            content_ss = contents.xpath('./descendant-or-self::*')   #注意，这里除了P还有其他的节点，比如div

        for content in content_ss:
            ls_text = content.xpath('./text()').extract_first() #文本内容
            ls_url = content.xpath('./a/@href').extract_first() #链接
            ls_img = content.xpath('./img/@src').extract_first() #图片

            if ls_text:
                #如果有文本
                if ls_text != '':     #如果不为空
                    #print('文本------------',ls_text)
                    content_text.append(ls_text) #也改成列表
            if ls_url:
                #如果有链接
                #print('url------------',ls_url)
                urls.append(self.url_zh(ls_url)) #去除链接中的网站前缀 0818tuan.com.......
            if ls_img:
                #如果有图片
                #print('img------------',ls_img)
                imgs.append(ls_img)
        
        
        num_urls = len(urls)
        num_imgs = len(imgs)
        num_cts = len(content_text)

        if num_imgs == 0 and num_urls == 0:
            #如果图片和链接都没有(只有文字)，则不采集
            yes_or_no = False
            
        print('yes_or_no-------------',yes_or_no)        
        print('原链接个数--------------',num_urls)
        print('图片个数--------------',num_imgs)
        print('原文本个数--------------',num_cts)
        print('原文本内容--------------',content_text)
        
        

        cts = self.cts_zh(content_text)  #去除文本中没用的
        urls = list(set(urls))   #去除链接中重复项

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

