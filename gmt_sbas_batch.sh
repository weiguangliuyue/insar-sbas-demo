#!/bin/bash
# GMTSAR SBAS完整业务处理流水线演示脚本
# 仅流程演示，仿真脚本，不可直接跑真实数据，用于熟悉GMTSAR InSAR业务处理
echo "==== GMTSAR SBAS 处理流水线演示开始 ===="

# 1. 数据准备：Sentinel-1 SLC + orbit精密轨道 + DEM
echo "[1] 准备Sentinel-1 SLC影像、精密轨道文件、DEM"
# mkdir -p raw_slc orbits dem interferograms sbas_result

# 2. GMTSAR预处理：SLC配准、重采样
echo "[2] GMTSAR预处理：SLC影像配准，基于轨道+DEM几何配准"
# align_slc.csh master.SLC slave.SLC dem.grd

# 3. 生成干涉图、去地形相位
echo "[3] 生成干涉图，去除地形相位"
# xcorr.csh master slave
# phase_sim_orb.csh master slave dem.grd

# 4. 滤波 + 相位解缠 SNAPHU
echo "[4] 干涉图Goldstein滤波，SNAPHU相位解缠"
# filter.csh phase.grd filt_phase.grd
# snaphu.csh filt_phase.grd unwrap.grd

# 5. SBAS小基线集构建，基线筛选
echo "[5] SBAS基线筛选，构建小基线干涉对集合"
# sbas_select_pairs.csh baseline_table.txt temp_thresh space_thresh

# 6. SBAS时序反演，求解形变速率与时序形变
echo "[6] SBAS时序反演：SVD最小二乘求解LOS形变速率场"
# sbas_invert.csh unwrap_list.txt dem.grd velocity.grd ts_deform.grd

# 7. 后处理：大气校正、掩膜失相干区域、专题制图
echo "[7] 后处理：大气延迟校正，失相干掩膜，GMT专题图输出"
# mask_coh.csh coherence.grd velocity.grd mask_vel.grd
# gmt_plot_velocity.csh mask_vel.grd deform_map.ps

echo "==== GMTSAR SBAS流水线演示结束 ===="
echo "说明：本脚本仅演示真实Sentinel-1数据业务处理流程，当前项目为仿真代码，无真实SLC数据无法执行上述命令。"
