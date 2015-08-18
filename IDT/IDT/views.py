from django.http import HttpResponse
import gevent

hashTable = {1:1}

def idea(request):    
    e = request.GET.get('end', '')
    s = request.GET.get('start', '')
    
    try:
        start = int(s)
        end = int(e)    
        print "start: " + str(s) +" and end: "+ str(e)    
    except:
        return HttpResponse("Invalid parameters, add parameters like start=1&end=10")


    res = calMaxCount(start, end)
    return HttpResponse(res)

#need to make this using gevent
def calMaxCount(start, end):
    maxVal = 0
    for x in range(start, end+1):
        val = CC(x,hashTable)
        hashTable[x] = val
        #print hashTable
        if(val > maxVal):
            maxVal = val 
            print str(maxVal) + " corresponding to "+ str(x) 
    #print hashTable        
    return maxVal;

#calculator of CC
def CC(number,hashTable, cycle=0):    
    
    if(number==1):
        return cycle+1

    elif(number in hashTable):
        #print "## Using hashTable", number
        v = (hashTable[number])
        return cycle+v

    elif(number%2!=0):
        number = 3*number+1

    else:
        number = number/2
    
    return CC(number, hashTable, cycle+1)


def index(request):
    return HttpResponse("Welcome page! Nice to have you here.")


