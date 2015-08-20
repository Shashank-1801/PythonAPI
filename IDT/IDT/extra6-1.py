from urllib2 import urlopen
import gevent
from gevent.greenlet import Greenlet



def openPage(url):
    resp = urlopen(url)
    print "output : ", resp.read()
    print "url : ", resp.url
    gevent.sleep(0)
    
def createUrl(url,start, end):
    threads = []
    for x in xrange(end, start-1, -100):
        new = url+"?start=" + str(start)+ "&end=" + str(x)
        print new
        threads.append(gevent.spawn(openPage, new))
    gevent.joinall(threads)
    

openPage("https://thawing-fortress-9924.herokuapp.com/idea/cc?start=1&end=100")
createUrl("https://thawing-fortress-9924.herokuapp.com/idea/cc", 50, 1000)