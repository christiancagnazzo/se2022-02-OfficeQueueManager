import re
#from decimal import Decimal
#from decimal import getcontext


def inputCheck(t_r,n_r,k_i,s_i_r):
    return True

def toHourAndMInutes(time):
    #this kind of algorithom will cause bug:because of deviation, it gives 15:49 and the current answer is 15:50
    #hour = int(time)
    #minute = int((time - hour)*60 )
    hour = int(time * 60 //60)
    minute = int(round(time * 60 % 60,0))
    return hour, minute

def timeToString(hour,minute):
    if minute<10:
        minute = "0"+str(minute)
    else:
        minute = str(minute)
    return "" + str(hour) +":" + minute

#t_r is the service time for request type r
#n_r is the number of people in queue for request type r
#k_i is the number of different types of requests served by counter i
#s_i_r is an indicator variable equal to 1 if counter i can serve request r, 0 otherwise.
def minWaitingTime(t_r,n_r,k_i,s_i_r):
    if inputCheck(t_r,n_r,k_i,s_i_r):
        sum_k = sum(map(lambda i,j:1/i*s_i_r[j] ,k_i,s_i_r))
        #print("sun_k:"+str(sum_k))
        T_r = t_r * (n_r/sum_k + 0.5)
        time = toHourAndMInutes(T_r)
        #print(time)
        return timeToString(time[0],time[1]) 
    else:
        return



if __name__ == "__main__":
    #example input  
    t_r = 5 #service time is 5 minutes
    n_r = 4 #4 people waiting for the same service,
    k_i = [2,1] # 2 service center offer 2 and 1 kind of service respectively
    s_i_r = [1,1] # all service offer this kind of service
    print(minWaitingTime(t_r,n_r,k_i,s_i_r)) 


