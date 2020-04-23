#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# author : zlq16
# date   : 2018/10/25

def determine_allocation_with_clear_market(bidders, platform):
    '''
        通过bidder的估值函数去决定最佳分配
        :param bidders:  投标者
        :param platform:  平台
        :param mode:    按照精确估值还是拟合估值去进行求解
        :return:
    '''
    from auction_base.utility import N
    from pyscipopt import Model, quicksum
    import numpy as np
    demand = np.sum([bidder.capacity for bidder in bidders])
    supply = N(platform.supplies)

    model = Model("max social welfare")
    x, b, c = {}, {}, {}
    supplies = platform.supplies
    goods = [good for good in supplies.index]
    I = list(range(len(bidders)))
    C = [range(bidder.capacity + 1) for bidder in bidders]
    J = list(range(len(goods)))

    # 构建决策变量
    for i in I:
        for n in C[i]:
            b[i, n] = model.addVar(name="b_{0}_{1}".format(i, n), vtype="BINARY")
            c[i, n] = bidders[i].cost[n]

    for i in I:
        for j in J:
            x[i, j] = model.addVar(name="x_{0}_{1}".format(i, j), vtype="INTEGER", lb=0, ub=supplies[goods[j]])

    # 每一个承包商可以被分配的数量不可以大于运载容积
    for i in I:
        if demand < supply: # 求不应供
            model.addCons(quicksum(x[i, j] * goods[j].union_number for j in J) == bidders[i].capacity)
        else:               # 供不应求
            model.addCons(quicksum(x[i, j] * goods[j].union_number for j in J) <= bidders[i].capacity)

    # 每一个商品配分配出去的是小于供应量
    for j in J:
        if demand < supply: # 求不应供
            model.addCons(quicksum(x[i, j] for i in I) <= supplies[goods[j]])
        else:               # 供不应求
            model.addCons(quicksum(x[i, j] for i in I) == supplies[goods[j]])


    # 每一个承包商同时只可以运载一个小于容积的人数
    for i in I:
        model.addCons(quicksum(b[i, c] for c in C[i]) == 1)

    # 每一个分配方案必须满足商品不可分割（例如三人团不可以分解成为一人团和二人团）
    for i in I:
        model.addCons(quicksum(x[i, j] * goods[j].union_number for j in J) == quicksum(b[i, n] * n for n in C[i]))

    # 设定目标
    model.setObjective(quicksum([b[i, n] * c[i, n] for i in I for n in C[i]]), "minimize")
    model.hideOutput()
    model.optimize()

    allocation = {}
    if model.getStatus() == "optimal":
        status = True
        for i in I:
            for n in C[i]:
                if int(np.round(model.getVal(b[i, n]))) == 1:
                    allocation[bidders[i]] = n
                    break
    else:
        status = False

    return status, allocation
