import gevent
from CollatzConjecture import calMaxCount
from random import randint



def newFunc(x,y, name):
    t = randint(0,5)*0.2
    print name + "is sleeping for " + str(t)
    gevent.sleep(t)
    print calMaxCount(x, y)
    print "End of function with name: " + str(name)


g0 = gevent.spawn(newFunc,21, 30, "g0")    
g1 = gevent.spawn(newFunc,11, 20, "g1")
g2 = gevent.spawn(newFunc,1, 1000000, "g2")

events = [g1,g2,g0]
gevent.joinall(events)