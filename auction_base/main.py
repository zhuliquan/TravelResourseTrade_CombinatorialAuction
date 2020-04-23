#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# author : zlq16
# date   : 2018/10/12
if __name__ == '__main__':
    #### 测试 ####
    import numpy as np
    from auction_base.utility import generate_discrete_norm_problity
    from auction_base.utility import generate_goods
    from auction_base.utility import generate_vf
    from auction_base.utility import N
    from auction_base.setting import ALPHA, SELLER_PRICE, GOODS, TOURIST_UNION
    from auction_base.setting import BIDDER_NUMBER, D_MUI, D_SIGMA, SERVER_FEE, CAPACITIES, V_E
    from auction_base.agent import BaseBidder,BasePlatform
    goods_p = generate_discrete_norm_problity(TOURIST_UNION)
    capacity_p = generate_discrete_norm_problity(CAPACITIES)
    bidders = []
    for i in range(BIDDER_NUMBER):
        id = i
        D = np.random.normal(D_MUI, D_SIGMA)
        unit_server_cost = SERVER_FEE
        capacity = np.random.choice(CAPACITIES,replace=False,p=capacity_p)
        v_f = generate_vf(V_E)
        bidder = BaseBidder(id,D,unit_server_cost,capacity,v_f)
        bidders.append(bidder)
        print(bidder)
        print(bidder.margin_cost)

    n = np.sum([bidder.capacity for bidder in bidders])
    quantity = generate_goods(n, ALPHA, GOODS, goods_p)
    seller = BasePlatform(SELLER_PRICE, quantity)
    print(seller)
    print(N(seller.supplies))


    # import matplotlib.pyplot as plt
    # from auction_base.setting import V_E
    # x = np.linspace(0.1,100,1000)
    # for _ in range(10):
    #     plt.plot(x,generate_vf(V_E)(x))
    # plt.show()