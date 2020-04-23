#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# author : zlq16
# date   : 2018/9/5
import numpy as np


def affine_func(x, a_1, a_0):
    return a_1 * x + a_0


def quadro_func(x, a_2, a_1, a_0):
    return a_2 * x * x + a_1 * x + a_0


def triple_func(x, a_3, a_2, a_1, a_0):
   return a_3 * x * x * x + a_2 * x * x + a_1 * x + a_0


def generate_environment(
        alpha, price_get_tourist, goods, tourist_union,
        bidder_number, min_d, max_d, server_fee, capacities, v_e,
):
    from auction_base.utility import generate_goods
    from auction_base.utility import generate_vf
    from auction_base.utility import generate_discrete_norm_problity
    from vcg_approximate_auction.agent import Bidder, Platform
    goods_p = generate_discrete_norm_problity(tourist_union)
    capacity_p = generate_discrete_norm_problity(capacities)
    bidders = []
    for id in range(bidder_number):
        while True:
            D = np.random.uniform(min_d, max_d)
            unit_server_cost = server_fee
            capacity = np.random.choice(capacities, replace=False, p=capacity_p)
            v_f = generate_vf(v_e)
            bidder = Bidder(id, D, unit_server_cost, capacity, v_f, price_get_tourist)
            if bidder.real_value(bidder.capacity) > 0: # 如果可以盈利了就退出循环
                break
        bidders.append(bidder)

    n = np.sum([bidder.capacity for bidder in bidders])
    quantity = generate_goods(n,alpha,goods,goods_p)
    platform = Platform(quantity)
    return bidders,platform


def print_env(bidders, platform):
    for bidder in bidders:
        print(bidder,end=" ")
        print([bidder.price_get_tourist*n - bidder.cost[n] for n in range(bidder.capacity+1)])
    print("需求的总人数为:{0}".format(sum([bidder.capacity for bidder in bidders])))
    print(platform)
    from auction_base.utility import N
    print("供应的总人数为:{0}".format(N(platform.supplies)))


def fit_all_approximate_values(bidders,mode):
    for bidder in bidders:
        bidder.fit_approximate_value(mode)


def compute_social_welfare(bidders, allocation,mode):
    """
    bidders按照allocation进行分配求解最大社会福利
    :param bidders:
    :param allocation:
    :param mode:
    :return:
    """
    if  mode == "approximate":
        return sum([bidder.approximate_value(allocation[bidder]) for bidder in bidders])
    elif mode == "misreported":
        return sum([bidder.misreported_value(allocation[bidder]) for bidder in bidders])
    elif mode == "real":
        return sum([bidder.real_value(allocation[bidder]) for bidder in bidders])
