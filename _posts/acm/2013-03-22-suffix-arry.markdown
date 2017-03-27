---
layout: post
title:   实现后缀数组的倍增算法和DC3算法
author: "R. Liao" 
categories: acm
tags: 后缀数组
---


### 数据结构：后缀数组(Suffix_Array)     

#### 子串  
字符串S的子串r[i..j]，i≤j，表示r串中从i到j这一段，  
也就是顺次排列r[i],r[i+1],...,r[j]形成的字符串;     

#### 后缀  
后缀是指从某个位置i开始到整个串末尾结束的一个特殊子串;  
字符串r的从第i个字符开始的后缀表示为Suffix(i),也就是Suffix(i)=r[i...len(r)];

#### 后缀数组SA  
后缀数组保存的是一个字符串的所有后缀的排序结果;  
其中SA[i]保存的是字符串所有的后缀中第i小的后缀的开头位置;  
#### 名次数组Rank  
名次数组Rank[i]保存的是后缀i在所有后缀中从小到大排列的“名次”;  
后缀数组是"排第几的是谁",名次数组是"排第几",即后缀数组和名次数组为互逆运算;  

### 算法  
* (1)倍增算法:  
用倍增的方法对每个字符开始的长度为2^k的子字符串进行排序，求出排名，即rank值。  
k从0开始，每次加1，当2^k大于n以后，每个字符开始的长度为2^k的子字符串便相当于所有的后缀。  
并且这些子字符串都一定已经比较出大小，即rank值中没有相同的值，那么此时的rank值就是最后的结果。  
每一次排序都利用上次长度为2^k-1的字符串的rank值，  
那么长度为2^k的字符串就可以用两个长度为2^k-1的字符串的排名作为关键字表示，  
然后进行基数排序，便得出了长度为2^k的字符串的rank值。  

* (2)DC3算法：  
①先将后缀分成两部分，然后对第一部分的后缀排序;  
②利用①的结果，对第二部分的后缀排序;  
③将①和②的结果合并，即完成对所有后缀排序;  

### 时间复杂度    
倍增算法的时间复杂度为O(nlogn),DC3算法的时间复杂度为O(n);  
从常数上看，DC3算法的常数要比倍增算法大;  

### 空间复杂度  
倍增算法和DC3算法的空间复杂度都是O(n);  
倍增算法所需数组总大小为6n,DC3算法所需数组总大小为10n;  

