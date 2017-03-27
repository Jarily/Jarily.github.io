---
layout: post
title:  字符串-最小(大)表示法
author: "R. Liao" 
categories: acm
tags: 最小(大)表示法
---


### 问题描述    
最小(大)表示法主要用于解决判断"同构"一类问题;  

* 循环同构问题  
给出两个串:s1="babba"和s2="bbaba",其中两者均看成环状即首尾相接的;  
问：从s1的哪里断开可以得到和s2一样的串或者两者不会相同？  
本题就是从s1的第2个字符’a’后面断开,可以得到与s2一样的串;  
这个问题即为**同构问题**;

### 同构问题的解决算法  

#### (1)朴素算法(O(nm))  
即尝试s1的n个断开点,与s2进行比较,如果相同则找到同构位置,否则找不到;  
该算法仅适用于n,m规模较小情况;

#### (2)转换为模式匹配  
首先构造新的模型：S=s1+s1为主串,s2为模式串;  
如果s1和s2是循环同构的,那么s2就一定可以在S中找到匹配,否则找不到匹配则两则不能同构;  
本问题转换为模式匹配后应用KMP算法,可以在O(n+m)的时间内获得问题的解;

#### (3)最小(大)表示法  
它也可以在O(n+m)时间内求解,更大的优势还有无需KMP算法的Next数组,仅需要两个指针即可;


### 代码  

```
#include<iostream>
#include<string>
#include<cstring>
#include<cstdio>
using namespace std;

int GetMin(char *P)//用最小表示法求字符串S的最小字典序,返回字典序最小的串的首字母位置
{
    int len=strlen(P);
    int i=0,j=1,k=0;
    while(i<len&&j<len&&k<len)
    {
        int t=P[(i+k)%len]-P[(j+k)%len];
        if(!t)
            k++;
        else
        {
            if(t>0)
                i+=k+1;
            else
                j+=k+1;
            if(i==j)
                j++;
            k=0;
        }
    }
    return i<j?i:j;
}

int GetMax(char *P) //用最大表示法求字符串S的最小字典序,返回字典序最大的串的首字母位置
{
    int len=strlen(P);
    int i=0,j=1,k=0;
    while(i<len&&j<len&&k<len)
    {
        int t=P[(i+k)%len]-P[(j+k)%len];
        if(!t)
            k++;
        else
        {
            if(t>0)
                j+=k+1;
            else
                i+=k+1;
            if(i==j)
                j++;
            k=0;
        }
    }
    return i<j?i:j;
}


```