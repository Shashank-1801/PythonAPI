"""
3n+1 problem (Collatz conjecture)

Collatz conjecture states that for any number n, the below function f(n) will always boil down to 1, if you apply the same function over and over again to the previous result.

f(n) = {   
3n+1, if n is odd,  
n/2, if n is even  
1, if n is 1  
}  

Eg: if n = 20, then:  
f(20) = 20/2 = 10  
f(10) = 10/2 = 5  
f(5)  = 3*5+1 = 16  
f(16) = 16/2 = 8  
f(8)  = 8/2 = 4  
f(4)  = 4/2 = 2  
f(2)  = 1  

The term cycle count refers to the length of the sequence of numbers generated. In the above case, cycle count for f(20) is 8.  

The problem is as follows:  
Given a range of inputs (like 1-100), calculate the maximum cycle count that is encountered. As you can imagine, there is a lot of computation that is involved, for each number in the range. So optimise your logic with every method, you can think of.  

Your expected input range should be: 1 - 1million.  

Please use gevent (http://www.gevent.org/) [Github: https://github.com/surfly/gevent] to write a python server application that solves the 3n+1 problem.   

Use your learnings from above to create the python application. Optimize it and make it responsive. It should be able to handle multiple requests concurrently.  
Submit your python code to us by email.  

If you have any questions/doubts, please feel free to reach out.

Ritesh
"""

def CC(number, cycle=0):
    if(number==1):
        return cycle+1
    elif(number%2!=0):
        number = 3*number+1
    else:
        number = number/2
    
    return CC(number, cycle+1)

def calMaxCount(start, end):
    maxVal = 0
    for x in range(start, end):
        val = CC(x)
        if(val > maxVal):
            maxVal = val 
            print str(maxVal) + " corresponding to "+ str(x) 
            
    return maxVal;


#driver program:    
print CC(20)
p = calMaxCount(1, 100)
print "Max value is : " + str(p)








    