---
layout: post
title:   高精度乘法
author: "R. Liao" 
categories: acm
tags: 高精度
---

### 思想  
计算的过程几乎和最原始的列竖式做乘法相同;  
在编程处理中，先不要急于进位，在最后统一处理;  

### 规律  
一个数的第i位和另一个数的第j位相乘所得的数;  
一定是要累加到结果的第i+j位上;(i,j都是自右向左从0开始计数);  

### 代码
```
#include<iostream>
#include<cstring>
#include<cstdlib>
#include<cstdio>
#include<climits>
#include<algorithm>
using namespace std;

const int N=1000;
int a[N],b[N],res[N*2];
char x[N],y[N];
int len1,len2;

void init()
{
    len1=strlen(x);
    len2=strlen(y);
    memset(a,0,sizeof(a));
    memset(b,0,sizeof(b));
    memset(res,0,sizeof(res));
    for(int i=len1-1,j=0; i>=0; i--)
    {
        a[j++]=x[i]-'0';
    }
    for(int i=len2-1,j=0; i>=0; i--)
    {
        b[j++]=y[i]-'0';
    }
}

void solve()
{
    init();
    for(int i=0; i<len2; i++) //乘法处理
    {
        for(int j=0; j<len1; j++)
        {
            res[i+j]+=a[i]*b[j];
        }
    }

    for(int i=0; i<N*2; i++) //进位处理
    {
        if(res[i]>=10)
        {
            res[i+1]+=res[i]/10;
            res[i]%=10;
        }
    }

    bool flag=0;
    for(int i=N*2-10; i>=0; i--) //输出处理
    {
        if(flag)
            printf("%d",res[i]);
        else if(res[i])
        {
            printf("%d",res[i]);
            flag=1;
        }
    }
    if(!flag)
        printf("0");
    printf("\n");

}

int main()
{
    freopen("C:\\Users\\Administrator\\Desktop\\kd.txt","r",stdin);
    while(gets(x))
    {
        gets(y);
        solve();
    }
    return 0;
}
```