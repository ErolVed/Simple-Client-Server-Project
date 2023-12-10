import psutil
from uptime import uptime
cpu=0
while(cpu==0):
    cpu= psutil.cpu_percent(interval=0.1)
ram = psutil.virtual_memory().percent
disk = psutil.disk_usage('/')[3]
upTime=uptime()

d = str(int(upTime / 60 / 60 / 24))

h = str(int((upTime / 3600) % 24) )  

m =str(int(upTime / 60 % 60) )   

sec = str(int(upTime % 60) )     
upTime = d + ':' + h + ':' + m + ':' + sec
out = str('cpu: '+ str(cpu)+ ' ram: '+ str(ram)+ ' disk: '+ str(disk)+ ' uptime: '+ upTime)
print(out)
