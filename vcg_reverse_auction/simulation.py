#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# author : zlq16
# date   : 2018/10/25


def test_alpha_reserved_price(alpha, reserve_price):
    from auction_base.setting import GOODS, TOURIST_UNION
    from auction_base.setting import BIDDER_NUMBER, MIN_D, MAX_D, SERVER_FEE, CAPACITIES, V_E
    from vcg_reverse_auction.utility import generate_environment, print_env
    from vcg_reverse_auction.auction import determine_allocation_with_clear_market
    from vcg_reverse_auction.utility import compute_social_cost

    bidders, platform = generate_environment(
        alpha, reserve_price, 0.0, GOODS, TOURIST_UNION,
        BIDDER_NUMBER, MIN_D, MAX_D, SERVER_FEE, CAPACITIES, V_E,
    )

    # print_env(bidders, platform)
    status, vcg_allocation = determine_allocation_with_clear_market(bidders, platform)

    # print("####### 分配结果 #######")
    # for bidder in bidders:
    #     print("{0} 分配人数 {1:<3} 成本为 {2:.5}".format(bidder.__str__(),
    #                                               vcg_allocation[bidder],
    #                                               bidder.cost[vcg_allocation[bidder]]))

    # print("####### 支付情况 #######")
    vcg_social_cost = compute_social_cost(bidders, vcg_allocation)
    I = list(range(len(bidders)))
    vcg_payment = {}
    for i in I:
        if i == 0: continue
        other_bidders = [bidders[j] for j in I if j != i]
        status, other_allocation = determine_allocation_with_clear_market(other_bidders, platform)
        other_social_cost = compute_social_cost(other_bidders, other_allocation)
        bidder_i_cost = bidders[i].cost[vcg_allocation[bidders[i]]]
        remove_i_cost = vcg_social_cost - bidder_i_cost
        payment_i = other_social_cost - remove_i_cost
        vcg_payment[bidders[i]] = payment_i

        # print("计算bidder{0:<3}的支付".format(bidders[i].id))
        # print("{0}".format(bidders[i]), end=" ")
        # print("分配人数 {0:<3}".format(vcg_allocation[bidders[i]]), end=" ")
        # print("分配支付 {0:.5}".format(payment), end=" ")
        # print("服务成本 {0:.5}".format(bidders[i].cost[vcg_allocation[bidders[i]]]), end=" ")
        # print("支付后的效用 {0:.5}".format(payment - bidder_i_cost))
        # print("除去bidder{0}后其他人的情况".format(bidders[i].id))
        # for bidder in other_bidders:
        #     print("{0}".format(bidder), end=" ")
        #     print("分配人数 {0:<3}".format(other_allocation[bidder]), end=" ")
        #     print("服务成本 {0:.5}".format(bidder.cost[other_allocation[bidder]]))
        # print("############")
    real_bidders = bidders[1:]
    return vcg_allocation, vcg_payment, real_bidders, platform


if __name__ == '__main__':
    from vcg_reverse_auction.setting import COMMISION_RATE
    from auction_base.utility import N
    import numpy as np

    for alpha in np.arange(0.6, 1.01, 0.05):
        for reserve_price in np.arange(0.8, 1.23, 0.1):
            solutions = []
            for i in range(1, 2):
                vcg_allocation, vcg_payment, real_bidders, platform = test_alpha_reserved_price(alpha, reserve_price)
                allocation_tourist = sum([vcg_allocation[bidder] for bidder in real_bidders])
                utilities = np.array(
                    [vcg_payment[bidder] - bidder.cost[vcg_allocation[bidder]] for bidder in real_bidders if
                     vcg_allocation[bidder] != 0])
                total_utility = np.sum(utilities)
                payments = np.array([vcg_payment[bidder] for bidder in real_bidders if vcg_allocation[bidder] != 0])
                total_payment = np.sum(payments)
                commision = (reserve_price * allocation_tourist - total_payment) * COMMISION_RATE
                profit_rates = utilities / payments
                requester_payment = commision + total_payment
                solution = []
                solution.append(total_utility / total_payment)
                solution.append(np.sum(profit_rates) / len(real_bidders))
                solution.append(np.max(profit_rates))
                solution.append(np.min(profit_rates))
                solution.append(allocation_tourist / N(platform.supplies))
                solution.append(requester_payment / allocation_tourist)
                solution.append(commision / allocation_tourist)
                print("######################")
                print("alpha {0} reserve_price {1} instance {2}".format(alpha, reserve_price, i))
                print("total profit rate {0}".format(solution[0]))
                print("average profit rate {0}".format(solution[1]))
                print("max profit rate {0}".format(solution[2]))
                print("min profit rate {0}".format(solution[3]))
                print("clear rate {0}".format(solution[4]))
                print("average requesters payment {0}".format(solution[5]))
                print("average commoision {0}".format(solution[6]))
                print("######################")
                solutions.append(solution)
            solutions = np.array(solutions)
            np.save("./data/{0}_{1}".format(alpha, reserve_price), solutions)
