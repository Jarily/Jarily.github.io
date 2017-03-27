# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 14:33:35 2017

@author: Jarily
"""

import os


def change(filename):
    f=open(filename,'r',encoding='utf-8')
    lines=f.readlines()
    text=[]
    flag=0
    flag1=0
    for line in lines:
        if 'categories:' in line:
            if flag==0:
                text.append('categories: research\n')
                flag=1
            #print(line)
        elif 'guid: urn' in line:
            pass
        elif 'author: "R. Liao"' in line:
            if flag1==0:
                text.append('author: "R. Liao" \n')
                flag1=1
        else:
            text.append(line)
    #print(text)
    if flag==0:
        text.insert(3,'categories: research\n')
    if flag==0:
        text.insert(4,'author: "R. Liao" \n')
    f.close()
    f=open(filename,'w',encoding='utf-8')
    f.writelines(text)
    f.close()
def main():
    dir=os.getcwd()       #当前目录
    lists = os.listdir(dir)  #列出目录下的所有文件和目录
    #print(lists)
    
    for ls in lists:
        if ls[-8:]=='markdown' or ls[-2:]=='md':
            change(ls)
        
        #print(ls[-8:])
        #print(ls[-2:])
        #if ls[-8:])
        
    

if __name__=='__main__':
    main()