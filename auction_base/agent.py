#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# author : zlq16
# date   : 2018/3/15
import numpy as np
import pandas as pd

class BasePlatform(object):

    def __init__(self,id, quantity):
        self.id = id
        self.supplies = quantity

    def __str__(self):
        return "供应量是:\n{0}".format(self.supplies)

    def __hash__(self):
        return hash(str(self.id))

class BaseBidder(object):

    def __init__(self, id, D, unit_server_cost, capacity, v_f):
        self.id = id
        self.D = D
        self.capacity = capacity  # 表示容积限制
        self.unit_server_cost = unit_server_cost
        self.total_solid_cost = v_f(capacity)
        self.cost = np.array(list(map(self.cost_utility, range(0, capacity + 1))))
        self.margin_cost = self.cost[1:-1] - self.cost[0:-2]

    def cost_utility(self, n):
        P_s = self.unit_server_cost
        if 0 < n <= self.capacity:
            return P_s*n*np.power(self.D,-n/self.capacity) + self.total_solid_cost
        else:
            return 0

    def __str__(self):
        return "id:{0:2},运载量是:{1:3}".format(self.id, self.capacity)

    def __hash__(self):
        return hash(str(id))

    def __eq__(self, other):
        return self.id == other.id
