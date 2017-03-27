---
layout: post
title: 修改应用程序窗口的外观
author: "R. Liao" 
categories: study
tags: MFC
---

### 一 于MFC 应用程序来说，为了改变 MFC AppWizard 自动生成的应该程序外观和大小，我们既可以在应用程序窗口创建之前进行，也可以在该窗口创建之后进行。    
如果希望在应用程序窗口创建之前修改它的外观和大小，就应该在 CMainFrame 类的 PreCreateWindow 成员函数中进行。

### 二 在CMainFrame::PreCreateWindow中 添加 cs.lpszName="XXX"; 我想把程序的标题改为XXX；  但是程序运行时，却发现标题没有改过来。     
因为我们创建的应用程序 是一个 SDI 应用程序，在单文档界面（SDI) 应用程序中，框架的默认窗口样式是 WS_OVERLAPPEDWINDOW 和 FWS_ADDTOTITLE 样式的组合。  
其中，FWS_ADDTOTITLE 是MFC 特定的一种样式，指示框架将文档标题添加到窗口标题上。  
因此想让窗口显示自己设置的标题，只需要将窗口的某个类型的方法，就是对 FWS_ADDTOTITLE 样式去掉即可。       
就是说再添加 这样一条语句： cs.style&=~FWS_ADDTOTITLE;  

此外，还可以这样。  
直接把CREATESTRUCT 结构体中的 style 成员设置为 WS_OVERLAPPEDWINDOW 。  
该成员的初始定义代码 是：  
cs.style= WS_OVERLAPPEDWINDOW | FWS_ADDTOTITLE;  
可以修改为：  
cs.style=WS_OVERLAPPEDWINDOW ;也能达到同样的效果。

### 三 在窗口创建之后可以利用 SetWindowLong 这个函数来实现这种功能。  

要想获得现有窗口的类型可以利用 GetWindowLong 这个函数。

### 四如果代码是 AppWizard 自动生成的，WinMain 函数被隐藏了。  
那么我们可以利用 MFC 为我们提供的一个全局函数： AfxGetInstanceHandle   来得到当前应用程序实例的句柄。

### 五 在 MFC 程序中，如果想要修改应用程序窗口的图标，则应在框架类中进行。  
因为在框架窗口中才有标题栏，所以才能修改位于该标题栏上的图标；  
如果想要修改程序窗口的背景和光标，就应该在视类中进行。（这是因为应用程序包含有两个窗口：应用程序框架窗口和视类窗口，前者包含后者，后者覆盖在前者的上面）

### 六 MFC 为我们提供了一个全局函数 AfxRegisterWndClass ,用来设定窗口的类型、光标、背景和图标。    

#### 举例用法  
在 CMainFrame类的PreCreateWindow 函数中添加这一句  
cs.lpszName=AfxRegisterWndClass(CS_VREDRAW | CS_HREDRAW,0,0,  
LoadIcon(NULL, IDI_WARNING)); //   这里的第二、三个参数直接设置为0，因为在框架窗口中修改窗口类的光标和背景是毫无意义的。  
如果想要修改 光标和背景刚在 在 视类的PreCreateWindow 函数中添加    例如：  
cs.lpszName=AfxRegisterWndClass(CS_HREDRAW | CS_VREDRAW ,LoadCursor(NULL,IDC_CROSS),  
(HBRUSH) GetStockObject(BLACK_BRUSH),0);  
即可

### 七 窗口创建完成之后，还能修改它的光标、图标和背景吗？？  
当然可以。可以利用全局API 函数；SetClassLong;  
该函数用来重置指定窗口所属窗口类的 WNDXLASSEX   结构体（是   WNDCLASS 结构的扩展） 中指定数据成员的属性。  
这个函数和上面介绍的 SetWindowLong  差不多。