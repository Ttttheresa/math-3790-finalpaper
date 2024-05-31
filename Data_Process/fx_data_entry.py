# 遍历每日数据文件
from .util import util

class FX_data:
    def __init__(self, file_path, currency_pair, time) -> None:
        self.file_path = file_path
        self.currency_pair = currency_pair
        self.time = time
        self.data_name = currency_pair + " " + time
        self.data = util.dataProcess(file_path=file_path)
        self.nTimeSteps = len(self.data)
        self.timelist = self.data['Time'].to_list()


