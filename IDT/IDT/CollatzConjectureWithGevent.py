import gevent
from CollatzConjecture import calMaxCount



def newFunc(x,y, name):
    gevent.sleep(3)
    print calMaxCount(x, y)
    print "End of function with name: " + str(name)

def newFunc2(x,y, name):
    print calMaxCount(x, y)
    gevent.sleep(2)
    print "End of function with name: " + str(name)

def newFunc3(x,y, name):
    print calMaxCount(x, y)
    gevent.sleep(3)
    print "End of function with name: " + str(name)



g0 = gevent.spawn(newFunc,21, 30, "g0")    
g1 = gevent.spawn(newFunc2,11, 20, "g1")
g2 = gevent.spawn(newFunc3,1, 10, "g2")

events = [g1,g2,g0]
gevent.joinall(events)