---
layout: post
title:  Cartographer开源代码分析
author: "R.Liao" 
categories: study
tags: SLAM
---

## 1.     Cartographer理论概述
## 2.     开源代码逻辑

&emsp;Google开源的代码包含两个部分：cartographer和cartographer_ros。cartographer主要负责处理来自雷达、IMU和里程计的数据并基于这些数据进行地图的构建，是cartographer理论的底层实现。

&emsp;cartographer_ros则基于ros的通信机制获取传感器的数据并将它们转换成cartographer中定义的格式传递给cartographer处理，与此同时也将cartographer的处理结果发布用于显示或保存，是基于cartographer的上层应用。

## 3.     cartographer代码结构

common：定义了基本数据结构以及一些工具的使用接口。

ensor：定义了雷达数据及点云等相关的数据结构。

transform：定义了位姿的数据结构及其相关的转换。

kalman_filter: 主要通过kalman滤波器完成对IMU、里程计及基于雷达数据的估计位姿的融合，进而估计新进的laser scan的位姿。

mapping：定义了上层应用的调用接口以及局部submap构建和基于闭环检测的位姿优化等的接口。

mapping_2d和mapping_3d：对mapping接口的不同实现。


## 4.     mapping_2d代码逻辑

### 4.1 cartographer::mapping_2d:: GlobalTrajectoryBuilder

cartographer::mapping_2d::GlobalTrajectoryBuilder类主要实现了接收处理上层应用传递的传感器数据的主要接口：

 1. AddImuData用于接收处理上层应用传递的IMU数据。

 2. AddOdometerPose用于接收处理上层应用传递的里程计数据。

 3. AddHorizontalLaserFan用于接收处理上层应用传递的雷达数据。

其中包含重要的对象成员：

 1. artographer::mapping_2d::LocalTrajectoryBuilder类的对象local_trajectory_builder_用于完成局部submap的构建。

 2. cartographer::mapping_2d::SparsePoseGraph类的对象sparse_pose_graph_用于完成闭环检测及全局位姿优化。

&emsp;在AddImuData和AddOdometerPose函数的实现中会将接收的相应传感器数据传递给local_trajectory_builder_对象处理。

&emsp;在AddHorizontalLaserFan函数的实现中则将新进的laser fan传递给local_trajector_builder_对象用于局部submap构建，如果该laser fan被成功插入到某个submap，那么该laser fan被插入后的相关信息则被传递给sparse_pose_graph_对象用于基于闭环检测的全局位姿优化。

### 4.2 cartographer::mapping_2d::LocalTrajectoryBuilder

cartographer::mapping_2d::LocalTrajectoryBuilder类主要完成局部submap的构建。其提供了接收处理传感器数据的public函数：

 1. AddImuData用于处理IMU数据。
 
 2. AddOdometerPose用于处理里程计数据。
 
 3. AddHorizontalLaserFan用于处理雷达数据。

以及包含了一些重要的private成员：

 1. ScanMatch成员函数基于submap已有的laser fan估计当前laser fan在submap中的位置。

 2. cartographer::kalman_filter::PoseTracker类的对象pose_tracker_用于融合基于雷达数据的laser fan的局部估计位姿、IMU数据以及里程计数据，进而估计出较优的laser fan的位姿。

&emsp;在AddImuData和AddOdometerPose函数中会将IMU数据和里程计数据传递给pose_tracker_进行处理。

&emsp;pose_tracker通过UKF不断融合IMU和里程计数据进而更新当前位姿，因此通过pose_tracker可以获取当前laser fan的估计位姿的一个较好的初始化值。

&emsp;进一步的，在AddHorizontalLaserFan函数中会调用ScanMatch，ScanMatch函数中通过在submap中局部匹配得到的当前laser fan的估计位姿被pose_tracker_用来调整该laser fan的初始化值。

&emsp;这样pose_tracker_通过融合多传感器数据，进而能够估计出较优的laser fan的位姿。

### 4.3  cartographer::mapping_2d::SparsePoseGraph

cartographer::mapping_2d::SparsePoseGraph类主要完成基于闭环检测的全局位姿优化。其提供了接收处理新进被插入到submap的laser fan相关信息的public函数：

 1. AddScan 对新进的laser fan进行闭环检测及在适当的时候进行全局优化。
以及一些重要的私有成员：

 2. ComputeConstraintsForScan对新近laser fan信息进行处理并启动闭环检测scan
    match以及计算其约束，进而将约束添加到位姿优化目标中。

 3. AddWorkItem将laser
    fan与ComputeConstraintsForScan绑定，并将任务加入到队列中。
 
 4. HandleScanQueue依此调度队列中的任务。
 
 5. sparse_pose_graph::ConstraintBuilder constraint_builder_
    用于完成laser fan的scan match以及约束计算。

 6. RunOptimization优化目标。

&emsp;在AddScan函数中会将laser fan相关信息与ComputeConstraintsForScan函数绑定，并将绑定好的任务通过AddWorkItem函数加入到队列中。

&emsp;HandleScanQueue函数则依次调度队列中的任务。第一次调用AddWorkItem时会直接启动ComputeConstraintsForScan任务，且在第一次ComputeConstraintsForScan任务时启动HandleScanQueue调度。

&emsp;在ComputeConstrainsScan中，通过constraint_builder_对象完成闭环检测的scan match以及约束计算。

&emsp;当所有约束计算完成时，则会进行RunOptimization优化目标。

### 4.4  ScanMatch
&emsp;LocalTrajectoryBuilder中的scan match策略与SparsePoseGraph中的scan match策略是不同的。

&emsp;前者使用scan_matching::RealTimeCorrelativeScanMatcher，&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;后者则使用scan_matching::FastCorrelativeScanMatcher。

&emsp;二者的目标优化均是由scan_matching::CeresScanMatcher完成。

## 5.     总结
&emsp;Cartographer的重点内容是融合多传感器数据的局部submap创建以及用于闭环检测的scan match策略。

&emsp;重点内容对应的实现是：

 - 基于UKF的多传感器数据融合对应cartographer/kalman_filter目录下的文件；

 - scan match策略对应cartographer/mapping_2d/scan_matching目录下的文件。
