---
layout: post
title:  Floyd算法求最小环
author: "R. Liao" 
categories: acm
tags: 最小环
---

### 基本介绍     
 求一个图G中的最小环路的朴素算法为:每次找到一条边,删除了求这两点之间的最短路径;  
 若能求出,则这条最短路径与原来的边构成一个环,不过时间复杂度略高;

### 算法思想    
Floyd算法是按照顶点的编号增加的顺序更新最短路径的;  
如果存在最小环,则会在这个环中的点编号最大的那个点u更新最短路径之前发现这个环;  
即当点u被拿来更新i到j的最短路径的时候,可以发现这个闭合环路;  

* 发现的方法是,更新最短路径前,遍历i,j点对,一定会发现某对i到j的最短路径长度:  
dist[i][j]+map[j][u]+map[u][i]!=INF,这时s的i和j是当前环中挨着点u的两个点;  
因为在之前的最短路径更新过程中,u没有参与更新,所以dist[i][j]所表示的路径中不会有点u,即一定为一个环;  

* 如果在每个新的点拿来更新最短路径之前遍历i和j验证上面的式子,虽然不能遍历到所有的环;  
但是由于dist[i][j]是i到j点的最短路径m所以肯定可以遍历到最小的环;

* 如果有负权环,则该算法失效,因为包含负环的图上,dist[i][j]已经不能保证i到j的路径上不会经过同一个点多次了;

### 举例应用-PKU1743  

#### 链接  
[Sightseeing trip](http://poj.org/problem?id=1734)

#### 题意         
n个点，m条边的加权无向图，求其中的最小环，并输出路径


#### 代码  

```
/**============================================================================
#	   @author	         Jarily
#	   @name		 POJ 1734
#	   @date		 2013/05/01
============================================================================**/
#include<iostream>
#include<cstring>
#include<cstdlib>
#include<queue>
#include<cstdio>
#include<climits>
#include<algorithm>
using namespace std;

const int N=111;
const int INF=0xffffff;

int min_loop;
int num;
int map[N][N],dist[N][N],pre[N][N];
int path[N];
int n,m;

void dfs(int i,int j)
{
    int k=pre[i][j];
    if(k==0)
    {
        path[num++]=j;
        return;
    }
    dfs(i,k);
    dfs(k,j);
}

void Floyd()
{
    min_loop=INF;
    memset(pre,0,sizeof(pre));
    for(int k=1; k<=n; k++)
    {
        for(int i=1; i<k; i++)
        {
            for(int j=i+1; j<k; j++)
            {
                if(dist[i][j]+map[i][k]+map[k][j]<min_loop)
                {
                    min_loop=dist[i][j]+map[i][k]+map[k][j];
                    num=0;
                    path[num++]=i;
                    dfs(i,j);
                    path[num++]=k;
                }
            }
        }

        for(int i=1; i<=n; i++)
        {
            for(int j=1; j<=n; j++)
            {
                if(dist[i][k]+dist[k][j]<dist[i][j])
                {
                    dist[i][j]=dist[i][k]+dist[k][j];
                    pre[i][j]=k;
                }
            }
        }
    }
}

int main()
{
   // freopen("C:\\Users\\Administrator\\Desktop\\kd.txt","r",stdin);
    while(~scanf("%d%d",&n,&m))
    {
        for(int i=1; i<=n; i++)
        {
            for(int j=i+1; j<=n; j++)
                map[i][j]=map[j][i]=dist[i][j]=dist[j][i]=INF;
            map[i][i]=dist[i][i]=0;
        }
        for(int i=0; i<m; i++)
        {
            int u,v,w;
            scanf("%d%d%d",&u,&v,&w);
            if(w<map[u][v])
            {
                map[u][v]=map[v][u]=w;
                dist[u][v]=dist[v][u]=w;
            }
        }
        Floyd();
        if(min_loop==INF)
            puts("No solution.");
        else
        {
            for(int i=0; i<num-1; i++)
                printf("%d ",path[i]);
            printf("%d\n",path[num-1]);
        }
    }
    return 0;
}

```