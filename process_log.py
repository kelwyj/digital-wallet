import re
import datetime
f=open('log.txt')

#definite functions
def getId(line):
    host=line.split(" ")[0]
    site=str(re.findall(r" [ /](.+?) HTTP",line)).replace("'","")
    site='/'+site.replace("[","").replace("]","")
    code=int(line.split(" ")[-2])
    Time1=re.findall(r'(\d+/\w+/\d+:\d{2}:\d{2}:\d{2})',line)[0]
    Time=datetime.datetime.strptime(Time1,'%d/%b/%Y:%H:%M:%S')
    return(host,site,code,Time)

# definite the function(find_min) which can find the key which has the minimum value in list including 10 keys. 
def find_min(relist,dic_reg,lenOftop):
    minkey=relist[0]
    for k in range(1,lenOftop):
        if dic_reg[minkey]>dic_reg[relist[k]]:
           minkey=relist[k]
    return minkey

# definite the function to save one list(top_list) and sort list (e.g.top 10 active host/IP address , top 10 resources)
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


# definite a dictionary (dic_host): key=host/IP,value=how many times this key(host/ip) access the site
# definite a dictionary (dic_site):key=site,value= bytes  
# definite a dictionary (dic_time):key=time,value=how many times the sites was accessed during that time period
dic_host={}
dic_site={}
window_5min={} # save the host/IP that need be blocked in after 5 minutes,key is host/IP, value is  Time
window_20sec={} # save the host/IP that need be record in 20sec, key is host,value is [times,Time] that times means failed login in 20sec
blocked=[]

lenOftop=10

for line in f.readlines()[0:]:
    # feature 1
    host,site,code,Time=getId(line)
    if host in dic_host:
       dic_host[host]+=1
    else:
       dic_host[host]=1

    #feature 2
    if type(line.split(" ")[-1])!=int:
       byte=0
    else:
       byte=int(int(line.split(" ")[-1]))
    if site in dic_site:
       dic_site[site]+=byte
    else:
       dic_site[site]=byte
    #feature 3

    #feature 4
    if code!=200:  # whether failed login
       if window_5min.has_key(host)==True and (Time-window_5min[host]).seconds<=300:    # check whether this host/IP alraedy blocked 
          blocked.append(line)
       if window_5min.has_key(host)==True and (Time-window_5min[host]).seconds>300:
          del window_5min[host]
       if window_5min.has_key(host)==False:               # the host not be block now
          if window_20sec.has_key(host)==False:           # first time failed login in 20sec 
             window_20sec[host]=[1,Time]
          else:                                            #not first time failed login   
               if (Time-window_20sec[host][1]).seconds>20:#second failed login over 20sec
                    del window_20sec[host]
               else:
                    if window_20sec[host][0]==1:# second failed login in 20sec
                       window_20sec[host][0]=2
                    else:                      #  #third failed login in 20sec
                         blocked.append(line)
                         window_5min[host]=Time

#feature 1
f1=toplist(dic_host,lenOftop)
outf1=open('hosts.txt','w')
for line in f1:
    outf1.write(str(line)+","+str(dic_host[line])+'\n')

#feature 2
f2=toplist(dic_site,lenOftop)
outf2=open('resources.txt','w')
for line in f2:
    outf2.write(str(line).replace("[","").replace("]","")+'\n')

#feature 4
outf4=open('blocked.txt','w')
for i in range(0,len(blocked)):
    line=str(blocked[i])
    outf4.write(line)

