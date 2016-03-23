#!/usr/bin/env python
import sys
import os
import time
from subprocess import Popen, PIPE
from optparse import OptionParser


defaultRemoteIp = '172.16.11.20'
parser = OptionParser()
parser.add_option('-s', '--serverip', dest="serverIp",
                    help="remote tftp serverIp, default is %s" % defaultRemoteIp)
parser.add_option('-p', '--serverScriptsPath', dest='serverScriptsPath',
                    help="""remote server scripts addresss like          \n
h01p55r-release-00.02/H01P55R-00.02.13-1532204-11/helios/scripts/""")


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


def mstarCommand(factorytftpIP, serverScriptsPath, serverIp):
    """
    factorytftp: factoryimg tftp IP
    serverScriptsPath: remote server scripts addresss like below
            'h01p55r-release-00.02/H01P55R-00.02.13-1532204-11/helios/scripts/'
    """
    factoryTftpPath = 'scripts/[[factory'
    remotePath = serverScriptsPath
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


def comList2Str(command_List):
    return '\n'.join(command_List)

def create_Script(commandstr):
    filePath = os.path.join(curDir, 'mupianScript')
    try:
        with open(filePath, mode='w+') as f:
            f.write(commandstr)
    except StandardError, e:
        print e

(options, args) = parser.parse_args()

if options.serverIp is None:
    options.serverIp = defaultRemoteIp

if options.serverScriptsPath is None:
    parser.error('need input remote scripts addresss')

if __name__ == '__main__':
    com = mstarCommand(get_IP(), options.serverScriptsPath, options.serverIp)
    print '\n'.join(com)
    create_Script('\n'.join(com))