---
layout: post
title: 字符串匹配相关算法
author: "R. Liao" 
categories: acm
tags: 字符串匹配
---

### 字符串匹配算法-单模式匹配

#### 准备代码
```
#include<iostream>
#include<string>
#include<cstring>
#include<cstdio>
using namespace std;
const int N=100000;//文本串的最大长度
const int M=100;//模式串的最大长度
int n;//文本串的实际长度
int m;//模式串的实际长度
char T[N];//文本串
char P[M];//模式串
int pre[N];//kmp里面的前缀函数
```

#### 1 朴素匹配    
若串T中从第s（S 的下标0≤s<n-m+1）个字符起，存在和串P相同的子串，  
则称匹配成功，返回第一个这样的子串在串T中的下标，否则返回-1  

##### 代码实现
```
int Index_BF()
{
    int s=0 , j= 0;
    while(s<= n-m)
    {
        if ( T[s+j] == P[j] )
            j++;    // 一个字符匹配，继续比较后一字符
        else
        {
            s++;
            j = 0;    // S移动一个位置，重新开始新的一轮匹配过程，模式P的指针回到首部
        }
        if ( j == m )
            return s;   // 匹配成功，返回下标
    }
    return -1;  // 串T中不存在和串P相同的子串
}
```

#### 2 Sunday算法：  
在匹配过程中，模式串并不被要求一定要按从左向右进行比较还是从右向左进行比较；  
它在发现不匹配时，算法能跳过尽可能多的字符以进行下一步的匹配，从而提高了匹配效率。  
Sunday算法思想跟BM算法很相似，在匹配失败时关注的是文本串中参加匹配的最末位字符的下一位字符。
*如果该字符没有在匹配串中出现，则直接跳过，即移动步长 = 模式串的长度+1；
*否则，移动步长 = 模式串中最右端的该字符到模式串末尾的距离+1。

##### 代码实现
```
int sunday()
{
    int n = strlen(T);       //文本串的长度
    int m = strlen(P);      //模式串的长度
    int next[256] = {0};   //记录模式串中每个字符到最右边的最短距离+1的值

    for (int j = 0; j < 256; ++j)
    {
        //将每个字符到最右边的最短距离+1的值全部初始化为m+1，即最大值
        next[j] = m + 1;
    }

    for (int j = 0; j < m; ++j)
    {
        //记录模式串中每个字符到最右边的最短距离+1
        //例如：p = "abcedfb"
        //next = {7 1 5 4 3 2 8 8 8 8 8 ........}
        next[ (int)P[j] ] = m - j;
    }
    int pos = 0;
    while (pos < (n - m + 1)) //末端对齐
    {
        int i = pos;
        int j;
        for (j = 0; j < m; ++j, ++i)
        {
            if (T[i] != P[j])
            {
                //不等于就跳跃，跳跃是核心
                pos += next[(int)T[pos + m] ];
                break;
            }
        }
        if ( j == m )
            return pos;
    }
    return -1;
}
```

#### 3 ZZL算法：
首先在文本串T中查找模式串P的首字母；  
每找到一个则将它的位置存储，然后依次提取这些位置；  
从这些位置开始继续匹配模式串P。  
对于频繁使用的要匹配的主串和模式串来说；  
由于预先保存了模式串在主串中的所有存储位置，所以匹配速度会非常快。

##### 代码实现
```
int k;    //记录为模式串P首字母在主串中出现的次数
int v;    //记录模式串P首字母在主串中出现的次数
int x[N];   //模式串P首字符在文本串中的所有出现位置，并将其保存在一个数组x中
int s[N];  //模式串在文本串中匹配时，记录想x[i]的下标

int  zzl()
{
    int n = strlen(T);       //文本串的长度
    int m = strlen(P);      //模式串的长度
    //查找模式串P首字符算法
    k = 0;
    for(int i=0; i<n-m+1; i++)
    {
        if(T[i] == P[0])
        {
            x[k] = i;
            k++;
        }
    }

    //匹配算法
    v=0;
    int j;
    for(int i=0; i<k; i++)
    {
        for(j=1; j<m; j++)
        {
            if(T[ (x[i]+j) ] != P[j])
            {
                break;
            }
        }
        if(j == m)
        {
            s[v] = i;
            v++;
        }
    }
    return v;
}
```

#### 4 RK算法：
通过对字符串进行哈希运算（散列运算）；  
即给文本中模式长度为m的字符串哈希出一个数值；  
然后只需比较这个数值即可；  
之后在数值的基础上再用朴素算法比较字符串。

