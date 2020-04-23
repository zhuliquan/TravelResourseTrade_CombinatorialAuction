#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# author : zlq16
# date   : 2018/9/4
import numpy as np
from scipy import optimize
from numpy.polynomial import Polynomial
from auction_base.agent import BaseBidder, BasePlatform
from vcg_approximate_auction.utility import affine_func, quadro_func, triple_func


class Platform(BasePlatform):

    def __init__(self, quantity):
        super(Platform, self).__init__(0, quantity)


class Bidder(BaseBidder):
    price_get_tourist = 0

    def __init__(self, id, D, unit_server_cost, capacity, v_f, price_get_tourist):
        super(Bidder, self).__init__(id, D, unit_server_cost, capacity, v_f)
        Bidder.price_get_tourist = price_get_tourist
        self._approximate_value = None

    def misreported_value(self, n):
        if self.id == 0:
            if self.real_value(n) > 0:
                return self.real_value(n) + 100
            return self.real_value(n)
        else:
            return self.real_value(n)

    def approximate_value(self, n):
        if self._approximate_value != None:
            if n > 0:
                return self._approximate_value(n)
            else:
                return 0
        else:
            raise Exception("你需要先进行拟合才可以进行近似估值的提取")

    def real_value(self, n):
        return Bidder.price_get_tourist * n - self.cost[n]

    def fit_approximate_value(self, mode):
        '''
        进行函数拟合
        goal:
            min(sum((v(x) - ax - b)^2))
        :param mode: 拟合形式 affine/quadro
        :return:
        '''
        if self._approximate_value == None:
            x0 = np.array(list(range(1, self.capacity + 1)))
            y0 = np.array(list(map(self.real_value, x0)))
            if mode == "affine":
                coef = optimize.curve_fit(affine_func, x0, y0)[0]
            elif mode == "quadro":
                coef = optimize.curve_fit(quadro_func, x0, y0)[0]
            elif mode == "triple":
                coef = optimize.curve_fit(triple_func, x0, y0)[0]
            else:
                coef = [0]
            self._approximate_value = Polynomial(coef[::-1])
        return self._approximate_value
