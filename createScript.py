#!/usr/bin/env python
import sys
import os
import time
from subprocess import Popen, PIPE

curDir = os.path.abspath('.')

remoteAddr = ''

def shell_Cmd(str):
    return Popen(str, shell=True, stdout=PIPE, stderr=PIPE)

# p = shell_Cmd('ping 172.16.105.90')
# while p.poll() == None:
#     print p.stdout.readline()
#     time.sleep(1)
# print p.stdout.read()


def get_IP():
    p = shell_Cmd("ifconfig")
    res = p.stdout.readlines()
    ip = ''
    for line in res:
        if line.find('Bcast') >= 0:
            ip = line.split(':')[1].split()[0]
    return ip


def mstarCommand(factorytftpIP, servertftpAddr, serverIp='172.16.11.20'):
    """
    factorytftp: factoryimg tftp IP
    servertftpAddr: remote img folder addresss like below
            'h01p55r-release-00.02/H01P55R-00.02.13-1532204-11/helios/scripts/'
    """
    factoryTftpPath = 'scripts/[[factory'
    remotePath = servertftpAddr
    command_List = []
    command_List.append('mmc erase.boot 2 0 512')
    command_List.append('mmc erase')
    command_List.append('mmc write.p 0x20200000 MBOOT $(filesize)')
    command_List.append('set serverip ' + serverIp)
    command_List.append('mstar ' + os.path.join(remotePath, 'scripts/set_partition'))
    command_List.append('set serverip ' + factorytftpIP)
    command_List.append('mstar ' + factoryTftpPath)
    command_List.append('mstar ' + os.path.join(remotePath, 'scripts/[[mboot'))
    return command_List


def create_Script(command_List):
    command_Str = ''
    for c in command_List:
        command_Str += c + '\n'
    filePath = os.path.join(curDir, 'mupianScript')
    try:
        with open(filePath, mode='w+') as f:
            f.write(command_Str)
    except StandardError, e:
        print e

com = mstarCommand(get_IP(), 'h01p55r-release-00.02/H01P55R-00.02.13-1532204-11/helios/')
create_Script(com)
