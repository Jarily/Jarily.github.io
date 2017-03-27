---
layout: post
title: MATSim工具的样例运行
author: "R. Liao" 
categories: study
tags: MATSim
      Java
      Via
---

### 环境

MATSim版本 matsim-0.8.0 [MATSim下载地址](http://matsim.org/downloads)  

Via版本为： Via-1.7.0 64位 (需要自己在线生成一个vialicense.xml)  [Via下载地址](http://via.senozon.com/download)

两者均是解压即可

我的步骤参考了[MATSim官网](http://www.matsim.org) 上面的步骤。
Demo文件也就是在Matsim文件中给出的example中找的一个

MATSim的running主要是通过命令行启动它的配置文件。即config文件。
config.xml是MATSim仿真的统一入口文件，用于设置仿真参数，控制仿真过程，包括迭代次数设置等到。
其中，在demo文件中，只有network.xml和plan.xml这两个必不可少的文件，其他的都缺省。


启动命令为：

```
java -Xmx2000m -cp matsim-0.8.0.jar org.matsim.run.Controler demo/demo-config.xml

```
参数说明：

* -Xmx2000m : Increases the Java heap space to 2000MB of memory. 
* -cp matsim-0.8.0.jar : The jar file (Java library) which contains MATSim.
* org.matsim.run.Controler : The class where the main method for running "iterations" resides. 


当然这是命令行的运行方式，还有就是GUI的运行方式，解压MATSim后打开对应的一个JAR包即可。


### 具体步骤

#####   （1）解压matsim-0.8.0.zip 文件到任意目录 我是解压到E:\Braess_Paradox\MATSim\matsim-0.8.0 

 ![解压](/images/study/2016-08-10/4.png)


#####   （2）将装有network.xml和plan.xml和config.xml三个文件的demo文件夹放到刚刚安装matsim的根目录下

![demo](/images/study/2016-08-10/5.png)

#####   （3）cmd下找到安装matsim 的目录下
输入以下命令

```
java -Xmx2000m -cp matsim-0.8.0.jar org.matsim.run.Controler demo/demo-config.xml

```
回车


![run](/images/study/2016-08-10/6.png)



运行结束后会matsim安装目录下会出现output文件夹，里面则为输出信息。

#####  （4）安装好Via工具，即解压即可， 

将network.xml文件和输出文件下面的ITERS\it.i文件中的i.events.xml.gz (i=0到10)拖到Via的Data Source 下面
在Via的Layer层左下角点击“+”号，选择network 点击Add
![run](/images/study/2016-08-10/7.png)
则会出现网络图
在Via的Layer层左下角点击“+”号，选择Vehicles 点击Add
然后点击左侧的 Load data按钮

仿真结果就会出现。

我是选择的第10次迭代的结果可视化，所以界面某个时间点为下：

![run](/images/study/2016-08-10/8.png)