### RMQ(Range Minimum/Maximum Query)问题  
对于长度为n的数列A，回答若干询问RMQ(A,i,j)(i,j<=n)，  
返回数列A中下标在i,j里的最小(大）值，  
也就是说，RMQ问题是指求区间最值的问题。  

### LCA(Least Common Ancestors)最近公共祖先问题  
对于有根树T的两个结点u、v，  
最近公共祖先LCA(T,u,v）表示一个结点x，  
满足x是u、v的祖先且x的深度尽可能大。  
另一种理解方式是把T理解为一个无向无环图，  
而LCA(T,u,v）即u到v的最短路上深度最小的点。

### RMQ标准算法  
先规约成LCA(Lowest Common Ancestor),再规约成约束RMQ，O(n)-O(q);  
首先根据原数列，建立笛卡尔树，  
从而将问题在线性时间内规约为LCA问题;  
LCA问题可以在线性时间内规约为约束RMQ，  
也就是数列中任意两个相邻的数的差都是+1或-1的RMQ问题;  
约束RMQ有O(n)-O(1)的在线解法，故整个算法的时间复杂度为O(n)-O(1);

### height数组  
定义height[i]=suffix(sa[i-1])和suffix(sa[i])的最长公共前缀，  
也就是排名相邻的两个后缀的最长公共前缀;  

**那么对于j和k，不妨设rank[j]<rank[k],则有以下性质**  
suffix(j)和suffix(k)的最长公共前缀为:     
height[rank[j]+1],height[rank[j]+2],height[rank[j]+3],…,height[rank[k]]中的最小值;

### 代码  

```

#include<iostream>
#include<cstring>
#include<cstdlib>
#include<cstdio>
#include<climits>
#include<algorithm>
using namespace std;

const int N=100010;

/**************倍增算法**************************

int wa[N],wb[N],wv[N],__ws[N];

int cmp(int *r,int a,int b,int l)
{
    return r[a]==r[b]&&r[a+l]==r[b+l];
}

void da(int *r,int *sa,int n,int m)
{
    int *x=wa,*y=wb,*t;
    for(int i=0; i<m; i++)
        __ws[i]=0;
    for(int i=0; i<n; i++)
        __ws[x[i]=r[i]]++;
    for(int i=1; i<m; i++)
        __ws[i]+=__ws[i-1];
    for(int i=n-1; i>=0; i--)
        sa[--__ws[x[i]]]=i;
    for(int j=1,p=1; p<n; j*=2,m=p)
    {
        p=0;
        for(int i=n-j; i<n; i++)
            y[p++]=i;
        for(int i=0; i<n; i++)
        {
            if(sa[i]>=j)
                y[p++]=sa[i]-j;
        }
        for(int i=0; i<n; i++)
            wv[i]=x[y[i]];
        for(int i=0; i<m; i++)
            __ws[i]=0;
        for(int i=0; i<n; i++)
            __ws[wv[i]]++;
        for(int i=1; i<m; i++)
            __ws[i]+=__ws[i-1];
        for(int i=n-1; i>=0; i--)
            sa[--__ws[wv[i]]]=y[i];
        t=x,x=y,y=t,p=1,x[sa[0]]=0;
        for(int i=1; i<n; i++)
        {
            x[sa[i]]=cmp(y,sa[i-1],sa[i],j)?p-1:p++;
        }
    }
    return;
}
**************倍增算法**************************/


/***************DC3算法**************************/

#define F(x) ((x)/3+((x)%3==1?0:tb))
#define G(x) ((x)<tb?(x)*3+1:((x)-tb)*3+2)

int wa[N],wb[N],wv[N],_ws[N];

int c0(int *r,int a,int b)
{
    return r[a]==r[b]&&r[a+1]==r[b+1]&&r[a+2]==r[b+2];
}

int c12(int k,int *r,int a,int b)
{
    if(k==2)
        return r[a]<r[b]||r[a]==r[b]&&c12(1,r,a+1,b+1);
    else
        return r[a]<r[b]||r[a]==r[b]&&wv[a+1]<wv[b+1];
}

void sort(int *r,int *a,int *b,int n,int m)
{
    for(int i=0; i<n; i++)
        wv[i]=r[a[i]];
    for(int i=0; i<m; i++)
        _ws[i]=0;
    for(int i=0; i<n; i++)
        _ws[wv[i]]++;
    for(int i=1; i<m; i++)
        _ws[i]+=_ws[i-1];
    for(int i=n-1; i>=0; i--)
        b[--_ws[wv[i]]]=a[i];
    return;
}

void dc3(int *r,int *sa,int n,int m)
{
    int *rn=r+n,*san=sa+n,ta=0,tb=(n+1)/3,tbc=0,p;
    r[n]=r[n+1]=0;
    for(int i=0; i<n; i++)
    {
        if(i%3!=0)
            wa[tbc++]=i;
    }
    sort(r+2,wa,wb,tbc,m);
    sort(r+1,wb,wa,tbc,m);
    sort(r,wa,wb,tbc,m);
    p=1,rn[F(wb[0])]=0;
    for(int i=1; i<tbc; i++)
    {
        rn[F(wb[i])]=c0(r,wb[i-1],wb[i])?p-1:p++;
    }
    if(p<tbc)
        dc3(rn,san,tbc,p);
    else
        for(int i=0; i<tbc; i++)
            san[rn[i]]=i;
    for(int i=0; i<tbc; i++)
    {
        if(san[i]<tb)
            wb[ta++]=san[i]*3;
    }
    if(n%3==1)
        wb[ta++]=n-1;
    sort(r,wb,wa,ta,m);
    for(int i=0; i<tbc; i++)
        wv[wb[i]=G(san[i])]=i;
    int i,j;
    for(i=0,j=0,p=0; i<ta && j<tbc; p++)
    {
        sa[p]=c12(wb[j]%3,r,wa[i],wb[j])?wa[i++]:wb[j++];
    }
    for(; i<ta; p++)
        sa[p]=wa[i++];
    for(; j<tbc; p++)
        sa[p]=wb[j++];
    return;
}
/***************DC3算法**************************/


int rank[N],height[N];

void calheight(int *r,int *sa,int n)
{
    int i,j,k=0;
    for(int i=1; i<=n; i++)
        rank[sa[i]]=i;
    for(int i=0; i<n; height[rank[i++]]=k)
    {
        for(k?k--:0,j=sa[rank[i]-1]; r[i+k]==r[j+k]; k++);
    }
    return;
}

int RMQ[N];
int mm[N];
int best[20][N];

void initRMQ(int n)
{
    int i,j,a,b;
    for(mm[0]=-1,i=1; i<=n; i++)
        mm[i]=((i&(i-1))==0)?mm[i-1]+1:mm[i-1];
    for(i=1; i<=n; i++) best[0][i]=i;
    for(i=1; i<=mm[n]; i++)
        for(j=1; j<=n+1-(1<<i); j++)
        {
            a=best[i-1][j];
            b=best[i-1][j+(1<<(i-1))];
            if(RMQ[a]<RMQ[b]) best[i][j]=a;
            else best[i][j]=b;
        }
    return;
}

int askRMQ(int a,int b)
{
    int t;
    t=mm[b-a+1];
    b-=(1<<t)-1;
    a=best[t][a];
    b=best[t][b];
    return RMQ[a]<RMQ[b]?a:b;
}

int lcp(int a,int b)
{
    int t;
    a=rank[a];
    b=rank[b];
    if(a>b)
    {
        t=a;
        a=b;
        b=t;
    }
    return(height[askRMQ(a+1,b)]);
}

```