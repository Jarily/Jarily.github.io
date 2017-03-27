---
layout: post
title:  流量有上下界的网络的最大流和最小流算法
author: "R. Liao" 
categories: acm
tags: 网络流
---

### 概念  
基础的网络流的每一条弧<u,v>都对应一个弧容量c(u,v)>=0;  
而有上下界的网络流中，每条弧对应两个权值b(u,v)和c(u,v),即为弧流量的下界和上界；  
很显然基础的网络流中为其特殊情况，即b(u,v)==0的时候;  

### 分析      

#### (1)最大流 
当b(u,v)>0的时候，这种有上下界的网络流不一定存在可行流；  
所以算法首先得判断该网络是否存在可行流；  
因为可行流上每条弧<u,v>上至少有b(u,v)的流量，可以假设一个伪流f1(u,v)，满足：  
f(u,v)=b(u,v)+f1(u,v);  
很显然有：  
0<=f1(u,v)<=c(u,v)-b(u,v);  
这样在伪流中，f1(u,v)去掉了流量下界；  
又由于伪流f1也不满足流量平衡条件，所以必须构造一个伴随网络G1来求解伪流f1；  
伴随网络需要满足的条件：  
①伴随网络G1与原网络同构，可以增设顶点；  
②伴随网络中所有弧的流量只有上界，而没有下界；  
③原网络的伪流f1包含在伴随网络的最大流f2中；  
这样就可以用基础的网络最大流算法求出伴随网络的最大流f2，从而求出伪流f1和可行流f；  
如果存在可行流，则可以按照基础的最大流算法放大可行流从而求出最大流；  
  
#### (2)最小流
同样先构造伴随网络G1判断是否存在可行流；
如果可行流存在，则从可行流出发，倒向求解；
即保持网络中的弧方向不变，将Vt作为源点，Vs作为汇点，用基础算法把可行流放大，即为正向网络的最小流；
  
### 过程  
* (1)构造伴随矩阵判断是否存在可行流；  
伴随网络G1的构造方法：  
①新增两个顶点(即附加源点Vs1和附加汇点Vt1);  
②对原网络G中每个顶点Vi,加一条新弧<Vi,Vt1>,这条弧的容量为顶点Vi发出的所有弧的流量下界之和；  
③对原网络G中每个顶点Vi,加一条新弧<Vs1,Vi>,这条弧的容量为进入到顶点Vi的所有弧的流量下界之和；  
④原网络G中的每条弧<u,v>，在伴随网络G1中仍然保留，但是弧的容量修正为：c1(u,v)=c(u,v)-b(u,v);  ⑤再添加两条新弧<Vs,Vt>和<Vt,Vs>，流量上界为无穷大；  
构造好伴随网络G1后，用网络流的基础算法求出附加源点Vs1到附加汇点Vt1的最大流；  
如果求得的最大流中，附加源点Vs1流出的所有弧均满载，即Vs1发出的所有弧e均满足f1(e)==c1(e);  
则原网络G中存在可行流f(e)=f1(e)+b(e)；  
即在该可行流中，每条弧上的流量为伴随网络最大流对应弧上的流量加上该弧的流量下界；  
如果伴随网络的最大流中，附加源点Vs1发出的弧没有满载，则原网络G中不存在可行流；  
  
* (2)如果存在可行流，则按照基础的最大流算法，把可行流放大，从而求的最大流；  
但是在放大可行流的过程中，因为增广路上的反向弧的流量会减少；  
所以在选择可改进量a时要保证反向流量减少后不低于流量下界b(e)；  
即a=min(min(c(e)-f(e)),min(f(e)-b(e)));

### 举例  
输入顶点数n和弧的数目m；  
然后输入每条弧的数据，即起点u,终点v,流量下界b,流量上界c；  
假设源点为第1个顶点，汇点为第n个顶点；  
采用最基础的Ford_Fulkerson(标号法)求最大流;

#### 测试数据

