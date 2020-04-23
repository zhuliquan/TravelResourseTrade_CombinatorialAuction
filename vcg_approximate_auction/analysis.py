#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# author : zlq16
# date   : 2018/10/25


def analysis_clear_market_pk_optmal():
    from vcg_approximate_auction.setting import PRICE_GET_TOURIST
    from auction_base.setting import ALPHA, GOODS, TOURIST_UNION
    from auction_base.setting import BIDDER_NUMBER, MIN_D, MAX_D, SERVER_FEE, CAPACITIES, V_E
    from vcg_approximate_auction.utility import generate_environment
    from vcg_approximate_auction.utility import compute_social_welfare
    from vcg_approximate_auction.auction import determine_allocation_with_optimal
    from vcg_approximate_auction.auction import determine_allocation_with_clear_market
    import numpy as np

    simulation = 20
    for a in np.arange(0.4, 1.05, 0.1):
        a_e = 0.0
        for i in range(simulation):
            print("in {0} simulation".format(i))
            bidders, platform = generate_environment(
                a, PRICE_GET_TOURIST, GOODS, TOURIST_UNION,
                BIDDER_NUMBER, MIN_D, MAX_D, SERVER_FEE, CAPACITIES, V_E)
            _, allocation = determine_allocation_with_clear_market(bidders, platform, "real")
            e1 = compute_social_welfare(bidders, allocation, "real")
            _, allocation = determine_allocation_with_optimal(bidders, platform, "real")
            e2 = compute_social_welfare(bidders, allocation, "real")
            a_e += (e1 / e2)
        print(a_e / 20)

    bidders, platform = generate_environment(
        ALPHA, PRICE_GET_TOURIST, GOODS, TOURIST_UNION,
        BIDDER_NUMBER, MIN_D, MAX_D, SERVER_FEE, CAPACITIES, V_E)
    _, allocation = determine_allocation_with_clear_market(bidders, platform, "real")
    e1 = compute_social_welfare(bidders, allocation, "real")
    _, allocation = determine_allocation_with_optimal(bidders, platform, "real")


def analysis_fit_value():
    from vcg_approximate_auction.setting import PRICE_GET_TOURIST
    from auction_base.setting import ALPHA, GOODS, TOURIST_UNION
    from auction_base.setting import BIDDER_NUMBER, MIN_D, MAX_D, SERVER_FEE, CAPACITIES, V_E
    from vcg_approximate_auction.utility import generate_environment

    #### test market generate ####
    import matplotlib.pyplot as plt
    from vcg_approximate_auction.utility import fit_all_approximate_values
    from vcg_approximate_auction.utility import print_env

    bidders, platform = generate_environment(ALPHA, PRICE_GET_TOURIST, GOODS, TOURIST_UNION,
                                             BIDDER_NUMBER, MIN_D, MAX_D, SERVER_FEE, CAPACITIES, V_E)
    print("#### generate market ####")
    print_env(bidders, platform)
    fit_all_approximate_values(bidders, mode="affine")
    print("#### fit all values #####")
    # for bidder in bidders:
    #     plt.figure()
    #     x = list(range(bidder.capacity+1))
    #     y1 = list([bidder.approximate_value(c) for c in x])
    #     y2 = ([bidder.real_value(c) for c in x])
    #     plt.grid('on')
    #     plt.plot(x[1:], y1[1:], 'r-')
    #     plt.plot(x[1:], y2[1:], 'b-')
    #     plt.plot(x[1:], [0]*(len(x)-1), 'k-')
    #     plt.title("bidder {0}".format(bidder.id))
    #     plt.xlabel('tourist number')
    #     plt.ylabel('value')
    #     plt.legend(["real valuation", "approximate valuation"])
    #     plt.show()

    from vcg_approximate_auction.auction import determine_allocation_with_optimal
    from vcg_approximate_auction.utility import compute_social_welfare
    _, approximte_vcg_allocation = determine_allocation_with_optimal(bidders, platform, "approximate")
    _, real_vcg_allocation = determine_allocation_with_optimal(bidders, platform, "real")
    print("approximate")
    for bidder in bidders:
        print(bidder, approximte_vcg_allocation[bidder])
    print("approximate social welfare {0}".format(compute_social_welfare(bidders, approximte_vcg_allocation, "real")))

    print("real")
    for bidder in bidders:
        print(bidder, real_vcg_allocation[bidder])

    print("real social welfare {0}".format(compute_social_welfare(bidders, real_vcg_allocation, "real")))


