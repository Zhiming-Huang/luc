#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 17 20:45:35 2022

@author: zhiming
"""

import sys
import numpy as np
import pyportus as portus


class MAB:
    def __init__(self, actions):
        # initialize the action set
        self.actions = actions
        self.K = len(actions)
        # initialize the probabiltiy distribution
        # self.eta = np.log(K)/t
        self.t = 1
        self.meta_dis = np.ones([self.K, self.K]) / self.K
        self.L = np.zeros([self.K, self.K])

    def __Markov_Steady_State_Prop(self):
        Q = np.mat(self.meta_dis)
        E = np.eye(self.K)
        p = np.vstack([Q.T - E, np.ones(self.K)]).I * np.vstack([np.zeros([self.K, 1]), 1])
        self.p = np.array(p.T)
        

    def draw_action(self):
        self.__Markov_Steady_State_Prop()
        return np.random.choice(self.actions, p=self.p[0])

    def update_dist(self, action, r):
        action_id = self.actions.index(action)
        eta = (np.log(self.K) / self.t) ** 0.5
        self.L[:, action_id] += (1 - r) * self.p / self.p[action_id]
        for i in range(self.K):
            self.meta_dis[i, :] = np.exp(-eta * self.L[i, :]) / np.sum(
                np.exp(-eta * self.L[i, :])
            )


if __name__ == "__main__":
    instance = MAB([1, 2, 3, 4])
    action = instance.draw_action()
