import re
import datetime
f=open('logtest.txt')

# definite a dictionary (dic_host): key=host/IP,value=how many times this key(host/ip) access the site
# definite a dictionary (dic_site):key=site,value= bytes  
# definite a dictionary (dic_time):key=time,value=how many times the sites was accessed during that time period
dic_period={}
lenOftop=10
for line in f.readlines()[0:]:
   
    # find start time of period and create dic_perioid{}
    def peri(period):
       df_period=re.findall(r'(\d+/\w+/\d+:\d{2}:\d{2}:\d{2})',period)[0]
       df=datetime.datetime.strptime(df_period,'%d/%b/%Y:%H:%M:%S')
       return df
    period=re.findall(r'(\d+/\w+/\d+:\d{2}:\d{2}:\d{2}\s\D\d{4})',line)[0]
    if period in dic_period:
       dic_period[period]+=1
       for key in dic_period:
           if ((peri(key)-peri(period)).seconds<=3600) or ((peri(period)-peri(key)).seconds<=3600):          
               dic_period[key]+=1             
    else:     
        for key in dic_period:
            if ((peri(key)-peri(period)).seconds<=3600) or ((peri(period)-peri(key)).seconds<=3600):          
               dic_period[key]+=1 
        dic_period[period]=1
    print period
   # print period,dic_period[period]
# definite the function(find_min) which can find the key which has the minimum value in list including 10 keys. 
def find_min(relist,dic_reg,lenOftop):
    minkey=relist[0]
    for k in range(1,lenOftop):
        if dic_reg[minkey]>dic_reg[relist[k]]:
           minkey=relist[k]
    return minkey

# definite a function to save one list(top_list) to save the top 10 (e.g.top 10 active host/IP address , top 10 resources)
def toplist(dic_reg,lenOftop):
    top_list=[]
    p=lenOftop
    for i in dic_reg:
        #print i,str(','),dic_reg[i]
        if p>0:
           top_list.append(i)
           p-=1
        else:
           minkey=find_min(top_list,dic_reg,lenOftop) 
           if int(dic_reg[i])>int(dic_reg[minkey]):
               top_list.remove(minkey)
               top_list.append(i)

    #sort the top 10 by the value
    result_topsorted={}
    max=0
    for j in range(0,lenOftop):
        result_topsorted[top_list[j]]=dic_reg[top_list[j]]
        result_list=sorted(result_topsorted.keys(),key=result_topsorted.get,reverse=True)
    return result_list


#feature 3
f3=toplist(dic_period,lenOftop)
outf3=open('hours.txt','w')
for line in f3:
    outf3.write(str(line)+","+str(dic_period[line])+'\n')

