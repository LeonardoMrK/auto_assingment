#!/usr/bin/env python
# coding: utf-8
# @Author  : Mr.K
# @Software: PyCharm Community Edition
# @Time    : 2019/12/28 10:10
# @Description:输入文章与词典，实现根据词典中的元素对文章进行序列标注

import re
import os
import time
from config import tag_config,dic_dir,essay_dir,save_dir



def index_get(essay,elements):
    """
    索引获取函数，根据词典内容返回在文章与词典中同时出现的元素的索引，在tag_processor中被调用
    :param essay: 一篇文章，要求无空格，全篇文章写在一行中，str格式，如'原因是CPU电路板故障，部分电子元件受损，需要对CPU电路板更换新的电子元件'
    :param elements: 要标注的数据词典（注意只能是一个词典），每个元素占一行，格式为str，每个元素用|分隔，如“电路板|CPU”
    :return: 返回该词典与文章中同时存在的词的索引（可能存在重复），如[(3, 6), (6, 9), (12, 14), (24, 27), (27, 30)],list
    格式，每个元素都打包成了元组格式
    """
    index_result=[]
    temp_result=[(m.group(), m.span()) for m in re.finditer(elements, essay)]
    #print("temp_result",temp_result)#result格式为[('CPU', (3, 6)), ('电路板', (6, 9)), ('部分', (12, 14)), ('CPU', (24, 27)), ('电路板', (27, 30))]
    for each in temp_result:
        index_result.append(each[1])#只要索引，不管索引对应的元素是啥
    #print("index_result",index_result)#[(3, 6), (6, 9), (12, 14), (24, 27), (27, 30)]
    return index_result


def save_function(dir_path,essay,tags):
    """
    保存函数，用于保存标注结果
    :param dir_path: 结果保存路径
    :param essay: 经过essay_processor处理后的原文数据
    :param tags: 经过tag_processor处理后的标注序列
    :return: None
    """
    # 写入标注好的数据到txt文档
    with open('%stagged_data.txt'%(dir_path), 'w', encoding='utf-8') as f:#注意这种保存路径的处理方式
        for char, tag in zip(essay, tags):#每一行一个字加一个空格加一个tag
            f.write(char + '\t' + tag + '\n')  # 在这里实现空格换行


def tag_processor(essay,elements):
    """
    标注函数，根据输入的文章数据以及要字典中元素的索引生成标注数据
    :param essay: 文章，要求为无空格的str变量，全篇文章写在一行中，如'原因是CPU电路板故障，部分电子元件受损，需要对CPU电路板更换新的电子元件'
    :param elements: 字典集合，要求为要标注的数据元素词典集合，list格式，每类词典用“，”分隔，一个词典中的不同元素用“|”分隔，如['电路板|CPU','部分|新的']
    :return:tags，返回list格式的标注序列
    """
    # 根据文章长度，生成list格式的标注序列
    tags = ['O'] * len(essay)  # 对所有语料都标注“O”
    for j in range(len(elements)):#循环处理每个词典
            #文章依次对照词典进行标注
            ele_index=index_get(essay, elements[j])#调用index获取函数，返回的是词典对应的索引
            #print('essay:', essay)  # 原始语料
            #print('ele_index:', ele_index)  # 选中的标注元素的索引
            #print('-------------------------------------------------------------------------------------')
            for each in ele_index:#获取每个元素的首尾索引
                start_index = each[0]
                end_index = each[1]
                # print(start_index, end_index)
                for i in range(start_index, end_index):  # 根据首尾索引修改标注序列，注意这里尾部index不需要+-1,在上一个函数输出时就考虑到了从0count的因素
                        tags[i] = 'I-'+tag_config[j]#先给所有字都打上结束标签
                        tags[start_index] = 'B-'+tag_config[j]#最后给首字打上开头标签
    return tags


def dic_generator(dic_dir):
    """
    字典集合生成函数，生成可用于标注的字典
    :param dic_dir: 原始字典保存路径，格式为一个txt文件保存一类词，一个词占一行，每个文件采用utf-8编码【文件需要按照类别排序】
    :return: 返回list格式的字典集合，类似：['电路板|CPU','部分|新的']，不同字典用“，”分隔
    """
    dics_list=[]
    files = os.listdir(dic_dir)#获取文件夹内所有文件，按照名称排序，这也是为什么词典要使用数字重新命名以及标签要按顺序设置的原因
    #print(files)
    for each_file in files:
        dic_str = ''
        if not os.path.isdir(each_file):#判断不是文件夹才打开
            with open(dic_dir+'/'+each_file,'r',encoding='utf-8') as f:
                lines=f.readlines()#使用readlines方法，返回格式为list的数据
                for each in lines:
                    temp1=each.replace('\t','')#替换掉空格
                    temp2=temp1.replace('\n','')#替换掉换行
                    #print(temp2)
                    dic_str+=temp2+'|'
        dics_list.append(dic_str)
    return dics_list


def essay_processor(eassy_dir):
    """
    文章处理函数，可把原始文件中的多行文本合并为一行，生成可用于标注的文章数据
    :param eassy_dir:文章路径，格式为一篇文章占一行，中间无空格，采用utf-8编码
    :return:将所有文章合并为一行，返回str格式的变量
    """
    one_line=''#用str格式的遍历保存数据，把所有数据都存为一行
    with open(eassy_dir,'r',encoding='utf-8') as f:
        while True:
            each_line=f.readline()#用readline方法一次读取一行
            if each_line:
                temp=each_line.replace('\n','')#去掉换行符
                one_line+=temp
            else:
                break
    return one_line





if __name__=='__main__':
    print('tagging start...')
    time_start=time.time()
    essies_on_oneline=essay_processor(essay_dir)#获取文章数据
    dics=dic_generator(dic_dir)#获取字典集
    tagged_data=tag_processor(essies_on_oneline, dics)#获取标注数据
    save_function(save_dir,essies_on_oneline,tagged_data)#保存标注数据
    time_end=time.time()
    print('complete.\ntime cost:',time_end-time_start,'s')

