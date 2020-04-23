#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# author : zlq16
# date   : 2018/11/11
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
if __name__ == '__main__':
    data = {}
    alphas = ["0.50", "0.55", "0.60", "0.65", "0.70", "0.75", "0.80", "0.85", "0.90", "0.95", "1.00"]
    reserved_prices = ["0.8", "0.9", "1.0", "1.1", "1.2"]
    for alpha in alphas:
        for reserved_price in reserved_prices:
            data[alpha, reserved_price] = np.load("./data/{0}_{1}.npy".format(alpha,reserved_price))

    # 线图
    # line_style = ["b-^","b-.-*","b-.","",""]
    # ax1 = plt.subplot(131)
    plt.rc('font', family='Times New Roman')
    fs = 16
    plt.figure(1)
    for reserved_price in reserved_prices:
        ts = []
        for alpha in alphas:
            key = alpha, reserved_price
            t = np.mean(data[key][:, 4])
            ts.append(t)
        x = list(map(float, alphas))
        plt.plot(x, ts)
        # ax1.plot(x, ts)
        # dfs[reserved_price] = df
        # plt.boxplot(df,widths=0.3)
    plt.xlim([0.50, 1.00])
    plt.xlabel("Supply and Demand Ratio", fontsize=fs)
    plt.ylabel("Task Clearing Ratio", fontsize=fs)
    plt.legend(reserved_prices, title="Reserve Price")
    plt.grid(True)
    plt.savefig("performance1.png")

    # ax2 = plt.subplot(132)
    plt.figure(2)
    for reserved_price in reserved_prices:
        ts = []
        for alpha in alphas:
            key = alpha, reserved_price
            t = np.mean(data[key][:, 1])
            ts.append(t)
        x = list(map(float, alphas))
        plt.plot(x, ts)
        # ax2.plot(x,ts)
        # dfs[reserved_price] = df
        # plt.boxplot(df,widths=0.3)
    plt.xlim([0.50, 1.00])
    plt.xlabel("Supply and Demand Ratio",fontsize=fs)
    plt.ylabel("Average Worker Profit Ratio",fontsize=fs)
    plt.legend(reserved_prices, title="Reserve Price")
    plt.grid(True)
    plt.savefig("performance2.png")

    # ax3 = plt.subplot(133)
    plt.figure(3)
    for reserved_price in reserved_prices:
        ts = []
        for alpha in alphas:
            key = alpha, reserved_price
            t = np.mean(data[key][:, 5])
            t = 1 - t/float(reserved_price)
            ts.append(t)
        x = list(map(float, alphas))
        plt.plot(x, ts)
        # ax3.plot(x,ts)
        # dfs[reserved_price] = df
        # plt.boxplot(df,widths=0.3)
    plt.xlim([0.50, 1.00])
    plt.xlabel("Supply and Demand Ratio", fontsize=fs)
    plt.ylabel("Average Requester Protection Ratio",fontsize=fs)
    plt.legend(reserved_prices, title="Reserve Price")
    plt.grid(True)
    plt.savefig("performance3.png")
    # plt.show()
