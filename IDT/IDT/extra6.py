import gevent
import urllib2
import re

def StartCrawl(url):
    response = urllib2.urlopen(url)
    #status = response.status()
    res = response.read()
    links = []
    
    a_tags = re.findall(r'(<a [^\s]+)', res)
    for tag in a_tags:
        if(tag.find("href")>-1 and tag.find("http")> -1):
            try:
                #print(tag)
                l = re.search(r'(https?://[^\s]+)"', tag).group(0)
                l = l[:-1]
                #print(l)
                links.append(l)
            except:
                try:
                    #print(tag)
                    l = re.search(r'(https?://[^\s]+)\'', tag).group(0)
                    l = l[:-1]
                    #print(l)
                    links.append(l)
                except:
                    print "exception! for " + tag
            
    return links

def gcrawl(initurl, depth = 5):
    urls = []
    urls.append(initurl)
    c = 0
    while(c < depth or urls!=[]):
        threads = []
        c = c+1
        for x in range(len(urls)):
            print str(c) + " Visiting : " + urls[x]
            threads.append(gevent.spawn(StartCrawl,urls[x]))
        urls = []
        res = gevent.joinall(threads)
        for eachgreenlet in res:
            if(type(eachgreenlet.value!=None)):
                urls = urls + eachgreenlet.value
        print urls
            
gcrawl("http://www.ndtv.com")
  
    