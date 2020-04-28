import base64
f=open('F://YOLOv4-1.png','rb') #用二进制方式打开图片
ls_f=base64.b64encode(f.read())#读取文件内容，转换为base64编码
f.close()
print(ls_f)
# 把图片存入markdown
'''
基础用法：！[avatar](data:image/png;base64,base64转换后的码)
插入的一长串字符串会把整个文章分隔开，可以把大段的base64字符串放在文章末尾，在文章中通过一个id来调用
高级用法：！[avatar][base64str]
[base64str]:data:image/png;base64,base64转换后的码
'''