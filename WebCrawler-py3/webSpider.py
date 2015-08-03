'''
author shekhar
August 3, 2015
'''
from urllib.request import urlopen
import re

def getTags(HTMLBody):
    res = HTMLBody
    a_tags = re.findall(r'(<a [^\s]+)', res)
    links = []
    for tag in a_tags:
        if(tag.find("href")>-1 and tag.find("http")> -1):
            #print(tag)
            l = re.search(r'(https?://[^\s]+)"', tag).group(0)
            l = l[:-1]
            #print(l)
            links.append(l)
    #for link in links:
    #   print(link)
        
    return links

def navigate(url_list=[], keyword="python", limit = 10):
    counter = 0
    while(url_list != [] and counter < limit):
        counter = counter + 1
        to_visit = str(url_list[0])
        url_list = url_list[1:]
        print(counter, " Visiting : " + to_visit)
        try:
            response = urlopen(to_visit)
            if(response.status==200):
                body = str(response.read())
                if(body.find(keyword) > -1):
                    print("\t **Success","'" + str(keyword) +"'", "found on this page!")
                links = getTags(body)
            for link in links:
                url_list.append(link)
        except:
            print("\t **Error in visiting :", to_visit)
            
        
def startCrawl(url, keyword, limit):
    print("-------STARTING--------")
    if(len(keyword)==0):
        print("Invalid Keyword")
        return 
    start_url = [url]
    navigate(start_url, keyword, limit)
    print("--------THE END--------")
    

startCrawl("http://www.tutorialspoint.com/index.htm","ruby",15)
    