##### 代码实现
```
bool NativeStringMatcher(const char *T, int s, const char *P)//朴素匹配算法，Rabin_Karp调用
{
    int m = strlen(P);
    int j;
    for (j = 0; j < m; j++)
    {

        if (T[s+j] != P[j])
        {
            return false;
        }
    }
    if (j == m)
    {
        return true;
    }
    return false;
}

void Rabin_Karp(int d, int q)//RabinKarp算法
{
    int n = strlen(T);
    int m = strlen(P);

    int h = 1;
    for(int i = 0; i < m - 1; i++) //计算h=d^(m-1) mod q
    {
        h *= d;     //h=h*d，pow可能会越界，所以用乘法
        if (h >= q)
        {
            h %= q;     //h=h % q
        }
    }
    int p = 0;
    int t = 0;
    for (int i = 0; i < m; i++)     //预处理，计算p和t
    {
        p = (d * p + (P[i] - '0')) % q;     //P[i] - '0'就是将字符转换为数字
        t = (d * t + (T[i] - '0')) % q;
    }

    for (int i = 0; i < n - m+1; i++)
    {
        printf("t%d = %d\n", i, t);
        if (p == t)
        {
            if (NativeStringMatcher(T,i, P))
            {
                printf("匹配位置是：%d\n", i);
            }
            else
            {
                printf("伪命中点：%d\n", i);
            }
        }

        if (i < n - m)
        {
            t = (d * (t - h * (T[i] - '0')) + T[i + m] - '0') % q;
            if (t < 0)
            {
                t += q;
            }
        }
    }
}

```

#### 5 KMP算法：
在发生失配时，文本串不需要回溯；  
而是利用已经得到的“部分匹配”结果将模式串右移尽可能远的距离，继续进行比较。  
这里要强调的是：
*模式串不一定向右移动一个字符的位置；  
*右移也不一定必须从模式串起点处重新试匹配；  
即模式串一次可以右移多个字符的位置，右移后可以从模式串起点后的某处开始试匹配。

##### 代码实现
```
//计算模式P的前缀函数
void compute_preflx( )
{
    int k=0;    //计算模式子串的最长前缀
    pre[1] = 0;     //前缀函数，从下标1开始
    for( int q = 2; q <= m; ++q )   //对模式串从第2个字符开始计算其前缀函数值
    {
        while( k > 0 and P[k+1] != P[q] )   //没有最大的前缀了
            k = pre[k];
        if( P[k+1] == P[q])
            k ++;
        pre[q] = k;
    }
    for( int i=1; i<=m; ++i )
        cout<<pre[i]<<"  ";
    cout<<endl;
}

void kmp( )
{
    int q = 0;      //匹配的字符个数，也是作为模式p的下标使用的
    compute_preflx();   //计算出模式p的前缀函数
    for( int i = 1; i<=n; ++i )    //对文本字符从左向右扫描，指针i是不回缩的
    {
        while( q >0 and P[q+1] != T[i] )     //当模式p中的下一个字符不与文本字符匹配时，
            q = pre[q];     //模式p的下标去要回缩
        if( P[q+1] == T[i] )  //当模式p中的下一个字符与文本字符匹配时
            q++;    //将模式p的下标+1
        if( q == m )    //  即模式p的所有字符都与文本字符匹配
        {
            cout<<"s="<<i-m<<endl;    //打印出有效位移s
            q = pre[q];         //寻找下一个匹配
        }
    }
}
```

#### 6 Horspool算法：  
对于每个文本搜索窗口，  
将窗口内的最后一个字符（例如β）与模式串的最后一个字符进行比较。  
如果相等，则继续从后向前验证其他字符，直到完全相等或者某个字符不匹配。  
然后，无论匹配与否，都将根据β在模式串的下一个出现位置将窗口向右移动。

##### 代码实现
```
void HorspoolMatch()
{
    int n = strlen(T);       //文本串的长度
    int m = strlen(P);      //模式串的长度

    if (m > n)
    {
        return ;
    }

    short skip[256];   //记录模式串中每个字符到最右边的最短距离的值
    for(int i = 0; i < 256; i++)
    {
        skip[i] = m;
    }

    //计算模式串P中的每个字符到最右边的最短距离
    for(int i = 0; i < m - 1; i++)
    {
        skip[P[i]] = m - i - 1;
    }

    int pos = 0;
    while(pos <= n - m)
    {
        int j = m -1;  //从后面向前面匹配
        while(j >= 0 && T[pos + j] == P[j])
        {
            j--;
        }
        if(j < 0)
        {
            cout<<"an occurrence at:"<<pos<<endl;
        }
        pos = pos + skip[T[pos + m -1]];    //跳到m-1字符在模式串最右边的位置
    }
}

```

#### 测试代码
```
int main()
{
    while(gets(T))
    {
        gets(P);
        kmp();
        HorspoolMatch();
        Rabin_Karp(10, 13);
        zzl();
        sunday();
    }
    return 0;
}
```
