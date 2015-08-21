from urllib2 import urlopen

def justOpenUrl(url):
    for x in xrange(100000,1000000, 100000):
        newurl = url+"?start=" + str(1)+ "&end=" + str(x)
        print newurl
        resp = urlopen(newurl)
        print "output : ", resp.read()
        print 


justOpenUrl("http://localhost:8080/idea/cc")