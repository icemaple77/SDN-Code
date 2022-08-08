#!/usr/bin/env python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info

def myNetwork():

    net = Mininet( topo=None,build=False, ipBase='10.0.0.0/8', controller=Controller)

    info( '*** Adding controller\n' ) # this is where we can edit our controller and add them to the existing mininet
    c0=net.addController('c0')
    
    hosts=[]
    n = 2000 #number of hosts
    for h in range(n):
     hosts.append('h%s' % (h+1))
    
    switcheslayer1=[]
    switcheslayer2=[]
    i= 200 #number of switches in layer 1
    c= 0 #switch count
    x = 0 #switch layer 2
    for s in range(i):
     switcheslayer1.append('s%d' % (s+1))
     c += 1
     if (c == 10): # the incriment
      switcheslayer2.append('ss%d' % (x+1))
      x += 1
      c = 0
      
    info( '*** Add hosts\n')
    for h in hosts:
     globals() [h] = net.addHost(h)
     info(h + " ")
    info('\n')

    info( '*** Add switches\n')
    for s in switcheslayer1:
     globals() [s] = net.addSwitch(s, cls=OVSSwitch)
     info(s + " ")
    info('\n')
    for s in switcheslayer2:
     globals() [s] = net.addSwitch(s, cls=OVSSwitch)
     info(s + " ")
    info('\n')

    info( '*** Add links\n')
    i=n=0
    for h in hosts:
     net.addLink(h,switcheslayer1[i])
     info("(" + h + "," + switcheslayer1[i] + ") ")
     n += 1
     if (n == 10): #the amount of split of each switch can be done here n== 10 means use another swicth after the prev one has linked to 10 hosts
      i += 1
      n=0
    info('\n')

    info( '*** Add links beetwen the switches\n') #links between switches can be edited here
    i=n=0
    for s in switcheslayer1:
     net.addLink(s,switcheslayer2[i])
     info("(" + s + "," + switcheslayer2[i] + ") ")
     n += 1
     if (n == 10): #the amount of split of each switch can be done here n== 10 means use another swicth after the prev one has linked to 10 hosts
      i += 1
      n=0
    info('\n') 
    
    c=0
    for i in switcheslayer2:
     if ((c+1) < len(switcheslayer2)):
      net.addLink(i, switcheslayer2[c+1])
      c += 1 
    
    
    info( '*** Starting network\n')
    net.start()
    
    info( '*** Enable Spinning Tree\n') #need to be asked not sure myself
    for s in switcheslayer1:
     globals() [s].cmd('ovs-vsctl set bridge %s stp-enable=true' % (s))
    for s in switcheslayer2:
     globals() [s].cmd('ovs-vsctl set bridge %s stp-enable=true' % (s))
    
    info( '*** Post configure switches and hosts\n')
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()
