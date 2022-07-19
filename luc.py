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
        self.p = (
            np.vstack([Q.T - E, np.ones(self.K)]).I
            * np.vstack([np.zeros([self.K, 1]), 1])
        ).I

    def draw_action(self):
        self.__Markov_Steady_State_Prop()
        self.p[0]
        return np.random.choice(self.actions, p=self.p[0])

    def update_dist(self, action, r):
        action_id = self.actions.index(action)
        eta = (np.log(self.K) / self.t) ** 0.5
        self.L[:, action_id] += (1 - r) * self.p / self.p[action_id]
        for i in range(self.K):
            self.meta_dis[i, :] = np.exp(-eta * self.L[i, :]) / np.sum(
                np.exp(-eta * self.L[i, :])
            )


class LUCFlow:
    INIT_CWND = 10

    def __init__(self, datapath, datapath_info):
        self.datapath = datapath
        self.datapath_info = datapath_info
        self.init_cwnd = float(self.datapath_info.mss * LUCFlow.INIT_CWND)
        self.cwnd = self.init_cwnd
        self.datapath.set_program("default", [("Cwnd", int(self.cwnd))])

    def on_report(self, r):
        if r.loss > 0 or r.sacked > 0:
            self.cwnd /= 2
        else:
            self.cwnd += self.datapath_info.mss * (r.acked / self.cwnd)

        print(f"acked {r.acked} rtt {r.rtt} inflight {r.inflight}")
        self.cwnd = max(self.cwnd, self.init_cwnd)
        self.datapath.update_field("Cwnd", int(self.cwnd))


class LUC(portus.AlgBase):
    def datapath_programs(self):
        return {
            "default": """\
                (def (Report
                    (volatile acked 0)
                    (volatile sacked 0)
                    (volatile loss 0)
                    (volatile timeout false)
                    (volatile rtt 0)
                    (volatile inflight 0)
                ))
                (when true
                    (:= Report.inflight Flow.packets_in_flight)
                    (:= Report.rtt Flow.rtt_sample_us)
                    (:= Report.acked (+ Report.acked Ack.bytes_acked))
                    (:= Report.sacked (+ Report.sacked Ack.packets_misordered))
                    (:= Report.loss Ack.lost_pkts_sample)
                    (:= Report.timeout Flow.was_timeout)
                    (fallthrough)
                )
                (when (|| Report.timeout (> Report.loss 0))
                    (report)
                    (:= Micros 0)
                )
                (when (> Micros Flow.rtt_sample_us)
                    (report)
                    (:= Micros 0)
                )
            """
        }

    def new_flow(self, datapath, datapath_info):
        return LUCFlow(datapath, datapath_info)


alg = LUC()

portus.start("netlink", alg)
