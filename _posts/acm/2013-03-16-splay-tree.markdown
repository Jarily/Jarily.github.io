---
layout: post
title:   数据结构-Spaly_Tree
author: "R. Liao" 
categories: acm
tags: 伸展树
---


### 数据结构：  
Splay_Tree,伸展树;

### 性质  
伸展树是二叉查找树的一种改进;  
与二叉查找树一样,伸展树也具有有序性;  
即伸展树中的每一个节点x都满足：  
该节点左子树中的每一个元素都小于x;  
而其右子树中的每一个元素都大于x;  
与普通二叉查找树不同的是，伸展树可以自我调整;

### 特点  
伸展树并不是严格意义上的平衡树;  
也还是极有可能退化成线性结构,但伸展操作能使它的每一次操作近似(logn);

### 伸展操作  
伸展操作和平衡树的保持平衡是类似的;  
只不过他不要求保持平衡,只是相应的旋转;  
旋转有三种情况要处理：  
* (1)Zig或Zag(节点x的父节点y是根节点)  
* (2)Zig-Zig或Zag-Zag(节点x的父节点y不是根节点，且x与y同时是各自父节点的左孩子或者同时是各自父节点的右孩子)  
* (3)Zig-Zag或Zag-Zig(节点x的父节点y不是根节点，x与y中一个是其父节点的左孩子而另一个是其父节点的右孩子)  
即一字型旋转和之字型旋转;

### 优势  
能快速定位一个区间[l,r]，并且能将区间进行删除、旋转操作;  
将第l-1个结点旋转至根(之前的Splay操作)，将第r+1个结点旋转至根的右孩子;  
由于伸展树的本质还是二叉搜索树,则根据二叉查找树的性质可以知道;  
在这两个结点之间，也是根的右孩子的左子树就包括节点[l,r];  
即很快定位了区间[l,r]，如果需要删除，直接把子树拿走即可;

### 应用举例-PKU3468   

