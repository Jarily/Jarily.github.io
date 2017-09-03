---
layout: post
title:  SLAM开源算法比较
author: "[转载]" 
categories: study
tags: SLAM
---


## 1各算法项目介绍
&emsp;主要有4个开源算法：ORB-SLAM,LSD-SLAM, CoSLAM, Cartographer。

&emsp;除Cartographer之外，其他三个算法均为视觉SLAM算法，且各自在自己领域内是目前公认最好的。

&emsp;ORB-SLAM采用稀疏特征点的方法来定位和构建地图，速度快，精度较高，鲁邦性较强；

&emsp;LSD-SLAM采用直接法来定位和构建，生成半稠密的地图，可视效果好，能在纹理较少的情况下使用；

&emsp;CoSLAM能利用多个机器人来协作，可克服单相机的视角问题，生成融合的地图，并更好地定位。

&emsp;雷达SLAM项目cartographer，该项目产品化程度高，运行速度快，精度高，对我们以后的SLAM研发具有很强的参考性。



|&emsp;| ORB-SLAM    | CoSLAM|LSD-SLAM|Cartographer|
|-------- | -------- | --------|--------|--------|
| 输入数据| RGB图像 |RGB视频|RGB图像|雷达数据+IMU数据|
| 传感器| 单目和立体摄像机均支持|单目摄像机，但支持多个摄像机协作|单目和立体摄像机均支持|雷达和IMU|
| 采用方法| 基于特征的方法| 基于特征的方法|直接方法|多传感器融合方法|
| 前段检测|ORB特征，词袋模型|每帧均采用KTL检测和跟踪特征点|对全图光度进行求解|~~~|
|后端优化|用g2o库进行优化|用Levenberg-Marquart算法来解非线性最小二乘问题|用g2o库进行优化|用Ceres库进行problem优化，4个线程进行后端优化|
|闭环检测|采用关键帧的方式，利用BoW来加速，对ORB特征匹配来进行闭环检测|文中并未提及，代码中未看到相关代码|用openFabMap（也即视觉字典）进行闭环检测（在编译时可选是否打开）|依据多分辨绿多层的树型结构，单枝生长方式和及时剪枝操作，深度优先搜索确定闭环|
|运动预测和观测|相机变换（通过最小化特征匹配误差值），3D特征点位置|采用KTLtracker和SfM进行|相机变换(通过最小化整图的光度值误差)，逆深度map(通过像素级的kalman滤波)|利用imu构建预测模型|
|地图类型|ORB特征的点云，关键帧图|3D点云|图(顶点为关键帧—包含图像和深度map，边为约束关系--主要为尺度转换)|网格占有形式的地图|
|适应场景|可适应大尺度场景（ORB-SLAM2中可对自动驾驶场景进行测试）|能适应较大场景（测试视频场景约为数百平方米以上）|能适应较大场景|可适应大场景（数万平米）|
|实测运行速度|ORB-SLAM2：测试包271帧，耗时为28s，fps约为10，CPU：127%左右，MEM：1.9%|测试视频6000帧左右，耗时接近15分钟，fps约为7，CPU：130%-180%，MEM：7.8%||测试包运行了40多分钟，从运行上看为实时。CPU：50%-400%之间不稳定地跳动，MEM：1.8%|
|运行速度|快（100）||较快（300）||
|定位误差|较小（100）||较大（500-1000）||
|优点|运行速度快，定位较为准确，鲁棒性较强|能适应较高程度的动态环境|能生成半稠密可视地图，在特征缺失、图像模糊等情况下有更好的鲁棒性|运行速度快，精度高|
|缺点|对环境特征的的丰富程度和图像质量十分敏感，点云地图较为稀疏，不利于后续的重建和导航|相对其他算法，运算速度较慢，多台相机会造成成本高昂|相对其他算法，运算速度较慢，且定位效果要差些|需要用雷达作为感应器，成本高，且无法生成带颜色的可视化结果。|


&emsp;其中，在运行速度和定位误差这两栏：运行速度越快，值越大，该值以ORB-SLAM为参考（100）；定位误差越大，值越大，该值以ORB-SLAM为参考（100）。
另外，本文实验是在ubuntu14.04 LTS 64-bit下进行的，其Memory为23.5GiB, Precessor为8核的Inteli7-6700k CPU @ 4.0GHk。

