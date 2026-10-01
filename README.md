# insar-sbas-demo
SBAS-InSAR时序地表形变仿真项目
> 面向秋招：东方至远、天仪研究院、中科卫星 InSAR遥感处理岗位，地球物理本科背景

## 项目简介
本项目实现**SBAS（Small Baseline Subset）小基线集InSAR时序地表形变仿真**，不依赖真实SAR原始数据，通过数值模拟生成时序干涉相位、DEM残差、大气相位、热噪声，构建小基线干涉对集合，利用奇异值分解+最小二乘反演地表LOS（视线向）形变速率与时序形变。
项目包含：相位误差分解仿真、SBAS时序反演、PyGMT滑坡形变专题图绘制、GMTSAR处理流水线shell演示脚本。
用于理解InSAR时序形变反演核心原理、相位误差来源，熟悉InSAR数据处理全流程，适配遥感InSAR岗位面试与简历项目展示。

## 技术栈
- Python：numpy、scipy、matplotlib、pygmt
- 数值算法：奇异值分解SVD、最小二乘反演、时序相位建模
- 制图：PyGMT（GMT）遥感专题图绘制
- Shell：GMTSAR InSAR处理流水线脚本
- Git + GitHub：代码版本管理

## 项目模块
1. `sbas_insar_simulation.py`：SBAS-InSAR核心仿真，构建干涉对，反演LOS形变速率与时序形变，输出 `sbas_result.png`
2. `phase_error_simulation.py`：InSAR相位误差分解仿真，模拟DEM残差相位、大气湍流相位、热噪声相位，输出 `insar_error_decompose.png`
3. `plot_deformation.py`：PyGMT绘制滑坡区域LOS形变网格专题图，输出 `gmt_deform_map.png`
4. `gmt_sbas_batch.sh`：GMTSAR SBAS完整业务处理流水线演示脚本（真实数据处理流程模拟）

## 原理说明
SBAS-InSAR核心思想：
1. 选取时间基线+空间基线均小于阈值的干涉对，降低时空失相干；
2. 将各干涉图相位差转化为形变增量方程；
3. 构建观测矩阵，通过SVD+最小二乘求解每个时间间隔平均形变速率，积分得到时序形变；
4. InSAR观测相位 = 形变相位 + DEM残差相位 + 大气相位 + 噪声相位；本项目单独对各类误差分量进行仿真分解，理解误差对形变反演的影响。

![SBAS反演时序形变结果](sbas_result.png)
![InSAR相位误差分解图](insar_error_decompose.png)
![GMT滑坡LOS形变专题图](gmt_deform_map.png)

## 运行依赖
```bash
pip install numpy matplotlib scipy pygmt rasterio
