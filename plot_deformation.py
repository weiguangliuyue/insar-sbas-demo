"""
PyGMT脚本：模拟滑坡形变网格，绘制LOS形变专题图
输出：gmt_deform_map.png
"""
import pygmt
import numpy as np

# 生成模拟滑坡网格形变数据
nx, ny = 120,120
lon_min, lon_max = 100.2, 100.6
lat_min, lat_max = 25.1, 25.4
lon = np.linspace(lon_min, lon_max, nx)
lat = np.linspace(lat_min, lat_max, ny)
lon_grid, lat_grid = np.meshgrid(lon, lat)

# 模拟滑坡中心，LOS形变负值代表向卫星靠近
center_lon, center_lat = 100.4, 25.25
sigma_lon, sigma_lat = 0.06, 0.04
deform = -12 * np.exp(
    -((lon_grid-center_lon)**2/(2*sigma_lon**2) + (lat_grid-center_lat)**2/(2*sigma_lat**2))
)

# 保存为网格文件
grd = pygmt.GMTData(x=lon, y=lat, z=deform)

# GMT绘图
fig = pygmt.Figure()
fig.basemap(region=[lon_min, lon_max, lat_min, lat_max], projection="M12c", frame=["a", "+t滑坡LOS地表形变图"])
fig.grdimage(grd, cmap="roma", nan_transparent=True)
fig.colorbar(frame=["x+lLOS形变 mm/yr"])
fig.coast(shorelines="0.3p,black", land="#f0f0f0")
fig.savefig("gmt_deform_map.png", dpi=150)
print("PyGMT形变专题图绘制完成：gmt_deform_map.png")