def analysis_lost():
    from vcg_approximate_auction.setting import PRICE_GET_TOURIST
    from auction_base.setting import ALPHA, GOODS, TOURIST_UNION
    from auction_base.setting import BIDDER_NUMBER, MIN_D, MAX_D, SERVER_FEE, CAPACITIES, V_E
    from vcg_approximate_auction.utility import generate_environment

    #### test market generate ####
    from vcg_approximate_auction.auction import determine_allocation_with_clear_market
    from vcg_approximate_auction.auction import determine_allocation_with_optimal
    from vcg_approximate_auction.utility import print_env
    from vcg_approximate_auction.utility import compute_social_welfare

    bidders, platform = generate_environment(ALPHA, PRICE_GET_TOURIST, GOODS, TOURIST_UNION,
                                             BIDDER_NUMBER, MIN_D, MAX_D, SERVER_FEE, CAPACITIES, V_E)
    print("#### generate market ####")
    print_env(bidders, platform)

    mode = "real"
    print("in clear market situation")
    status, vcg_allocation = determine_allocation_with_clear_market(bidders, platform, mode)
    vcg_social_welfare = compute_social_welfare(bidders, vcg_allocation, mode)
    I = list(range(len(bidders)))
    payment = {}
    for i in I:
        print("calculate bidder {0} payment".format(bidders[i].id))
        other_bidders = [bidders[j] for j in I if j != i]
        s, allocation = determine_allocation_with_clear_market(other_bidders, platform, mode)
        other_social_welfare = compute_social_welfare(other_bidders, allocation, mode)
        if mode == "approximate":
            remove_i_social_welfare = vcg_social_welfare - bidders[i].approximate_value(vcg_allocation[bidders[i]])
        elif mode == "misreported":
            remove_i_social_welfare = vcg_social_welfare - bidders[i].misreported_value(vcg_allocation[bidders[i]])
        elif mode == "real":
            remove_i_social_welfare = vcg_social_welfare - bidders[i].real_value(vcg_allocation[bidders[i]])

        print("other_social_cost {0}".format(other_social_welfare))
        print("bidder {0} {1}".format(bidders[i].id, bidders[i].real_value(vcg_allocation[bidders[i]])))
        print("remove_i_social_welfare {0}".format(remove_i_social_welfare))
        payment[bidders[i]] = other_social_welfare - remove_i_social_welfare

    for bidder in bidders:
        print(bidder, end=" ")
        print("vcg_allocation: {0} ".format(vcg_allocation[bidder]), end=" ")
        print("payment: {0} ".format(payment[bidder]), end=" ")
        print("utility: {0}".format(bidder.real_value(vcg_allocation[bidder]) - payment[bidder]))
    print("total social welfare {0}".format(compute_social_welfare(bidders, vcg_allocation, "real")))

    # mode = "misreported"
    # print("in misreported situation")
    # status, vcg_allocation = determine_allocation_with_clear_market(bidders, platform, mode)
    # vcg_social_cost = compute_social_cost(bidders, vcg_allocation, mode)
    # I = list(range(len(bidders)))
    # payment = {}
    # for i in I:
    #     print("calculate bidder {0} payment".format(bidders[i].id))
    #     other_bidders = [bidders[j] for j in I if j != i]
    #     s, vcg_allocation = determine_allocation_with_clear_market(other_bidders, platform, mode)
    #     other_social_cost = compute_social_cost(other_bidders, vcg_allocation, mode)
    #     if mode == "approximate":
    #         remove_i_social_welfare = vcg_social_cost - bidders[i].approximate_value(vcg_allocation[bidders[i]])
    #     elif mode == "misreported":
    #         remove_i_social_welfare = vcg_social_cost - bidders[i].misreported_value(vcg_allocation[bidders[i]])
    #     elif mode == "real":
    #         remove_i_social_welfare = vcg_social_cost - bidders[i].real_value(vcg_allocation[bidders[i]])
    #
    #     print("other_social_cost {0}".format(other_social_cost))
    #     print("bidder {0}".format(bidders[i].real_value(vcg_allocation[bidders[i]])))
    #     print("remove_i_social_welfare {0}".format(remove_i_social_welfare))
    #     payment[bidders[i]] = other_social_cost - remove_i_social_welfare
    #
    # for bidder in bidders:
    #     print(bidder, end=" ")
    #     print("vcg_allocation: {0} ".format(vcg_allocation[bidder]), end=" ")
    #     print("payment: {0} ".format(payment[bidder]), end=" ")
    #     print("utility: {0}".format(bidder.real_value(vcg_allocation[bidder]) - payment[bidder]))
    # print("total social welfare {0}".format(compute_social_cost(bidders, vcg_allocation, "real")))


