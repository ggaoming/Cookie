#!/usr/bin/python2.7  
# -*- coding: utf-8 -*- 
import os


class Deviceid:
    def __init__(self):
        self.device_id = []
        self.device_mac = []
        self.device_name = []
    def getDevices(self):
        cmd = 'tshark -D'
        lines = os.popen(cmd).readlines()
        print 'Device :'
        for line in lines:
            line = line.split(' ',2)
            device_id = line[0][0]
            device_mac = line[1][13:-1]
            device_name = line[2][1:-2].decode('utf-8')
            print device_id,device_mac,device_name
            self.device_id.append(device_id)
            self.device_mac.append(device_mac)
            self.device_name.append(device_name)
        return self.device_id,self.device_mac,self.device_name
       
        






if __name__ == '__main__':
    print "init system"
    device = Deviceid()
    num,mac,name, = device.getDevices()
