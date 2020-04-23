#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# author : zlq16
# date   : 2018/3/21
import numpy as np
from auction_base.item import Item
###global setting###
# cost(bidder) = P_s * n_i * d_i^(-n_i/C_i) + v_f(C_i)
BIDDER_NUMBER = 10                      #n   买家的数目
SERVER_FEE = 1.0                       #P_s 买家为每一个游客的服务费用
MIN_CAPACITY = 10                      #C_i 买家最小可以运载的游客数目
MAX_CAPACITY = 30                      #C_i 买家最大可以运载的游客数目
MAX_U = 6                              #m   环境中最大一起出行的人数 max(g_j)
MIN_D = 1.2
MAX_D = np.e
V_E = np.linspace(0.3, 0.4, 10)        #买家的固定成本函数的指数部分
CAPACITIES = np.arange(MIN_CAPACITY,MAX_CAPACITY+1,1) #买家可以承载的游客数目
ALPHA = 0.5                             # 表示生成的游客资源占总体的供应商的比例
TOURIST_DESTINATION = ["Shanghai",
                       "Beijing",
                       "Sanya",
                       "Haikou",]      # 旅游地点
GOODS = [Item(TOURIST_DESTINATION[0], i) for i in range(1, MAX_U + 1)]
TOURIST_UNION = np.array([good.union_number for good in GOODS])