```
6 8

1 2 0 10

1 3 1 3

2 4 2 8

3 5 5 7

4 3 2 4

4 6 2 6

5 2 1 3

5 6 3 5

0 0
````

#### 运行结果    
最大流为：10  
最小流为：5  

#### 参考资料    
《图论算法理论、实现及应用》

#### 代码实现  

```
#include<iostream>
#include<cstdio>
#include<cmath>
#include<cstring>
#include<cstdlib>
#include<queue>
#include<algorithm>
using namespace std;
const int MAXN=100;
const int INF1=0xffffff;//顶点之间不存在弧连接时设置的流量上界
const int INF2=0xffff;//伴随网络中新增的两条弧的流量上界
struct arc
{
    int b,c,f;//弧流量的下界，上界和实际流量
};
arc G1[MAXN][MAXN];//原网络
arc G2[MAXN][MAXN];//伴随网络
int n,m;
int flag[MAXN];//顶点状态： -1未标号，0已标号未检查，1已标号已检查
int pre[MAXN];//标号的第一个分量，表示从哪一个顶点得到
int a[MAXN];//标号的第二个分量，表示可改进量a
//int queue[MAXN];//队列
int q;//从队列取出的头元素
//int qs,qe;//队列的头，尾

//求最大流的基础算法
int Ford_Fulkerson(arc G[][MAXN],int s,int t,int max)//max为-1表示求伴随网络G2的最大流，1表示求原网络G1的最大流，0表示求最小流
{

    while(1)//标号至不可再改进路
    {
        queue<int>Q;
        memset(flag,-1,sizeof(flag));
        memset(pre,-1,sizeof(pre));
        memset(a,-1,sizeof(a));
        flag[s]=pre[s]=0;
        a[s]=INF1;
        //qs=qe=0;
        //queue[qe]=s;
        //qe++;
        Q.push(s);
        //while(qs<qe&&flag[t]==-1)
        while(!Q.empty()&&flag[t]==-1)
        {
            //q=queue[qs];
            //qs++;
            q=Q.front();
            Q.pop();
            for(int i=s; i<=t; i++)
            {
                if(flag[i]==-1)
                {
                    if(G[q][i].c<INF1&&G[q][i].f<G[q][i].c)//正向且流量还可以增加
                    {
                        flag[i]=0;
                        pre[i]=q;
                        a[i]=min(a[q],G[q][i].c-G[q][i].f);
                        //queue[qe]=i;
                        //qe++;
                        Q.push(i);
                    }
                    else if(G[i][q].c<INF1&&G[i][q].f>G[i][q].b)//反向且流量还可以减少
                    {
                        flag[i]=0;
                        pre[i]=-q;
                        a[i]=min(a[q],G[i][q].f-G[i][q].b);
                        //queue[qe]=i;
                        //qe++;
                        Q.push(i);
                    }
                }
            }
            flag[q]=1;//顶点q已标号已检查
        }

        if(flag[t]==-1||a[t]==0)//当汇点没有获得标号或者汇点的调整量为0.则退出
            break;

        int k1=t;
        int k2=abs(pre[k1]);
        int a1=a[t];//可改进量
        while(1)
        {
            if(G[k2][k1].f<INF1)//正向
                G[k2][k1].f=G[k2][k1].f+a1;
            else//反向
                G[k1][k2].f=G[k1][k2].f-a1;
            if(k2==s)//调整到源点
                break;
            k1=k2;
            k2=abs(pre[k2]);
        }
    }//算法结束

    int max_f=0;
    for(int i=s; i<=t; i++)
    {
        for(int j=s; j<=t; j++)
        {
            if(i==s&&G[i][j].f<INF1)//源点流出
                max_f+=G[i][j].f;
            if(i==s&&G[j][i].f<INF1)//源点流入
                max_f-=G[j][i].f;
        }
    }
    // cout<<"max_f=="<<max_f<<endl;
    if(max)//求最大流
        return max_f;
    else//求最小流
        return -max_f;
}

