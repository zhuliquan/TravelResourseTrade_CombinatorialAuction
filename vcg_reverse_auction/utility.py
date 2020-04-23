#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# author : zlq16
# date   : 2018/10/25
def generate_environment(
        alpha,predict_price_mui,predict_price_sigma, goods, tourist_union,
        bidder_number, min_d, max_d, server_fee, capacities, v_e,
):
    import numpy as np
    from auction_base.utility import N
    from auction_base.utility import generate_goods
    from auction_base.utility import generate_vf
    from auction_base.utility import generate_discrete_norm_problity
    from vcg_reverse_auction.agent import Bidder, VirtualBidder,Platform
    goods_p = generate_discrete_norm_problity(tourist_union)
    capacity_p = generate_discrete_norm_problity(capacities)
    bidders = []
    real_bidders = []
    for id in range(1, bidder_number+1):
        D = np.random.uniform(min_d, max_d)
        unit_server_cost = server_fee
        capacity = np.random.choice(capacities, replace=False, p=capacity_p)
        v_f = generate_vf(v_e)
        bidder = Bidder(id, D, unit_server_cost, capacity, v_f)
        real_bidders.append(bidder)

    n = np.sum([bidder.capacity for bidder in real_bidders])
    quantity = generate_goods(n,alpha,goods,goods_p)
    platform = Platform(quantity,predict_price_mui, predict_price_sigma)
    # 将platform 转化成为一个虚拟的投标者
    virtual_bidder = VirtualBidder(platform.predict_price_mui + platform.predict_price_sigma ,
                                   N(quantity))
    bidders.append(virtual_bidder)
    for bidder in real_bidders:
        bidders.append(bidder)
    return bidders,platform

def generate_goods():
    pass

def print_env(bidders, platform):
    real_bidders = bidders[1:]
    for bidder in real_bidders:
        print(bidder,end=" ")
        print([bidder.cost[n] for n in range(bidder.capacity+1)])
    print("需求的总人数为:{0}".format(sum([bidder.capacity for bidder in real_bidders])))
    print(platform)
    from auction_base.utility import N
    print("供应的总人数为:{0}".format(N(platform.supplies)))

def compute_social_cost(bidders, allocation):
    """
    bidders按照allocation进行分配求解最大社会福利
    :param bidders:
    :param allocation:
    :param mode:
    :return:
    """
    return sum([bidder.cost[allocation[bidder]] for bidder in bidders])
