---
layout: post
title:  SQLConfigDataSource函数
author: "R. Liao" 
categories: study
tags:  SQLConfigDataSource函数
---
```
BOOL SQLConfigDataSource(HWND hwndParent, UINT
                           fRequest,LPCSTR IpszDriver, LPCSTR IpszAttributes);
```

**无论是用ODBC还是DAO类，在访问ODBC数据源以前，都必须先注册DSN。通过调用函数SQLConfigDataSource，可以实现自动注册DSN。**


#### (1)参数hwndPwent是父级窗口句柄。  
如果句柄为NULL，将不会显示一些有关的对话框。  
如果参数 IpszAttributes提供的信息不够完善，在创建过程中就会出现对话框要求用户提供相应信息。


#### (2)参数fRequest可以设置为下面的数值之一:  
ODBC＿ADD＿DSN: 增加＿个新数据源  
ODBC＿CONHG＿DSN: 配置（修改)一个已经存在的数据源  
ODBC＿REMOVE＿DSN: 删除一个已经存在的数据源  
ODBC＿ADD＿SYS＿DSN:. 增加一个新的系统数据源  
ODBC_CONFIG—SYS—DSN： 更改一个已经存在的系统数据源  
ODBC＿REMOVE＿SYS＿DSN:. 删除一个已经存在的系统数据源


#### (3)参数lpszDriver是数据库引擎名称。


#### (4)参数lpszAttributes为一连串的"KeyName=value"字符串。  
每两个KeyName值之间用" "字符隔开。  
KeyName主要是新数据源缺省的驱动程序注册说明，其中最主要的关键字是"DSN"，为新数据源的名称.  
其余关键字则根据不同的数据源有不同要求,包括缺省目录以及驱动程序版本信息。


对SQLConfigDataSource函数的第四个参数的设置方法:  
可以打开Windows的注册表看一看已注册过的DSN的各项属性。  
运行RegEdit可以打开注册表，  
然后依次打开HKEY_CURRENT_USER->Software->ODBC->ODBC.INI，  
就可以看到已注册的DSN，  
打开各DSN，则可以看到该DSN的各项属性，  
则可以仿照DSN属性来设置第四个参数。


* DSN的名字必须唯一，因此如果要注册的DSN已被注册过，那么SQLConfigDataSource就修改原来DSN的属性。


#### (5)SqlConfigDataSource的应用条件  
使用SqlConfigDataSource函数之前，必须把ODBCINST.H文件包含在工程头文件中。  
将ODBC-CP32.LIB加入工程，同时保证ODBCCP32.DLL运行时处于系统子目录下。  


```  
#include "afxdb.h"
CDatabase db;
if(!SQLConfigDataSource(NULL,ODBC_ADD_DSN,"Microsoft Access Driver (*.mdb)",
                        "DSN=MYDB\0","DBQ=MYDB.mdb\0"))
{
    AfxMessageBox("Can't add DSN!");
    return;
}
TRY
{
    db.Open("MYDB");
}
CATCH(CDBException,e)
{
    AfxMessageBox(e->m_strError);
    return;
}
END_CATCH  
```




