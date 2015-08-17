from django.http import HttpResponse
import gevent



def index(request):
    return HttpResponse("Welcome page! Nice to have you here.")

def idea(st=0,en=10):
    #s = request.GET.get('start', '')
    #e = request.GET.get('end', '')
    try:
        start = int(st)
        end = int(en)
        return HttpResponse(calMaxCount(start, end))
    except:
        return HttpResponse("Invalid parameters, add start=1&end=10")
    
    

#need to make this using gevent
def calMaxCount(start, end):
    maxVal = 0
    for x in range(start, end):
        val = CC(x)
        if(val > maxVal):
            maxVal = val 
            print str(maxVal) + " corresponding to "+ str(x) 
            
    return maxVal;

#calculator of CC
def CC(number, cycle=0):
    if(number==1):
        return cycle+1
    elif(number%2!=0):
        number = 3*number+1
    else:
        number = number/2
    
    return CC(number, cycle+1)


idea()