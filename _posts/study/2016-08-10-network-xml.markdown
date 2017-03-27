---
layout: post
title: MATSim-将network.osm文件转换为network.xml
author: "R. Liao" 
categories: study
tags: Network
      Eclipse
      Java
---

MATSim仿真软件中需要的network.xml需要从.osm文件中转换过来。
所用到工具有matsim提供的jar包，JDK环境，Eclipse工具。

[MATSim下载地址](http://matsim.org/downloads)  

下载后解压。将解压目录下面的两个jar包导入你的工程里面。  

然后新建一个java文件直接贴上如下代码。  

修改一下文件名和文件路径之后Ctrl+F11运行即可。


``` 

import org.matsim.api.core.v01.Scenario;
import org.matsim.api.core.v01.network.Network;
import org.matsim.core.config.Config;
import org.matsim.core.config.ConfigUtils;
import org.matsim.core.network.algorithms.NetworkCleaner;
import org.matsim.core.network.NetworkWriter;
import org.matsim.core.scenario.ScenarioUtils;
import org.matsim.core.utils.geometry.CoordinateTransformation;
import org.matsim.core.utils.geometry.transformations.TransformationFactory;
import org.matsim.core.utils.io.OsmNetworkReader;

/**
 * "P" has to do with "Potsdam" and "Z" with "Zurich", but P and Z are mostly used to show which classes belong together.
 */
public class Networks{
        
        public static void main(String[] args) {
                
                /*
                 * The input file name.
                 */
                String osm = "E:/Braess_Paradox/OSM/network/bj-no.osm";
                
                
                /*
                 * The coordinate system to use. OpenStreetMap uses WGS84, but for MATSim, we need a projection where distances
                 * are (roughly) euclidean distances in meters.
                 * 
                * UTM 33N is one such possibility (for parts of Europe, at least).
                 * 
                */
               CoordinateTransformation ct = 
                        TransformationFactory.getCoordinateTransformation(TransformationFactory.WGS84, TransformationFactory.WGS84_UTM33N);
              
                /*
                * First, create a new Config and a new Scenario. One always has to do this when working with the MATSim 
                * data containers.
                 * 
                */
              Config config = ConfigUtils.createConfig();
                Scenario scenario = ScenarioUtils.createScenario(config);
               
              /*
                * Pick the Network from the Scenario for convenience.
                 */
                Network network = scenario.getNetwork();
               
                OsmNetworkReader onr = new OsmNetworkReader(network,ct);
              onr.parse(osm);
                
               /*
                * Clean the Network. Cleaning means removing disconnected components, so that afterwards there is a route from every link
                * to every other link. This may not be the case in the initial network converted from OpenStreetMap.
              */
               new NetworkCleaner().run(network);
                
               /*
                * Write the Network to a MATSim network file.
                 */
               new NetworkWriter(network).write("E:/Braess_Paradox/OSM/network/network-tmp.xml");
               
        }

}



```

转换完成后可以把得到的.XML文件放到Via可视化软件中查看一下。

我的地图是提取后的北京市二环的地图。效果如下：

没有提取主干道的效果：
 ![1](/images/study/2016-08-10/2.png)

提取了主干道的效果：
 ![2](/images/study/2016-08-10/3.png)