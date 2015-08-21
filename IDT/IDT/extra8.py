import gevent
from gevent.local import local

x = 11

def myFun(val):
    global x
    print "old val of x :", x 
    x = val
    print "new val of x :", x
    print
    
    
gl = [gevent.spawn(myFun, x) for x in range(10)]
gevent.joinall(gl)