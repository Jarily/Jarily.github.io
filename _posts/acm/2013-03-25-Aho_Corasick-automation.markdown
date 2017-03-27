---
layout: post
title:   字符串匹配-AC自动机
author: "R. Liao" 
categories: acm
tags: AC自动机
---


### 基本介绍    
AC自动机(Aho_Corasick automation),为多模字符串匹配算法;    
常见的例子为给出n个单词,再给出一段包含m个字符的文章,找出有多少个单词在文章里出现过;

### 基本步骤  

#### (1)构造一棵Trie树;
根节点不包含字符,除根节点外每一个节点都只包含一个字符;  
从根节点到某一节点,路径上经过的字符连接起来,为该节点对应的字符串;  
每个节点的所有子节点包含的字符都不相同;

#### (2)构造失败指针;
设这个节点上的字母为C;  
沿着他父亲的失败指针走,直到走到一个节点,他的儿子中也有字母为C的节点;  
然后把当前节点的失败指针指向那个字母也为C的儿子;  
如果一直走到了root都没找到,那就把失败指针指向root;

* 具体操作  
先把root加入队列(root的失败指针指向自己或者NULL),    
这以后每处理一个点,就把它的所有儿子加入队列;  

#### (3)模式匹配过程;  
①当前字符匹配,表示从当前节点沿着树边有一条路径可以到达目标字符;  
此时只需沿该路径走向下一个节点继续匹配即可;　　  
目标字符串指针移向下个字符继续匹配;　　  
②当前字符不匹配,则去当前节点失败指针所指向的字符继续匹配;　　  
匹配过程随着指针指向root结束;　　  
重复这2个过程中的任意一个,直到模式串走到结尾为止;

### 补充说明    
* 当前字符无匹配,就表示当前节点的任何一条边都无法达到要匹配的字符;  
此时不能沿现有路径前进,只能回溯,回溯到存在最长的后缀字符串处;  
如果没有任何后缀字符串匹配则回溯到树根处;  
然后从当前回溯节点判断是否可以到达目标字符串中的字符;

* 由于Trie树中字符串的后缀字符串都是已知的,  
可以在Trie树结构中存储匹配失败的路径方向,  
因此只要Trie树构造完毕,就可以根据Trie树的路径进行匹配了,效率很高;

* KMP中用两个指针i和j分别表示,A[i-j+ 1..i]与B[1..j]完全相等;  
也就是说i是不断增加的,随着i的增加j相应地变化,且j满足以A[i]结尾的长度为j的字符串正好匹配B串的前j个字符;  
当A[i+1]≠B[j+1],KMP的策略是调整j的位置(减小j值)使得A[i-j+1..i]与B[1..j]保持匹配且新的B[j+1]恰好与A[i+1]匹配;  
而next函数恰恰记录了这个j应该调整到的位置;  

* 同样AC自动机的失败指针具有同样的功能;  
也就是说当模式串在Tire上进行匹配时;  
如果与当前节点的关键字不能继续匹配的时候;  
就应该去当前节点的失败指针所指向的节点继续进行匹配;


### 代码  

```
#include<iostream>
#include<cstdio>
#include<cstring>
using namespace std;

const int K=26;
const int C=55;
const int N=500010;
const int M=1000010;

struct node
{
    node *fail; //失败指针 　　
    node *next[K]; //Tire每个节点的26个子节点（最多26个字母） 　　
    int count; //是否为该单词的最后一个节点 　　
    node()//构造函数初始化 　　
    {
        fail=NULL;
        count=0;
        memset(next,NULL,sizeof(next));
    }
}*q[N]; //队列，方便用于bfs构造失败指针 　

char keyword[C]; //输入的单词 　　
char str[M]; //模式串 　　
int head,tail; //队列的头尾指针 　

void insert(char *str,node *root)//建立Trie
{
    node *p=root;
    int len=strlen(str);
    for(int i=0; i<len; ++i)
    {
        int temp=str[i]-'a';
        if(p->next[temp]==NULL)
            p->next[temp]=new node();
        p=p->next[temp];
    }
    p->count++;
}

void build_ac_automation(node *root)//初始化fail指针，BFS
{
    root->fail=NULL;
    q[head++]=root;//弹出队头
    while(head!=tail)
    {
        node *temp=q[tail++];
        node *p=NULL;
        for(int i=0; i<K; i++)
        {
            if(temp->next[i])
            {
                if(temp==root)//第一个元素fail必指向根
                    temp->next[i]->fail=root;
                else
                {
                    p=temp->fail;//失败指针
                    while(p)//2种情况结束：匹配为空or找到匹配
                    {
                        if(p->next[i])//找到匹配
                        {
                            temp->next[i]->fail=p->next[i];
                            break;
                        }
                        p=p->fail;
                    }
                    if(p==NULL)//为空则从头匹配
                        temp->next[i]->fail=root;
                }
                q[head++]=temp->next[i];//入队
            }
        }
    }
}

int query(node *root)//扫描
{
    node *p=root;//Tire入口
    int len=strlen(str);
    int cnt=0;
    for(int i=0; i<len; i++)
    {
        int index=str[i]-'a';
        while(p->next[index]==NULL && p!=root)//跳转失败指针
            p=p->fail;
        p=p->next[index];
        p=(p==NULL)?root:p;
        node *temp=p;//p不动，temp计算后缀串
        while(temp!=root&&temp->count!=-1)
        {
            cnt+=temp->count;
            temp->count=-1;
            temp=temp->fail;
        }
        i++;
    }
    return cnt;
}

int main()
{
    //freopen("C:\\Users\\Administrator\\Desktop\\kd.txt","r",stdin);
    int t;
    scanf("%d",&t);
    while(t--)
    {
        head=tail=0;
        node *root=new node();
        int n;
        scanf("%d",&n);
        getchar();
        while(n--)
        {
            gets(keyword);
            insert(keyword,root);
        }
        build_ac_automation(root);
        scanf("%s",str);
        printf("%d\n",query(root));
    }
    return 0;
}



```