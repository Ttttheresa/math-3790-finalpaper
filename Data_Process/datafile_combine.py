import os, glob
import pandas as pd

base_path = "E:\Work\MSc-Individual-Project-main_my version"
data_path = os.path.join(base_path, "Experiment copy")
output_path = os.path.join(base_path, "daily_data")

# 确保输出目录存在
os.makedirs(output_path, exist_ok=True)

# 获取所有符合条件的文件
all_files = glob.glob(os.path.join(data_path, "EURUSD-2024-03*.csv"))
all_files.sort()

# 循环处理每个文件
for f in all_files:
    try:
        # 读取CSV文件，指定列名
        day_df = pd.read_csv(f, sep=",", names=["Currency", "Time", "Bid", "Ask"])

        # 提取文件名中的日期部分
        date_part = os.path.basename(f).split('.')[0][-8:]  # 假设文件名如 "EURUSD_20240301.csv"

        # 构建完整的输出文件路径
        output_file_path = os.path.join(output_path, f"EURUSD_{date_part}.csv")

        # 转换时间格式
        day_df['Time'] = pd.to_datetime(day_df['Time'], format='%Y%m%d %H:%M:%S.%f')

        # 保存每天的数据到单独的文件中
        day_df.to_csv(output_file_path, index=False)

    except Exception as e:
        print(f"Failed to process file {f}: {e}")
