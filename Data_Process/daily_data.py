import os
import pandas as pd

base_path = "E:\\Work\\MSc-Individual-Project-main_my version"
data_path = os.path.join(base_path, "Experiment copy")
output_path = os.path.join(base_path, "daily_data")

# 确保输出目录存在
os.makedirs(output_path, exist_ok=True)

# 读取一个大的CSV文件
input_file = os.path.join(data_path, "EURUSD-2024-03.csv")  # 假设存在一个包含整月数据的大文件
df = pd.read_csv(input_file, sep=",", names=["Currency", "Time", "Bid", "Ask"])

# 转换时间格式
df['Time'] = pd.to_datetime(df['Time'], format='%Y%m%d %H:%M:%S.%f')

# 按日期分组
grouped = df.groupby(df['Time'].dt.date)

# 循环处理每个组（每一天）
for date, group in grouped:
    # 构建输出文件名，基于日期
    output_file_path = os.path.join(output_path, f"EURUSD_{date}.csv")
    
    # 保存每天的数据到单独的文件中
    group.to_csv(output_file_path, index=False)