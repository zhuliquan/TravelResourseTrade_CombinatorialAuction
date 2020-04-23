#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# author : zlq16
# date   : 2018/9/5


def determine_allocation_with_clear_market(bidders, platform, mode):
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

    if demand < supply:
        flag = True  # 求不应供
    else:
        flag = False  # 供不应求

    model = Model("max social welfare")
    x, b, v = {}, {}, {}
    supplies = platform.supplies
    goods = [good for good in supplies.index]
    I = list(range(len(bidders)))
    C = [range(bidder.capacity + 1) for bidder in bidders]
    J = list(range(len(goods)))
    # 构建决策变量
    for i in I:
        for c in C[i]:
            b[i, c] = model.addVar(name="b_{0}_{1}".format(i, c), vtype="BINARY")
            if mode == "approximate":
                v[i, c] = bidders[i].approximate_value(c)
            elif mode == "misreported":
                v[i, c] = bidders[i].misreported_value(c)
            elif mode == "real":
                v[i, c] = bidders[i].real_value(c)

    for i in I:
        for j in J:
            x[i, j] = model.addVar(name="x_{0}_{1}".format(i, j), vtype="INTEGER", lb=0, ub=supplies[goods[j]])

    # 每一个承包商可以被分配的数量不可以大于运载容积
    for i in I:
        model.addCons(quicksum(x[i, j] * goods[j].union_number for j in J) <= bidders[i].capacity)

    # 每一个商品配分配出去的是小于供应量
    for j in J:
        if flag:  # 求不应供
            model.addCons(quicksum(x[i, j] for i in I) <= supplies[goods[j]])
        else:  # 供不应求
            model.addCons(quicksum(x[i, j] for i in I) == supplies[goods[j]])

    # 每一个承包商同时只可以运载一个小于容积的人数
    for i in I:
        model.addCons(quicksum(b[i, c] for c in C[i]) == 1)

    # 每一个分配方案必须满足商品不可分割（例如三人团不可以分解成为一人团和二人团）
    for i in I:
        model.addCons(quicksum(x[i, j] * goods[j].union_number for j in J) == quicksum(b[i, c] * c for c in C[i]))

    # 设定目标
    model.setObjective(quicksum([b[i, c] * v[i, c] for i in I for c in C[i]]), "maximize")
    model.hideOutput()
    model.optimize()

    allocation = {}
    if model.getStatus() == "optimal":
        status = True
        for i in I:
            for c in C[i]:
                if int(np.round(model.getVal(b[i, c]))) == 1:
                    allocation[bidders[i]] = c
                    break
    else:
        status = False

    return status, allocation


def determine_allocation_with_optimal(bidders, platform, mode):
    '''
        通过bidder的估值函数去决定最佳分配
        :param bidders: 投标者
        :param platform:  卖家
        :param mode:    按照精确估值还是拟合估值去进行求解
        :return:
        '''
    from pyscipopt import Model, quicksum
    import numpy as np

    model = Model("max social welfare")
    x, b, v = {}, {}, {}
    supplies = platform.supplies
    goods = [good for good in supplies.index]
    I = list(range(len(bidders)))
    C = [list(range(bidder.capacity + 1)) for bidder in bidders]
    J = list(range(len(goods)))

    # 构建决策变量
    for i in I:
        for c in C[i]:
            b[i, c] = model.addVar(name="b_{0}_{1}".format(i, c), vtype="BINARY")
            if mode == "approximate":
                v[i, c] = bidders[i].approximate_value(c)
            elif mode == "misreported":
                v[i, c] = bidders[i].misreported_value(c)
            elif mode == "real":
                v[i, c] = bidders[i].real_value(c)

    for i in I:
        for j in J:
            x[i, j] = model.addVar(name="x_{0}_{1}".format(i, j), vtype="INTEGER", lb=0, ub=supplies[goods[j]])

    # 每一个承包商可以被分配的数量不可以大于运载容积
    for i in I:
        model.addCons(quicksum(x[i, j] * goods[j].union_number for j in J) <= bidders[i].capacity)

    # 每一个商品配分配出去的是小于供应量
    for j in J:
        model.addCons(quicksum(x[i, j] for i in I) <= supplies[goods[j]])

    # 每一个承包商同时只可以运载一个小于容积的人数
    for i in I:
        model.addCons(quicksum(b[i, c] for c in C[i]) == 1)

    # 每一个分配方案必须满足商品不可分割（例如三人团不可以分解成为一人团和二人团）
    for i in I:
        model.addCons(quicksum(x[i, j] * goods[j].union_number for j in J) == quicksum(b[i, c] * c for c in C[i]))

    # 设定目标
    model.setObjective(quicksum([b[i, c] * v[i, c] for i in I for c in C[i]]), "maximize")
    model.hideOutput()
    model.optimize()

    # 记录结果
    allocation = {}
    if model.getStatus() == "optimal":
        status = True
        for i in I:
            for c in C[i]:
                if int(np.round(model.getVal(b[i, c]))) == 1:
                    allocation[bidders[i]] = c
                    break
    else:
        status = False

    return status, allocation
