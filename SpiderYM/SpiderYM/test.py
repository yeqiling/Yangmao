# -*- coding: utf-8 -*-
import sys,re


#print(u'你好')

list1=['aaa', '', 'bb', '', '     ', ' ']
list1=[x for x in list1 if x.strip()]
#print(list1)
'''
list2 = ['\r\n                ', ' ', '链接地址：', '链接', '\n\t', '\n\t', '\n\t', '\r\n', '\r\n     (adsbygoogle = window.adsbygoogle || []).push({});\r\n', 'OnitsukaTiger鬼塚虎GSM女子运动休闲鞋，316元', '空调101-100神 券', '>>']
list2=[x for x in list2 if x.strip().strip('\n\t').strip('\r\n')]
print(list2)




def is_keyword_valid(text,check_type=False):
    #默认模式：标题，只匹配 不包含的关键字
    #其他：匹配 包含与不包含的关键字
    KEYWORD = {
            'include': r'密令|红包|洪水|大水|有水|速度|神券|京豆|好价|bug|\d+元|\d+券|\d+减\d+|\d+-\d+',
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

title = '速度来啊'
print(is_keyword_valid(title))
'''

cts1 = ['进口护舒宝Always液体卫生巾日用18片*2，59，适合刚需', \
    'https://uland.taobao.com/coupon/edetail?activityId=91a373491a11439598ae49e0f4cf23a8&itemId=585406916911&pid=mm_46736561_19694158_68262194', \
    '进口护舒宝Always液体卫生巾日用18片*2，59，适合刚需 ', ' ', 'https://uland.taobao.com/coupon/edetail?activ...']

cts = ['SummerSale：REDDRAGONFLY红蜻蜓WTA40721/22男士正装皮鞋，低至126.75元', \
    '\r\n                ,\r\n                ,               ,\r\n                ,\r\n                ,                ,\r\n                ,\r\n                ,\r\n              ', \
        'https://item.jd.com/24673170402.html', '链接地址：,\n,真皮材质，系带开合~                            ', \
            ' ', 'https://item.jd.com/24673170402.html', '这款鞋采用牛皮材质，手感柔软舒适。打蜡处理，耐磨防 水。系带开合，结实耐用。',\
                 'https://item.jd.com/24673170402.html', '当前售价219元，现可享满4件立减最低1件价格，叠加领取 满399减150元优惠券，到手价格507元，折合每件低至126.75元，喜欢可入~', \
                     '京东', '\r\n,\r\n,\r\n,\r\n', '\r\n     (adsbygoogle = \window.adsbygoogle || []).push();\r\n',\
                          '上一篇：', '支付婊果然是大毛', '下一篇：', \
                              '包邮款补充，19.2，修正脱毛膏100g', '来源\r\n                  ,线报有时效性，及时参加，以免失效！\r\n                  ', '>>']

bb = list()
print('原有--------------',len(cts))
for x in cts:
    #b = x.replace(' ','')
    #b = re.sub(' ','',x) #去除空格
    #b = re.sub('\t','',b) #去除\t
    #b = re.sub('\n','',b)#去除\n
    #b = re.sub('\r','',b)#去除\r
    #b = re.sub(',','',b)#去除 
    r1 = re.compile('\s|,')
    b = re.sub(r1,'',x)
    
    
    if b == '':
        continue
    if '...' in b:
        print('...')
        continue
    print(b)
    bb.append(b)

#bb = list(set(bb))
print('原有--------------',len(bb))
print(bb[:-7])
