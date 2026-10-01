
# 【文件名】sbas_insar_simulation.py
```python
"""
SBAS-InSAR时序地表形变仿真
功能：模拟SAR时间序列、干涉对，最小二乘+SVD反演LOS形变速率
输出：sbas_result.png
面向：InSAR岗位秋招项目演示
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import svd

# ===================== 1. 仿真参数设置 =====================
n_time = 12          # SAR影像时序数量
time_days = np.linspace(0, 330, n_time)  # 时间轴，单位天
space_baseline_std = 80  # 空间基线标准差 m
threshold_temp = 90   # 时间基线阈值 天
threshold_spa = 120   # 空间基线阈值 m

# 模拟真实形变速率 mm/yr，LOS向
v_true = 8.0
# 模拟每个时间点的累积形变 mm
cum_deform_true = v_true * time_days / 365.0

# 生成随机空间基线
baselines = np.random.normal(0, space_baseline_std, n_time)

# ===================== 2. 构建小基线干涉对 =====================
pairs = []
for i in range(n_time):
    for j in range(i+1, n_time):
        dt = time_days[j] - time_days[i]
        db = baselines[j] - baselines[i]
        if dt < threshold_temp and abs(db) < threshold_spa:
            pairs.append([i, j])
n_pairs = len(pairs)
print(f"生成干涉对数量：{n_pairs}")

# 模拟干涉相位差 (形变相位 + 少量噪声)
# 相位和形变关系: phase = -4pi/lambda * displacement, C波段lambda=0.056m
lambda_c = 0.056
phase_factor = -4 * np.pi / lambda_c

# 构建观测向量d: 每个干涉对的相位差
d = np.zeros(n_pairs)
for idx, (i,j) in enumerate(pairs):
    delta_disp = cum_deform_true[j] - cum_deform_true[i]
    phase = phase_factor * (delta_disp * 1e-3)
    # 添加少量高斯噪声
    noise = np.random.normal(0, 0.2)
    d[idx] = phase + noise

# ===================== 3. SBAS矩阵构建 =====================
# G矩阵: n_pairs × (n_time-1)
G = np.zeros((n_pairs, n_time - 1))
for idx, (i,j) in enumerate(pairs):
    for k in range(i, j):
        dt_k = time_days[k+1] - time_days[k]
        G[idx, k] = dt_k

# ===================== 4. SVD求解最小二乘 =====================
U, s, Vt = svd(G, full_matrices=False)
s_inv = np.zeros_like(s)
tol = 1e-6
for i in range(len(s)):
    if s[i] > tol:
        s_inv[i] = 1.0 / s[i]
# 求解速率 v: mm/day
v_sol = Vt.T @ (s_inv * (U.T @ d))
# 积分得到累积形变
cum_deform_sol = np.zeros(n_time)
for t in range(1, n_time):
    dt = time_days[t] - time_days[t-1]
    cum_deform_sol[t] = cum_deform_sol[t-1] + v_sol[t-1] * dt

# 转换单位 mm
cum_deform_sol_mm = cum_deform_sol / phase_factor * 1000

# ===================== 5. 绘图输出 =====================
plt.figure(figsize=(10,6))
plt.plot(time_days, cum_deform_true, 'o-', label='真实累积形变', linewidth=2)
plt.plot(time_days, cum_deform_sol_mm, 'x--', label='SBAS反演累积形变', linewidth=2)
plt.xlabel('时间 (天)')
plt.ylabel('LOS累积形变 (mm)')
plt.title('SBAS-InSAR时序形变仿真反演结果')
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig("sbas_result.png", dpi=150)
plt.close()
print("SBAS仿真完成，结果图已保存：sbas_result.png")
print(f"真实形变速率: {v_true:.2f} mm/yr")
v_sol_yr = np.mean(v_sol)*365 / phase_factor *1000
print(f"反演平均形变速率: {v_sol_yr:.2f} mm/yr")
