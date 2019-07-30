import re
a = [1,2,3,4,5,6,7,8,9]
b = [1,3,5,7]
c = [11,33,55,77]

for i in range(len(a)):
    for x in range(len(b)):
        if b[x] == a[i]:
            a[i] = c[x]

#print(a)


d = 'https://pup.zh.cmbchina.com/mobi ... 8987003000012660534'

e = re.sub('\s','',d)  #清除空格
print(e)
