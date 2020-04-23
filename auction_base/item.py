#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# author : zlq16
# date   : 2018/10/9
class Item(object):
    def __init__(self, tourist_destination, union_number):
        self.tourist_destination = tourist_destination
        self.union_number = union_number
        self.id = union_number

    def __str__(self):
        return "({0},{1})".format(self.tourist_destination, self.union_number)

    def __hash__(self):
        return hash(self.__str__())
