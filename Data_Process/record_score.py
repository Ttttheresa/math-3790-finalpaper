import os
import csv
from Backtest.trade import Trade

class RecordFunction:
    def __init__(self, trader, parameters, strategy, date) -> None:
        self.parameters = parameters
        self.s = strategy
        self.date = date.strftime('%Y%m%d')  # 确保传入的 date 是 datetime 对象
        self.dataName = f"{self.s.dataName} {self.date}"
        self.t = Trade(strategy=strategy, trader=trader)
        self.pnl = self.t.pnl
        self.return_rate = self.t.return_rate
        self.varNames = list(parameters.keys())[:5]

        weights = ["w" + str(i+1) for i in range(len(parameters['weights']))]
        self.varNames += weights
        self.colNames = self.varNames + ["PnL", "Return"]

        self.record_data()

    def record_data(self):
        data_dict = {col: self.parameters.get(col) for col in self.varNames}
        data_dict["PnL"] = self.t.pnl
        data_dict["Return"] = self.t.return_rate

        file_path = f"EUR_GBP_{self.date}.csv"
        file_exists = os.path.exists(file_path)
        with open(file_path, mode="a", encoding="big5", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=self.colNames, delimiter=",")
            if not file_exists:
                writer.writeheader()
            writer.writerow(data_dict)