## 3.总结
VSLAM则已经慢慢走向了低功耗/实时/单RGB相机的运行模式。目前并无一种VSLAM算法，可较较为精确和鲁棒地适应较为复杂的环境。不过从测试结果来看，ORB-SLAM在众算法中性能较为突出。如果我们能想法解决其在低纹理情况下的相机位姿估计，且想法得到较为稠密的地图结果，其应该可较好地应用于我们手机上的VR和AR应用。

## 4.建议阅读文献
### 4.1.最新综叙
[1] Arthur Huletski, DmitriyKartashov, Kirill Krinkin. Evaluation of the Modern Visual SLAMmethods（强烈推荐）

[2] 刘浩敏,章国锋,鲍虎军.基于单目视觉的同时定位与地图构建方法综述[j].计算机辅助设计与图形学学报,2016.6, 28(6):855-868 （强烈推荐）

[3] Davide Dardari, Pau Closas,Petar M. Djuric. Indoor Tracking: Theory, Methods, and Technologies

[4] Emilio Garcia-Fidalgo, AlbertoOrtiz. vision-based topological mapping and localization methods: Asurvey

[5] Jianjun Gui, Dongbing Gu, SenWang, Huosheng Hu. A review of visual inertial odometry fromfiltering and optimisation perspectives

### 4.2.关于ORB-SLAM
[1] Raúl Mur-Artal and Juan D.Tardós, ORB-SLAM2: an Open-Source SLAM System for Monocular, Stereoand RGB-D Cameras. ArXiv:1610.06475v1.

[2] Raúl Mur-Artal, J. M. M.Montiel and Juan D. Tardós. ORB-SLAM: A Versatile and AccurateMonocular SLAM System. IEEE Transactions on Robotics, vol. 31, no. 5,pp. 1147-1163, 2015.

[3] Dorian Gálvez-López and JuanD. Tardós. Bags of Binary Words for Fast Place Recognition in ImageSequences. IEEE Transactions on Robotics, vol. 28, no. 5, pp. 1188-1197, 2012.

### 4.3.关于LSD-SLAM
[1] LSD-SLAM: Large-Scale DirectMonocular SLAM, J. Engel, T. Schöps, D. Cremers, ECCV14

[2] Semi-Dense Visual Odometry fora Monocular Camera, J. Engel, J. Sturm, D. Cremers, ICCV13

### 4.4.关于CoSLAM

[1] Zou Danping, Tan Ping.Coslam:Collaborative visual slam in dynamic environments. IEEE Trans.on Pattern Analysis and Machine Intelligence, 2013.

### 4.5.关于cartographer

[1] Wolfgang Hess, Damon Kohler,Holger Rapp, Daniel Andor. Real-Time Loop Closure in 2D LIDAR SLAM.IEEE International Conference on Robotics & Automation 2016.
## 5.其他的参考资料
### 5.1.博客
[1]OpenSLAM：这个网站中含有很多slam方面的资料，编写的程序也各有不同，很权威

https://openslam.org/（强烈推荐）

[2] 2D激光SLAM的比较，可参考博客

http://blog.csdn.NET/zyh821351004/article/details/47381135#comments

[3] 知乎上关于”学习SLAM需要哪些预备知识”的讨论https://www.zhihu.com/question/35186064

[4] OpenCV中关于相机标定和三维重建的教程

http://docs.opencv.org/2.4/modules/calib3d/doc/camera_calibration_and_3d_reconstruction.html

[5]关于SLAM的前世今生

http://www.leiphone.com/news/201605/5etiwlnkWnx7x0zb.html

[6] SLAM研究者交流QQ群：254787961（强烈推荐）

[7]http://www.cnblogs.com/gaoxiang12/半闲居士关于SLAM的博客（强烈推荐）

[8] http://www.fengbing.Net/关于SLAM项目实现的博客

[9]http://chuansong.me/n/383533742999 ICCV研讨会：实时SLAM的未来以及深度学习与SLAM的比较（强烈推荐）

### 5.2软件

[1]https://en.wikipedia.org/wiki/Bundle_adjustment wiki:求解BA的软件包