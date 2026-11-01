#!/usr/bin/env python3

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel


class RemoteMonitoringTopo(Topo):
    def build(self):
        h1 = self.addHost('h1', ip='10.0.0.1/24')
        h2 = self.addHost('h2', ip='10.0.0.2/24')
        s1 = self.addSwitch('s1', protocols='OpenFlow10')
        self.addLink(h1, s1)
        self.addLink(h2, s1)


def run():
    topo = RemoteMonitoringTopo()
    net = Mininet(topo=topo, controller=None, switch=OVSSwitch)
    net.addController(
        'c0',
        controller=RemoteController,
        ip='127.0.0.1',
        port=6633
    )
    net.start()
    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    run()
