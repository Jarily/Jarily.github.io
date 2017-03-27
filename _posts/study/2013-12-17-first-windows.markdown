---
layout: post
title: 第一个Windows程序
author: "R. Liao" 
categories: study
tags: Windows
---

##### 第一个windows程序
```
#include <windows.h>
#include <stdio.h>

LRESULT CALLBACK winhehepro(
							HWND hwnd,      // handle to window
							UINT uMsg,      // message identifier
							WPARAM wParam,  // first message parameter
							LPARAM lParam   // second message parameter
							);


int WINAPI WinMain(
				   HINSTANCE hInstance,  // handle to current instance
				   HINSTANCE hPrevInstance,  // handle to previous instance
				   LPSTR lpCmdLine,      // pointer to command line
				   int nCmdShow          // show state of window
				   ) 
{
    WNDCLASS wndcls;
    wndcls.cbClsExtra=0;
    wndcls.cbWndExtra=0;
    wndcls.hbrBackground=(HBRUSH)GetStockObject(BLACK_BRUSH);
    wndcls.hCursor=LoadCursor(NULL,IDC_CROSS);
    wndcls.hIcon=LoadIcon(NULL,IDI_ERROR);
    wndcls.hInstance=hInstance;
    wndcls.lpfnWndProc=winhehepro;
    wndcls.lpszClassName="hehe";
    wndcls.lpszMenuName=NULL;
    wndcls.style=CS_HREDRAW|CS_VREDRAW;
    RegisterClass(&wndcls);
	
    HWND hwnd;//创建窗口
    hwnd=CreateWindow(
		"hehe",  // pointer to registered class name
		"Jarily", // pointer to window name
		WS_OVERLAPPEDWINDOW,        // window style
		0,                // horizontal position of window
		0,                // vertical position of window
		600,           // window width
		400,          // window height
		NULL,      // handle to parent or owner window
		NULL,          // handle to menu or child-window identifier
		hInstance,     // handle to application instance
		NULL        // pointer to window-creation data
		);
	
    ShowWindow(hwnd,SW_SHOWNORMAL);
    UpdateWindow(hwnd);
	
    MSG msg;//消息循环
    //while(GetMessage(&msg,hwnd,0,0))
	while(GetMessage(&msg,NULL,0,0))
    {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }
	return msg.wParam;
    //return 0;
}

LRESULT CALLBACK winhehepro(
							HWND hwnd,      // handle to window
							UINT uMsg,      // message identifier
							WPARAM wParam,  // first message parameter
							LPARAM lParam   // second message parameter
							)
{
    switch(uMsg)
    {
    case WM_CHAR:
        char szChar[20];
        sprintf(szChar,"char is %d",wParam);
        MessageBox(hwnd,szChar,"xixi",0);
        break;
    case WM_LBUTTONDOWN:
        MessageBox(hwnd,"left button is checked","xixi",0);
        HDC hdc;
        hdc=GetDC(hwnd);//不能在响应WM_PAINT消息时调用
        TextOut(hdc,0,50,"Hello World!",strlen("Hello World!"));
        ReleaseDC(hwnd,hdc);
        break;
    case WM_PAINT:
        HDC hDC;
        PAINTSTRUCT ps;
        hDC=BeginPaint(hwnd,&ps);//BeginPaint只能在响应WM_PAINT消息时调用
        TextOut(hDC,0,0,"hehe and xixi!",strlen("hehe and xixi!"));
        EndPaint(hwnd,&ps);
        break;
    case WM_CLOSE:
        if(IDYES==MessageBox(hwnd,"是否真的退出窗口?","iloveyou",MB_YESNO))
        {
            DestroyWindow(hwnd);
        }
        break;
    case WM_DESTROY:
        PostQuitMessage(0);
        break;
    default:
		return DefWindowProc(hwnd,uMsg,wParam,lParam);
    }
    return 0;
}
```