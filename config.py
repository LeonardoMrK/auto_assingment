#!/usr/bin/env python
# coding: utf-8
# @Author  : Mr.K
# @Software: PyCharm Community Edition
# @Time    : 2019/12/29 13:04
# @Description: 标注结果保存路径、词典路径、文章路径以及标签设置


#标注结果保存路径
save_dir='D:\\project\\pycharmworkspace\\auto_assingment\\output\\'
#词典路径
dic_dir='D:\project\pycharmworkspace\\auto_assingment\dics'
#待处理文章路径
essay_dir='D:\project\pycharmworkspace\\auto_assingment\essays\essay_date.txt'


#根据dics文件夹中存放的词典内容顺序添加tag
#比如0.txt为食品词典，1.txt为添加剂词典，2.txt为地点词典，3.txt为人名词典
#其对应的tag分别为'FOOD','ADD','LOC','PER'，则设置应该为如下所示：
tag_config=['FOOD','ADD','LOC','PER']