//构造伴随矩阵，求可行流
int accompany()
{
    memcpy(G2,G1,sizeof(G1));
    int sum1,sum2;
    for(int i=1; i<=n; i++)
    {
        sum1=sum2=0;
        for(int j=0; j<=n; j++) //统计顶点i发出的弧和进入到顶点i的弧
        {
            if(G2[i][j].b!=INF1)
                sum1+=G2[i][j].b;
            if(G2[j][i].b!=INF1)
                sum2+=G2[j][i].b;
        }
        G2[i][n+1].c=sum1;
        G2[i][n+1].b=G2[i][n+1].f=0;
        G2[0][i].c=sum2;
        G2[0][i].b=G2[0][i].f=0;
    }

    for(int i=1; i<=n; i++)
    {
        for(int j=1; j<=n; j++)
        {
            if(G2[i][j].c!=INF1)//修改原网络中的弧
            {
                G2[i][j].c=G2[i][j].c-G2[i][j].b;
                G2[i][j].b=0;
            }
        }
    }

    G2[1][n].c=G2[n][1].c=INF2;
    G2[1][n].b=G2[n][1].b=0;
    G2[1][n].f=G2[n][1].f=0;

    Ford_Fulkerson(G2,0,n+1,-1);//求伴随网络的最大流

    bool judge=1;//判断是否存在可行流
    for(int i=0; i<=n+1; i++)
    {
        //cout<<"G2[0]["<<i<<"].f=="<<G2[0][i].f<<"          "<<"G2[0]["<<i<<"].c=="<<G2[0][i].c<<endl;
        if(G2[0][i].c!=INF1&&G2[0][i].f!=G2[0][i].c)
            judge=0;
    }

    if(judge==0)//没有可行流
    {
        printf("没有可行流！");
        return 0;
    }

    for(int i=1; i<=n; i++) //修改原网络的弧
    {
        for(int j=1; j<=n; j++)
        {
            if(G1[i][j].c!=INF1)
                G1[i][j].f=G2[i][j].f+G1[i][j].b;
        }
    }

    cout<<"最大流为：  "<<Ford_Fulkerson(G1,1,n,1)<<endl;//求原网络的最大流

    //求原网络的最小流，先还原到原网络的可行流
    int b,c,f;
    for(int i=1; i<=n; i++)
    {
        for(int j=1; j<=n; j++)
        {
            if(G1[i][j].c!=INF1)//修改原网络中的弧
                G1[i][j].f=G2[i][j].f+G1[i][j].b;
        }
    }

    for(int i=1; i<=n; i++) //将原网络的源点和汇点互换
    {
        //第1行与第n行互换，第1列与第n列互换
        b=G1[1][i].b;
        c=G1[1][i].c;
        f=G1[1][i].f;
        G1[1][i].b=G1[n][i].b;
        G1[1][i].c=G1[n][i].c;
        G1[1][i].f=G1[n][i].f;
        G1[n][i].b=b;
        G1[n][i].c=c;
        G1[n][i].f=f;
        b=G1[i][1].b;
        c=G1[i][1].c;
        f=G1[i][1].f;
        G1[i][1].b=G1[i][n].b;
        G1[i][1].c=G1[i][n].c;
        G1[i][1].f=G1[i][n].f;
        G1[i][n].b=b;
        G1[i][n].c=c;
        G1[i][n].f=f;
    }
    cout<<"最小流为：  "<<Ford_Fulkerson(G1,1,n,0)<<endl;
}

int main()
{
    //freopen("C:\\Users\\Administrator\\Desktop\\kd.txt","r",stdin);
    while(~scanf("%d%d",&n,&m))
    {
        if(n+m==0)
            break;
        for(int i=0; i<MAXN; i++)
        {
            for(int j=0; j<MAXN; j++)
                G1[i][j].b=G1[i][j].c=G1[i][j].f=INF1;
        }
        for(int i=1; i<=m; i++)
        {
            int u,v,b,c;
            scanf("%d%d%d%d",&u,&v,&b,&c);
            G1[u][v].b=b;
            G1[u][v].c=c;
            G1[u][v].f=0;
        }
        accompany();
    }
    return 0;
}
```


