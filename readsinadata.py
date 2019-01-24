#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import os
import re
import pickle
import data_helper

if __name__ == "__main__":
    filename="./data/sinanews/"
    files = os.listdir(filename)
    #headlinetxt = open('./data/sinatext.txt','w')
    labels=[]
    headline=[]
    texts=[]
    totaltext=[]
    rule1 = r"\[emotion_votes\](.+?)\[headline\]"
    rule2 = r"\[headline\](.+?)\[body\]"
    rule3 = r"\[body].*"
    stopwords = data_helper.stopwordslist("./data/stopwords.txt")  # 去掉停用词
    for file in files:  # 遍历文件夹
        paths = filename + file
        # 读取文件
        infile = open(paths,'r')
        text = infile.read()
        text = re.sub(r"\n", " ", text)

        # 得到标签
        content = re.search(rule1, text)
        content = re.sub(r"( )+", " ", content.group())
        content = content.split(' ')[1:-1]
        label = [int(emt.split(':')[1]) for emt in content]
        labels.append(label)

        # #得到标题
        # headline = re.search(rule2, text)
        # headline = re.sub(r"( )+", " ", headline.group())[len('[headline]')+1:-1-len('[body]')]
        # headline.append(content)
        #print(content,file=headlinetxt)


        #得到内容
        content = re.search(rule3, text)
        content = re.sub(r"( )+", " ", content.group())[len('[body]') + 3: ]
        # texts.append(content)
        # print(content, file=headlinetxt)

        # article=headline+' '+content

        totaltext.append(content)
        infile.close()

    totaltext, labels=data_helper.segment_sentence(totaltext, labels)
    totaltext = [data_helper.remove_words(text, stopwords) for text in totaltext]
    f=open('./data/sina/sentencetext.pkl','wb')
    pickle.dump(totaltext,f)
    f.close()

    f=open('./data/sina/sentencetext_label.pkl','wb')
    pickle.dump(labels,f)
    f.close()
