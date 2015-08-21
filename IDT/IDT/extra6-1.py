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
    

def justOpenUrl(url):
    for x in xrange(100,100000, 50):
        newurl = url+"?start=" + str(1)+ "&end=" + str(x)
        print newurl
        resp = urlopen(newurl)
        print "output : ", resp.read()
        print 

#openPage("https://thawing-fortress-9924.herokuapp.com/idea/cc?start=1&end=100")
#createUrl("https://thawing-fortress-9924.herokuapp.com/idea/cc", 50, 1000)
justOpenUrl("https://thawing-fortress-9924.herokuapp.com/idea/cc")