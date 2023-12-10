import os
import pexpect as pex
from paramiko import SSHClient, AutoAddPolicy
import xml.etree.ElementTree as ET
import ClientInfo as ci
from sqlalchemy.orm import sessionmaker

def run_server():
    root_path='./PecanProject/pecanproject/'
    file = ET.parse(root_path + 'ClientsAddresses.xml')
    myroot = file.getroot()
    LocalSession = sessionmaker(bind=ci.engine, autoflush= False)
    session = LocalSession()

    for client in myroot.findall('client'):
        id = myroot.findall('client').index(client) + 1
        ipa = client.attrib.get('ip')
        user = client.attrib.get('username')
        psword= client.attrib.get('password')
        p = pex.spawn("scp "+root_path+"client.py "+user+"@"+ipa+":/tmp/tempclient.py")
        index = p.expect(['continue','password'])
        if index==0:
            p.sendline('yes')
            p.expect('password')
            p.sendline('r')
        elif index == 1:
            p.sendline('r')
        print(p.read())
        ssh = SSHClient()
        ssh.set_missing_host_key_policy(AutoAddPolicy())
        ssh.connect(ipa,username=user,password=psword)
        stdin, stdout, stderr=ssh.exec_command('python3 /tmp/tempclient.py')
        out = stdout.read().decode("utf8")
        all = out.split(' ')
        prev = 'abc'
        cpuu = 5
        ramu = 5
        disku = 5
        up_time = 'abc'
        print(all)
        for word in all:
            if(prev=='cpu:'):
                cpuu = word
            elif(prev=='ram:'):
                ramu = word
            elif(prev=='disk:'):
                disku = word
            elif(prev == 'uptime:'):
                up_time = word
            prev = word
        newColumn = ci.ClientInfo(id = id, ip = ipa.strip(), cpu = cpuu, ram = ramu, disk = disku, upTime = up_time.strip())
        newObject = True
        for obj in session.query(ci.ClientInfo).all():
            if(obj.ip == ipa):
                obj.cpu = cpuu
                obj.ram = ramu
                obj.disk = disku
                obj.upTime = up_time
                newObject = False
                break
        if(newObject):
            session.add(newColumn)
        json_data = {}
        for obj in session.query(ci.ClientInfo).all():
            json_data["client"+str(obj.id)]={
            "id" : obj.id,
            "ip" : obj.ip,
            "cpu" : obj.cpu,
            "ram" : obj.ram,
            "disk" : obj.disk,
            "uptime" : obj.upTime
        }

        stdin.close()
        stdout.close()
        stderr.close()
        ssh.close()
    session.commit()
run_server()