def analysis_payment():
    from vcg_approximate_auction.setting import PRICE_GET_TOURIST
    from auction_base.setting import ALPHA, GOODS, TOURIST_UNION
    from auction_base.setting import BIDDER_NUMBER, MIN_D, MAX_D, SERVER_FEE, CAPACITIES, V_E
    from vcg_approximate_auction.utility import generate_environment

    #### test market generate ####
    from vcg_approximate_auction.auction import determine_allocation_with_clear_market
    from vcg_approximate_auction.auction import determine_allocation_with_optimal
    from vcg_approximate_auction.utility import print_env
    from vcg_approximate_auction.utility import compute_social_welfare

    bidders, platform = generate_environment(ALPHA, PRICE_GET_TOURIST, GOODS, TOURIST_UNION,
                                             BIDDER_NUMBER, MIN_D, MAX_D, SERVER_FEE, CAPACITIES, V_E)
    print("#### generate market ####")
    print_env(bidders, platform)

    mode = "real"
    print("in clear market situation")
    status, vcg_allocation = determine_allocation_with_clear_market(bidders, platform, mode)
    vcg_social_welfare = compute_social_welfare(bidders, vcg_allocation, mode)
    I = list(range(len(bidders)))
    payment = {}
    for i in I:
        print("calculate bidder {0} payment".format(bidders[i].id))
        other_bidders = [bidders[j] for j in I if j != i]
        s, allocation = determine_allocation_with_clear_market(other_bidders, platform, mode)
        other_social_welfare = compute_social_welfare(other_bidders, allocation, mode)
        if mode == "approximate":
            remove_i_social_welfare = vcg_social_welfare - bidders[i].approximate_value(vcg_allocation[bidders[i]])
        elif mode == "misreported":
            remove_i_social_welfare = vcg_social_welfare - bidders[i].misreported_value(vcg_allocation[bidders[i]])
        elif mode == "real":
            remove_i_social_welfare = vcg_social_welfare - bidders[i].real_value(vcg_allocation[bidders[i]])

        print("other_social_cost {0}".format(other_social_welfare))
        print("bidder {0}".format(bidders[i].real_value(vcg_allocation[bidders[i]])))
        print("remove_i_social_welfare {0}".format(remove_i_social_welfare))
        payment[bidders[i]] = other_social_welfare - remove_i_social_welfare

    for bidder in bidders:
        print(bidder, end=" ")
        print("vcg_allocation: {0} ".format(vcg_allocation[bidder]), end=" ")
        print("payment: {0} ".format(payment[bidder]), end=" ")
        print("utility: {0}".format(bidder.real_value(vcg_allocation[bidder]) - payment[bidder]))
    print("total social welfare {0}".format(compute_social_welfare(bidders, vcg_allocation, "real")))

    ###############################
    print("in optimal situation")
    mode = "real"
    status, vcg_allocation = determine_allocation_with_optimal(bidders, platform, mode)
    vcg_social_welfare = compute_social_welfare(bidders, vcg_allocation, mode)
    I = list(range(len(bidders)))
    payment = {}
    for i in I:
        print("calculate bidder {0} payment".format(bidders[i].id))
        other_bidders = [bidders[j] for j in I if j != i]
        s, allocation = determine_allocation_with_optimal(other_bidders, platform, mode)
        other_social_welfare = compute_social_welfare(other_bidders, allocation, mode)
        if mode == "approximate":
            remove_i_social_welfare = vcg_social_welfare - bidders[i].approximate_value(vcg_allocation[bidders[i]])
        elif mode == "misreported":
            remove_i_social_welfare = vcg_social_welfare - bidders[i].misreported_value(vcg_allocation[bidders[i]])
        elif mode == "real":
            remove_i_social_welfare = vcg_social_welfare - bidders[i].real_value(vcg_allocation[bidders[i]])

        print("other_social_cost {0}".format(other_social_welfare))
        print("bidder {0}".format(bidders[i].real_value(vcg_allocation[bidders[i]])))
        print("remove_i_social_welfare {0}".format(remove_i_social_welfare))
        payment[bidders[i]] = other_social_welfare - remove_i_social_welfare

    for bidder in bidders:
        print(bidder, end=" ")
        print("vcg_allocation: {0} ".format(vcg_allocation[bidder]), end=" ")
        print("payment: {0} ".format(payment[bidder]), end=" ")
        print("utility: {0}".format(bidder.real_value(vcg_allocation[bidder]) - payment[bidder]))
    print("total social welfare {0}".format(compute_social_welfare(bidders, vcg_allocation, "real")))


