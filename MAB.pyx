#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 17 20:45:35 2022

@author: zhiming
"""

import sys
import numpy as np
import matplotlib.pyplot as plt

class MAB:
    def __init__(self,K):
        # initialize the action set
       # self.actions = actions
        self.K = K
        # initialize the probabiltiy distribution
        # self.eta = np.log(K)/t
        self.t = 1
        self.meta_dis = np.ones([self.K, self.K]) / self.K
        self.L = np.zeros([self.K, self.K])
        self.p = np.ones(self.K)/self.K
        self.beta = (np.log(K)/self.t)

    def __Markov_Steady_State_Prop(self):
        Q = np.mat(self.meta_dis)
        E = np.eye(self.K)
        p = np.vstack([Q.T - E, np.ones(self.K)]).I * np.vstack([np.zeros([self.K, 1]), 1])
        self.p = np.array(p.T)[0]
        

    def draw_action(self):
        return np.random.choice(range(self.K), p=self.p)

    def update_dist(self, action, r):
        eta = (np.log(self.K) / self.t) ** 0.5
        beta = (np.log(self.K)/self.t)**0.5
        lambdat = 0.5*self.K*(np.log(self.K)/self.t)**0.5
        if lambdat >= 0.5:
            lambdat = 0.5
        self.L[:, action] += (r+beta) * (self.p / self.p[action])
        for i in range(self.K):
            self.meta_dis[i, :] = (1-lambdat)*np.exp(eta * self.L[i, :]) / np.sum(
                np.exp(eta * self.L[i, :])
            ) + lambdat / self.K
        self.__Markov_Steady_State_Prop()
        self.t += 1


if __name__ == "__main__":
    # module test program
    instance = MAB(2)
    T = 1000
    
    #generate a multivariable gaussian distribution  
    lowarm = np.random.uniform(0,0.4,[1, T])
    higharm = np.random.uniform(0.8,1,[1, T])

    rewards = np.vstack([higharm, lowarm])
    
    reward = np.zeros(T)
    time_ave_reward = np.zeros(T)
    
    reward2 = np.zeros(T)
    time_ave_reward2 = np.zeros(T)
    for t in range(T):
        # MAB selection
        action = instance.draw_action()
        r = rewards[action,t]
        instance.update_dist(action, r)
        reward[t] = r
        # random selection
        action = np.random.choice(range(2), p=[0.5,0.5])
        reward2[t] = rewards[action,t]
        
        
    cumureward = np.cumsum(reward)
    cumureward2 = np.cumsum(reward2)
    opt = max(np.sum(rewards,axis = 1)/T)
    for t in range(T):
        time_ave_reward[t] = cumureward[t]/(t+1)
        time_ave_reward2[t] = cumureward2[t]/(t+1)
    plt.plot(time_ave_reward)
    plt.plot(time_ave_reward2)
        
        
    
