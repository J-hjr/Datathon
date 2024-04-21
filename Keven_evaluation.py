import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("data.csv")
columns = ["median_monthly_costs_owner_occupied", "median_monthly_costs_renter_units", "families_median_income", "occupied_housing_units", "vacant_housing_units", ]
for column in df[columns]:
    df[column] = pd.to_numeric(df[column], errors='coerce')
df = df.dropna(subset=columns)
data = df[["families_median_income", "median_monthly_costs_owner_occupied", "median_monthly_costs_renter_units"]]

target_code = "1400000US12001000500"
target_line = df[df['geography'] == target_code]
target = data[df['geography'] == target_code].iloc[0]

df['Distance'] = np.sqrt(((data - target) ** 2).sum(axis=1))
df_sorted = df.sort_values(by='Distance')

nearest_points = df_sorted.sort_values(by='Distance').iloc[1:10]
total_vacant = 0
count = 0
for num in nearest_points["vacant_housing_units"]:
    if total_vacant >= target_line["occupied_housing_units"].item():
        break
    total_vacant += num
    count += 1

result = nearest_points.head(count)
print(result["geography"])

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# 选择三个维度
x = df_sorted['families_median_income']
y = df_sorted['median_monthly_costs_owner_occupied']
z = df_sorted['median_monthly_costs_renter_units']

norm = plt.Normalize(df_sorted['Distance'].min(), df_sorted['Distance'].max())
colors = plt.cm.viridis(norm(df_sorted['Distance']))

# 绘制散点图，颜色根据距离变化
scatter = ax.scatter(x, y, z, c=colors, marker='o')
ax.scatter(result['families_median_income'], result['median_monthly_costs_owner_occupied'], result['median_monthly_costs_renter_units'], color='red', marker='o')

# 创建颜色条
cbar = fig.colorbar(plt.cm.ScalarMappable(norm=norm, cmap='viridis'), ax=ax)
cbar.set_label('Distance')

# 设置轴标签
ax.set_xlabel('families_median_income')
ax.set_ylabel('median_monthly_costs_owner_occupied')
ax.set_zlabel('median_monthly_costs_renter_units')

# 设置标题
ax.set_title('Income and Housing Expenses')

# 显示图形
plt.show()