def analysis_allocation_efficiency():
    from vcg_approximate_auction.setting import PRICE_GET_TOURIST
    from auction_base.setting import GOODS, TOURIST_UNION
    from auction_base.setting import BIDDER_NUMBER, MIN_D, MAX_D, SERVER_FEE, CAPACITIES, V_E
    from vcg_approximate_auction.utility import generate_environment
    from vcg_approximate_auction.auction import determine_allocation_with_optimal
    from vcg_approximate_auction.auction import determine_allocation_with_clear_market
    from vcg_approximate_auction.utility import compute_social_welfare
    from vcg_approximate_auction.utility import fit_all_approximate_values

    ## test vcg_allocation ####
    import numpy as np
    for a in np.arange(0.5, 1.05, 0.1):
        a_e = 0
        print("alpha is {0}".format(a))
        for i in range(1):
            print("in {0} simulation".format(i))
            bidders, platform = generate_environment(a, PRICE_GET_TOURIST, GOODS, TOURIST_UNION,
                                                     BIDDER_NUMBER, MIN_D, MAX_D, SERVER_FEE, CAPACITIES, V_E)

            fit_all_approximate_values(bidders, mode="affine")
            mode = "approximate"
            status, allocation = determine_allocation_with_clear_market(bidders, platform, mode)
            if status:
                for bidder in bidders:
                    c = allocation[bidder]
                sw1 = compute_social_welfare(bidders, allocation, "real")
                print("approximate value optimal social welfare: {0}".format(sw1))
            else:
                print("don't find optimal vcg_allocation")

            mode = "real"
            status, allocation = determine_allocation_with_clear_market(bidders, platform, mode)
            if status:
                for bidder in bidders:
                    c = allocation[bidder]
                sw2 = compute_social_welfare(bidders, allocation, "real")
                print("real value optimal social welfare: {0}".format(sw2))
            else:
                print("don't find optimal vcg_allocation")

            e = sw1 / sw2
            a_e += e
        print("average e: {0}".format(a_e / 1))


if __name__ == '__main__':
    analysis_payment()
