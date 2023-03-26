import sys
import numpy as np
import MAB
import pyportus as portus



class LUCFlow:
    INIT_CWND = 10
    Initial_phase = "Initialphase"
    MAB_phase = "MABphase"
    
    def __init__(self, datapath, datapath_info):
        self.datapath = datapath
        self.datapath_info = datapath_info
        self.init_cwnd = float(self.datapath_info.mss * LUCFlow.INIT_CWND)
        self.cwnd = self.init_cwnd
        self.datapath.set_program("default", [("Cwnd", int(self.cwnd))])
        self.phase = LUCFlow.Initial_phase
        self.rttbefore = 0
        
    def on_report(self, r):
        if self.phase == LUCFlow.Initial_phase:
            if r.loss > 0:
                self.maxcwnd = self.cwnd
                #print(self.maxcwnd)
                self.cwndbase = self.cwnd / 2
                self.phase = LUCFlow.MAB_phase
                self.cwnd = max(self.cwnd, self.init_cwnd)
                self.num_actions = int((self.cwnd - self.cwndbase) / (self.datapath_info.mss*10))
                self.MAB = MAB.MAB(self.num_actions)
                #print(f"the number of actions {self.num_actions} cwndbase {self.cwndbase}")
                self.action = self.MAB.draw_action()
                self.cwnd = self.cwndbase  + (self.action + 1) * (self.datapath_info.mss * 10)
                #self.lastrtt = r.rtt
                
            else:
                self.cwnd += self.datapath_info.mss * 1.5 * (r.acked / self.cwnd)
                #self.cwnd = self.cwnd * 1.5
                #print(f"acked {r.acked} rtt {r.rtt} inflight {r.inflight} cwnd {self.cwnd}")
                self.cwnd = max(self.cwnd, self.init_cwnd)
            self.datapath.update_field("Cwnd", int(self.cwnd))
            
        else:
            #self.diffrtt = (r.rtt - self.lastrtt) / (10**6)
            #self.lastrtt = r.rtt
            #self.sndrate = r.rate
            if self.rttbefore == 0:
                self.rttbefore = r.rtt
        #print(f"the ack: {r.acked} the loss:{r.loss}")
                reward = max((self.cwnd -  r.loss)/ self.maxcwnd,0)
            else:
                rttdiff = r.rtt - self.rttbefore
                reward = max((self.cwnd - 10*self.cwnd/self.rttbefore * rttdiff - 100*self.datapath_info.mss* r.loss)/ self.maxcwnd,0)
                self.rttbefore = r.rtt
            #print(f"the action: {self.action} the rtt diff: {self.diffrtt} the reward:{reward} rate:{self.sndrate}")
            self.MAB.update_dist(self.action, reward)
            self.action = self.MAB.draw_action()
            self.cwnd = self.cwndbase  + (self.action + 1) * (self.datapath_info.mss*10)
            #print(f"the action: {self.action} the reward:{reward} the t {self.MAB.t} the cwnd: {self.cwnd} the probability {self.MAB.p}")
            
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
                    (volatile rate 0)
                ))
                (when true
                    (:= Report.inflight Flow.packets_in_flight)
                    (:= Report.rtt Flow.rtt_sample_us)
                    (:= Report.acked (+ Report.acked Ack.bytes_acked))
                    (:= Report.sacked (+ Report.sacked Ack.packets_misordered))
                    (:= Report.loss Ack.lost_pkts_sample)
                    (:= Report.timeout Flow.was_timeout)
                    (:= Report.rate Flow.rate_outgoing)
                    (fallthrough)
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
