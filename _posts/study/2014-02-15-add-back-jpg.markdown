---
layout: post
title:  MFC单文档添加背景图片
author: "R. Liao" 
categories: study
tags: MFC
---
#### 1.首先准备好一张BMP图片，保存为BMP格式。

#### 2.新建一个工程，命名为：test ，在资源编辑里用Import导入刚才准备好的位图文件.ID为IDB_BITMAP  
如果位图是大于16色的，会出现无法显示的提示。不要紧，这并不影响程序最终的显示。

#### 3.代码实现一  

##### 3.1 我们为CTestView类添加一个变量 CBrush m_brushBackground;这个画刷就是用于画背景的。  

##### 3.2 我们在CTestView的构造函数中加入如下代码:

```
CBitmap bmp;
 bmp.LoadBitmap(IDB_BITMAP); ///加载位图
   m_brushBackground.CreatePatternBrush(&bmp); ///创建位图画刷
```

##### 3.3 接着我们需要在OnDraw函数中画出来,  
代码如下: 

```
CRect rect;
 GetClientRect(rect);///取得客户区域
   pDC->FillRect(rect,&m_brushBackground); ///用背景画刷填充区域
```

##### 3.4 为了避免背景的闪烁，使显示更加完美，我们添加WM_ERASEBKGND消息的处理函数，并取消调用父类的处理函数，  
代码如下: 
```
BOOL CTestView::OnEraseBkgnd(CDC* pDC) 
{
 return TRUE;
}
```
接下来，我们就编译运行该程序了！


#### 4.代码实现二   
在CMyView中定义 ```CBitmap *m_bitmap;```    
在CMyView构造函数中加入
```
m_bitmap =new CBitmap;
m_bitmap->LoadBitmap(IDB_BITMAP1);
```  
然后  

```
CMyView::OnEraseBkgnd(CDC* pDC) 
{
CView::OnEraseBkgnd(pDC);
     CDC dcMem;
CClientDC dc(this);
HBITMAP hbit;

dcMem.CreateCompatibleDC(&dc);
hbit = (HBITMAP)dcMem.SelectObject(m_bitmap);

GetDC()->BitBlt(10,10,400,300,&dcMem,0,0,SRCCOPY);
return 0;
}
```