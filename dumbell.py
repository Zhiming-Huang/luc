#!/usr/bin/python     
                                                                       
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from time import sleep

class SingleSwitchTopo( Topo ):
    "Single switch connected to n hosts."
    def build( self, n=4 ):
        linkopts = dict(bw=10, delay='10ms', loss = 0, max_queue_size=100)
        linkopts2 = dict(bw=10, delay='0ms', loss = 0)
        switch1 = self.addSwitch( 's1' )
        switch2 = self.addSwitch('s2')
        self.addLink(switch1, switch2, **linkopts)    
        
        # Each host gets 50%/n of system CPU
        h1 = self.addHost( 'h1',cpu=.5/n, ip='10.0.0.1')
        h2 = self.addHost( 'h2',cpu=.5/n, ip='10.0.0.2')
        self.addLink(h1, switch1, **linkopts2)
        self.addLink(h2, switch1, **linkopts2)
        h3 = self.addHost( 'h3',cpu=.5/n, ip='10.0.0.3')
        h4 = self.addHost( 'h4',cpu=.5/n, ip='10.0.0.4')
        self.addLink(h3, switch2, **linkopts2)
        self.addLink(h4, switch2, **linkopts2)

                

def perfTest():
    "Create network and run simple performance test"
    topo = SingleSwitchTopo( n=4 )
    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink)
    net.start()
    print( "Dumping host connections" )
    dumpNodeConnections( net.hosts )
    # print( "Testing network connectivity" )
    # net.pingAll()
    print( "Testing bandwidth" )
    h1, h2, h3, h4 = net.get( 'h1', 'h2', 'h3', 'h4' )
    
    h3.sendCmd('iperf3 -s -p 5000')

    h4.sendCmd('iperf3 -s -p 5001')

    sleep(3)
    
    h1.sendCmd('iperf3 -c 10.0.0.3 -p 5000 -C ccp -i 1 -t 100 -J > test_results1.json')

    h2.sendCmd('iperf3 -c 10.0.0.4 -p 5001 -C ccp -i 1 -t 100 -J > test_results2.json')
    
    sleep(120)
    
    #net.iperf( (h1, h3) )
    #h1.sendCmd('preprocessor.sh test_results1.json .')
    #h2.sendCmd('preprocessor.sh test_results2.json .')
    
    h1.terminate()
    h2.terminate()    
    h3.terminate()
    h4.terminate()
    
    
    #sleep(10)
    
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    perfTest()
