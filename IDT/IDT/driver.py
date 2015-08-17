from urllib import urlopen
import gevent


def open(url):
    resp = urlopen(url)
    print resp.read()
    
    
def appendParameter(baseUrl):
    threads = []
    for x in xrange(1, 1000000):
        new_url = baseUrl+"?start=1&end="+str(x) 
        threads.append(gevent.spawn(open,new_url))
    gevent.joinall(threads)
        
appendParameter("https://thawing-fortress-9924.herokuapp.com/idea/cc")
#open("https://thawing-fortress-9924.herokuapp.com/idea/cc?start=1&end=100")