#### 链接  
[A Simple Problem with Integers](http://poj.org/problem?id=3468)

#### 题意    
Q a b   ：查询区间[a,b]的和;  
C a b x : 更新区间[a,b]，区间所有值加上x;   

### 代码实现  

```
#include<iostream>
#include<cstring>
#include<cstdio>
#include<algorithm>
using namespace std;

#define Key_value ch[ch[root][1]][0]//进行各种操作的区间

const int INF=0xffffff;
const int N=100010;
typedef long long LL;

int ch[N][2];//左右孩子(0为左孩子，1为右孩子)
int pre[N];//父结点
int key[N];//数据域
int size[N];//树的规模
int val[N];
int add[N];
int a[N];//结点元素
LL sum[N];//子树结点和
int root;  //根结点
int tot;//结点数量
int n,q;

void Push_Up(int u)//通过孩子结点更新父结点
{
    size[u]=size[ch[u][0]]+size[ch[u][1]]+1;
    sum[u]=sum[ch[u][0]]+sum[ch[u][1]]+val[u]+add[u];
}

void Push_Down(int u)//将延迟标记更新到孩子结点
{
    if(add[u])
    {
        val[u]+=add[u];
        add[ch[u][0]]+=add[u];
        add[ch[u][1]]+=add[u];
        sum[ch[u][0]]+=(LL)add[u]*size[ch[u][0]];
        sum[ch[u][1]]+=(LL)add[u]*size[ch[u][1]];
        add[u]=0;
    }
}

void New_Node(int &u,int f,int c)//新建一个结点，f为父节点
{
    u=++tot;
    val[u]=sum[u]=c;
    pre[u]=f;
    size[u]=1;
    ch[u][1]=ch[u][0]=add[u]=0;
}

void Build_Tree(int &u,int l,int r,int f)//建树，中间结点先建立，然后分别对区间两端在左右子树建立
{
    if(l>r)
        return;
    int m=(l+r)>>1;
    New_Node(u,f,a[m]);
    if(l<m)
        Build_Tree(ch[u][0],l,m-1,u);
    if(r>m)
        Build_Tree(ch[u][1],m+1,r,u);
    Push_Up(u);
}

void Rotate(int x,int c)//旋转操作，c=0 表示左旋，c=1 表示右旋
{
    int y=pre[x];
    Push_Down(y);// 先将Y结点的标记向下传递（因为Y在上面）
    Push_Down(x);//再把X的标记向下传递
    ch[y][!c]=ch[x][c];//类似SBT，要把其中一个分支先给父节点
    pre[ch[x][c]]=y;
    pre[x]=pre[y];
    if(pre[y])//如果父节点不是根结点，则要和父节点的父节点连接起来
    {
        ch[pre[x]][ch[pre[y]][1]==y]=x;
    }
    pre[y]=x;
    ch[x][c]=y;
    Push_Up(y);
}

void Splay(int x,int f)//Splay操作,把根结点x转到结点f的下面
{
    Push_Down(x);
    while(pre[x]!=f)
    {
        int y=pre[x];
        if(pre[y]==f)//父结点的父亲即为f，执行单旋转
            Rotate(x,ch[y][0]==x);
        else
        {
            int z=pre[y];
            int g=(ch[z][0]==y);
            if(ch[y][g]==x)
                Rotate(x,!g),Rotate(x,g);//之字形旋转
            else Rotate(y,g),Rotate(x,g);//一字形旋转
        }
    }
    Push_Up(x);// 最后再维护X结点
    if(f==0)//更新根结点
    {
        root=x;
    }
}

void Rotate_Under(int k,int f)//把第k位的数伸展到f下方
{
    //找到处在中序遍历第k个结点，并将其旋转到结点f 的下面
    int p=root;//从根结点开始
    Push_Down(p);// 由于要访问p的子结点，将标记下传
    while(size[ch[p][0]]!=k)//p的左子树的大小
    {
        if(k<size[ch[p][0]])// 第k个结点在p左边，向左走
        {
            p=ch[p][0];
        }
        else//否则在右边,而且在右子树中，这个结点不再是第k个
        {
            k-=(size[ch[p][0]]+1);
            p=ch[p][1];
        }
        Push_Down(p);
    }
    Splay(p,f);//执行旋转
}

int Insert(int k)//插入结点
{
    int r=root;
    while(ch[r][key[r]<k])
        r=ch[r][key[r]<k];
    New_Node(ch[r][k>key[r]],r,k);
    //将新插入的结点更新至根结点
    //Push_Up(r);
    Splay(ch[r][k>key[r]],0);
    return 1;
}

int Get_Pre(int x)//找前驱，即左子树的最右结点
{
    int tmp=ch[x][0];
    if(tmp==0)
    return INF;
    while(ch[tmp][1])
    {
    	tmp=ch[tmp][1];
    }
    return key[x]-key[tmp];
}

int Get_Next(int x)//找后继，即右子树的最左结点
{
    int tmp=ch[x][1];
    if(tmp==0)
    return INF;
    while(ch[tmp][0])
    {
        tmp=ch[tmp][0];
    }
    return key[tmp]-key[x];
}

LL Query(int l,int r)//查询[l,r]之间的和
{
    Rotate_Under(l-1,0);
    Rotate_Under(r+1,root);
    return sum[Key_value];
}

void Update(int l,int r)//更新
{
    int k;
    scanf("%d",&k);
    Rotate_Under(l-1,0);
    Rotate_Under(r+1,root);
    add[Key_value]+=k;
    sum[Key_value]+=size[Key_value]*k;
}

void Init()//初始化
{
    for(int i=0; i<n; i++)
        scanf("%d",&a[i]);
    ch[0][0]=ch[0][1]=pre[0]=size[0]=0;
    add[0]=sum[0]=0;
    root=tot=0;
    New_Node(root,0,-1);
    New_Node(ch[root][1],root,-1);   //头尾各加入一个空位
    size[root]=2;
    Build_Tree(Key_value,0,n-1,ch[root][1]);  //让所有数据夹在两个-1之间
    Push_Up(ch[root][1]);
    Push_Up(root);
}

int main()
{
    //freopen("C:\\Users\\Administrator\\Desktop\\kd.txt","r",stdin);
    while(~scanf("%d%d",&n,&q))
    {
        Init();
        while(q--)
        {
            char op;
            scanf(" %c",&op);
            int x,y;
            scanf("%d%d",&x,&y);
            if(op=='Q')
                printf("%lld\n",Query(x,y));
            else
                Update(x,y);
        }
    }
    return 0;
}

```