#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# author : zlq16
# date   : 2018/3/19
from scipy import stats
from scipy.stats import norm
import numpy as np
import pandas as pd
from collections import defaultdict

def int_split_unit(lens, step, arr, p, r):
    '''
    用于将整数划分
    :param lens:
    :param step:
    :param arr:
    :param p:
    :param r:
    :return:
    '''
    if lens == 0:
        r.append(arr[:p])
    for i in range(step, lens + 1, 1):
        arr[p] = i
        int_split_unit(lens - i, i, arr, p + 1, r)

def generate_discrete_norm_problity(sorted_arr):
    '''
    生成对应已经排序的数组每个数按照正太分布形成概率表
    :param sorted_arr: 商品集合
    :return:
    '''
    n = len(sorted_arr)
    d_v = sorted_arr[1] - sorted_arr[0]
    du_arr = sorted_arr - d_v / 2
    up_arr = sorted_arr + d_v / 2
    #根据中位数得到平均值
    loc = (sorted_arr[0] + sorted_arr[n-1]) / 2
    #根据3sigma原则决定sigma大小
    scale = (up_arr[n-1] - du_arr[0]) / 6
    p = np.zeros(shape=n,dtype=np.float)
    for i in range(n):
        p[i] = norm.cdf(up_arr[i],loc = loc,scale=scale)-\
               norm.cdf(du_arr[i],loc = loc,scale=scale)
    p = p + (1-np.sum(p))/n
    return p

def generate_discrete_possion_problity(time_serice,average):
    '''
    安装时间序列和平均值生成每一个时刻的概率
    :param time_serice: 时间序列
    :param average:     平均值
    :return:
    '''
    rx = stats.poisson(average)
    return rx.pmf(time_serice)

def generate_goods(capacity, alpha, goods, goods_p):
    '''
    根据最大限度生成一个商品总数
    :param capacity: 投标者的容积之和
    :param alpha:    实际市场中游客数目与capacity的比例
    :param goods:    商品集合
    :param goods_p:  获得商品概率
    :return:  一个键值对 表示每一个商品的数目
    '''
    real_tourist_number = int(capacity * alpha)
    gather_tourist_number = 0
    quantity = defaultdict(int)
    goods_idx = range(len(goods))
    while True:
        good_idx = np.random.choice(goods_idx,replace=False,p=goods_p)
        if goods[good_idx].union_number + gather_tourist_number < real_tourist_number:
            quantity[goods[good_idx]] += 1
            gather_tourist_number += goods[good_idx].union_number
        else:
            for good_idx in goods_idx:
                if goods[good_idx].union_number + gather_tourist_number == real_tourist_number:
                    quantity[goods[good_idx]] += 1
                    break
            break
    quantity = pd.Series(quantity,dtype=np.int32)
    return quantity

def generate_vf(V_e):
    '''
    随机生成固定成本函数
    :param V_e: 表示固定成本函数的幂函数系数
    :return:
    '''
    e = np.random.choice(V_e)
    return lambda x:np.power(x,e)

def N(bids):
    '''
    根据投标情况计算总的人数
    :param bids:  一个键值对 键:旅游团类型 值:数目
    :return: 人数
    '''
    total_number = 0
    kw = bids.to_dict()
    for good,quantity in kw.items():
        total_number += good.union_number * quantity
    return total_number
