#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# author : zlq16
# date   : 2018/10/26
if __name__ == '__main__':
    import matplotlib.pyplot as plt
    import numpy as np
    from vcg_reverse_auction.setting import PREDICT_PRICE_MUI, PREDICT_PRICE_SIGMA
    from auction_base.setting import ALPHA, GOODS, TOURIST_UNION
    from auction_base.setting import BIDDER_NUMBER, MIN_D, MAX_D, SERVER_FEE, CAPACITIES, V_E
    from vcg_reverse_auction.utility import generate_environment, print_env
    from vcg_reverse_auction.auction import determine_allocation_with_clear_market
    from vcg_reverse_auction.utility import compute_social_cost

    bidders, platform = generate_environment(
        ALPHA, PREDICT_PRICE_MUI, PREDICT_PRICE_SIGMA, GOODS, TOURIST_UNION,
        BIDDER_NUMBER, MIN_D, MAX_D, SERVER_FEE, CAPACITIES, V_E,
    )

    plt.figure()
    plt.grid(True)
    real_bidders = bidders[1:]
    for bidder in real_bidders:
        x = np.arange(1, bidder.capacity+1)
        y = bidder.cost[1:]
        plt.plot(x, y)
    plt.show()

