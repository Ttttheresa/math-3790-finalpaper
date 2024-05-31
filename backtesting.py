import os
import sys
from Data_Process.fx_data_entry import FX_data
from Strategy.MTS import MTS
from Strategy.BandH import BandH
from Strategy.MACD import MACD
from Strategy.RSI import RSI
from Strategy.STS import STS
from Backtest.trade import Trade
import pandas as pd

# 基本路径和数据处理
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# 参数设定
evalution_dict = {}
estimated_param = [0.3, 0.6, 1, 0.002, 0.004, 0.005, 0.008]
weight = [1, 1, 1, 1]
threshold_ls = [0.002, 0.004, 0.005, 0.008]
estimated_r_mutiplier = [[3.7, 5.26],[2.87, 2.32],[2.86, 1.37],[3, 1.42]]
budget = 9500000

i = 1

# for currency in ["EURUSD", "AUDUSD", "USDCAD"]:
for currency in ["EURUSD","USDCAD","AUDUSD"]:
    print(currency)
    if currency == "EURUSD":
        test_currency = "EURUSD"  # e.g. EURUSD
        data_ls = ["EURUSD-2024-01","EURUSD-2024-02","EURUSD-2024-03","EURUSD-2024-04"]
        budget = 9500000
        estimated_r_mutiplier = [[3.7, 5.26], [2.87, 2.32], [2.86, 1.37], [3, 1.42]]

        estimated_param_2 = [0.29, 0.59, 0.73, 0.002, 0.004, 0.005, 0.008]
        weight_2 = [0.68, 0.14, 0.83, 0.56]

    elif currency == "AUDUSD":
        test_currency = "AUDUSD"  # e.g. AUDUSD
        data_ls = ["AUDUSD-2024-01","AUDUSD-2024-02","AUDUSD-2024-03","AUDUSD-2024-04"]
        budget = 180000
        estimated_r_mutiplier = [[3.11, 5.58], [2.29, 5.58], [2.21, 2.20], [3, 45, 1.61]]

        estimated_param_2 = [0.29, 0.46, 0.71, 0.002, 0.004, 0.005, 0.008]
        weight_2 = [0.29, 0.41, 0.12, 0.94]

    elif currency == "USDCAD":
        test_currency = "USDCAD"  # e.g. AUDJPY
        data_ls = ["USDCAD-2024-01","USDCAD-2024-02","USDCAD-2024-03","USDCAD-2024-04"]
        budget = 150000
        estimated_r_mutiplier = [[3.02, 4.81], [2.22, 4.72], [2.79, 2.14], [2.21, 2.14]]

        estimated_param_2 = [0.3, 0.6, 0.75, 0.002, 0.004, 0.005, 0.008]
        weight_2 = [0.75, 0.96, 0.14, 0.78]

    for data in data_ls:
        file_path = ("E:\Work\MSc-Individual-Project-main_my version/Experiment copy/"
                    + data + ".csv")

    # initial asset
        trader = {
        "cash": budget,
        "Q trade": 1
        }
        time = data[-6:]
        fx_data_saver = FX_data(file_path=file_path,
                                currency_pair=test_currency,time=time)
        
        """
        Buy and Hold
        """
        print("case1")
        buy_and_hold = BandH(fx_data_saver)
        # # 确认时间数据处理
        # print("Time data extracted:", data[-6:])

        # # 打印 FX_data 保存器实例和相关属性
        # print("FX data saver instance data:", fx_data_saver.data)
        # print("FX data saver instance data:", fx_data_saver.timelist)
        # print("Currency pair:", fx_data_saver.currency_pair)
        # print("File path:", fx_data_saver.file_path)

        # # 打印买入持有策略实例和可能的属性
        # print("Buy and Hold strategy instance:", buy_and_hold)

        # # 打印交易者信息
        # print("Trader dictionary:", trader)
        # print("Trader cash:", trader['cash'])
        # print("Trader Q trade:", trader['Q trade'])
        # print("fx_data_saver",fx_data_saver)
        # print("buy_and_hold",buy_and_hold)
        # print("trader",trader)
        t1 = Trade(fx_data_saver, buy_and_hold, trader)
        # print(t1.pnl_record)
        t1.backtest()
        df = pd.DataFrame(t1.pnl_record)
        evalution_dict[str(i)] = [test_currency, "B&H", time, "None",
                                t1.total_pnl, t1.fitness,
                                t1.total_return,
                                t1.std_dev_returns,
                                t1.max_drawdown, t1.win_rate, len(df)]
        i += 1

        """
        RSI
        """
        print("case2")
        print(fx_data_saver.nTimeSteps)
        rsi = RSI(fx_data_saver)
        t1 = Trade(fx_data_saver, rsi, trader)
        t1.backtest()
        df = pd.DataFrame(t1.pnl_record)
        evalution_dict[str(i)] = [test_currency, "RSI", time, "None",
                                t1.total_pnl, t1.fitness,
                                t1.total_return,
                                t1.std_dev_returns,
                                t1.max_drawdown, t1.win_rate, len(df)]
        i += 1

        """
        MACD
        """
        print("case3")
        macd = MACD(fx_data_saver)

        t1 = Trade(fx_data_saver, macd, trader)
        t1.backtest()
        df = pd.DataFrame(t1.pnl_record)
        evalution_dict[str(i)] = [test_currency, "MACD", time, "None",
                                t1.total_pnl, t1.fitness,
                                t1.total_return,
                                t1.std_dev_returns,
                                t1.max_drawdown, t1.win_rate, len(df)]
        i += 1

        """
        STS
        """
        print("case4")
        j = 0
        print("evalution_dict",evalution_dict)
        print("threshold_ls",threshold_ls)
        for thres in threshold_ls:
            sts = STS(fx_data_saver,
                    estimated_r_mutiplier[j],
                    estimated_param_2 + [thres])
            t1 = Trade(fx_data_saver, sts, trader)
            t1.backtest()
            df = pd.DataFrame(t1.pnl_record)
            evalution_dict[str(i)] = [test_currency, "STS", time, thres,
                                    t1.total_pnl, t1.fitness,
                                    t1.total_return,
                                    t1.std_dev_returns,
                                    t1.max_drawdown, t1.win_rate, len(df)]
            i += 1
            j += 1

        """
        MTS
        """
        print("case5")
        TS1_multi = MTS(fx_data_saver, estimated_r_mutiplier, estimated_param)
        TS1_multi.go_strategy(weight)
        t1 = Trade(fx_data_saver, TS1_multi, trader)
        t1.backtest()
        df = pd.DataFrame(t1.pnl_record)
        evalution_dict[str(i)] = [test_currency, "MTS", time, "All",
                                t1.total_pnl, t1.fitness,
                                t1.total_return,
                                t1.std_dev_returns,
                                t1.max_drawdown, t1.win_rate, len(df)]

        i += 1
        """
        MTSGA
        """
        print("case6")
        TS1_multi = MTS(fx_data_saver, estimated_r_mutiplier, estimated_param_2)
        TS1_multi.go_strategy(weight_2)
        t1 = Trade(fx_data_saver, TS1_multi, trader)
        t1.backtest()
        df = pd.DataFrame(t1.pnl_record)
        evalution_dict[str(i)] = [test_currency, "MTSGA", time, "All",
                                t1.total_pnl, t1.fitness,
                                t1.total_return,
                                t1.std_dev_returns,
                                t1.max_drawdown, t1.win_rate, len(df)]
        i += 1

        evalution_df = pd.DataFrame(evalution_dict, index=["Currency", "Strategy",
                                                    "Time", "Threshold",
                                                    'PnL', 'Fitness',
                                                    'TR',
                                                    'std(RR)',
                                                    'MDD', 'Win Rate', 'nTrade'])
evalution_df.to_csv('Backtest.csv')
import sys
print(sys.path)
