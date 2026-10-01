"""
InSAR相位误差仿真，分解DEM残差相位、大气湍流相位、热噪声
输出：insar_error_decompose.png
"""
import numpy as np
import matplotlib.pyplot as plt

# ===================== 参数 =====================
nx, ny = 100, 100
x = np.linspace(-50,50,nx)
y = np.linspace(-50,50,ny)
xx, yy = np.meshgrid(x,y)

# ===================== 1. DEM残差相位（与空间基线相关，长波地形残差） =====================
# DEM残差高度误差
dem_err = 2.0 * np.sin(xx/20) * np.cos(yy/20)
lambda_c = 0.056
B_perp = 80
R = 80000
theta = np.radians(38)
# DEM残差相位公式
phase_dem = 4 * np.pi * dem_err * B_perp / (lambda_c * R * np.sin(theta))

# ===================== 2. 大气湍流相位（分形，空间相关短/长波大气延迟） =====================
def fractal_noise(nx, ny, exponent=-8/3):
    kx = np.fft.fftfreq(nx)
    ky = np.fft.fftfreq(ny)
    kxx, kyy = np.meshgrid(kx, ky)
    k = np.sqrt(kxx**2 + kyy**2)
    k[0,0] = 1e-8
    power = np.power(k, exponent)
    noise_ft = power * np.exp(1j * np.random.randn(nx, ny))
    noise = np.real(np.fft.ifft2(noise_ft))
    noise = noise / np.std(noise)
    return noise

phase_atm = fractal_noise(nx, ny) * 0.8

# ===================== 3. 热噪声（白噪声，失相干噪声） =====================
phase_noise = np.random.normal(0, 0.3, size=(nx, ny))

# 总误差相位
phase_total_err = phase_dem + phase_atm + phase_noise

# ===================== 绘图 =====================
fig, axes = plt.subplots(2,2, figsize=(12,10))
axes = axes.flatten()
im0 = axes[0].imshow(phase_dem, cmap="jet")
axes[0].set_title("DEM残差相位")
plt.colorbar(im0, ax=axes[0])

im1 = axes[1].imshow(phase_atm, cmap="jet")
axes[1].set_title("大气湍流相位")
plt.colorbar(im1, ax=axes[1])

im2 = axes[2].imshow(phase_noise, cmap="jet")
axes[2].set_title("热噪声相位")
plt.colorbar(im2, ax=axes[2])

im3 = axes[3].imshow(phase_total_err, cmap="jet")
axes[3].set_title("总相位误差")
plt.colorbar(im3, ax=axes[3])

plt.suptitle("InSAR相位误差分量分解仿真", fontsize=14)
plt.tight_layout()
plt.savefig("insar_error_decompose.png", dpi=150)
plt.close()
print("相位误差分解仿真完成，图片保存：insar_error_decompose.png")
