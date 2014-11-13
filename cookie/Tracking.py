# -*- coding: utf-8 -*- 
import os


class Tracking:
    def __init__(self,num):
        self.device_id = num
        self.macAddressWired = ''
        self.macAddressWireless = ''
        self.macAddress = ''
        self.track_datas = []
        self.end = False
    def get_datas(self):
        #cmd = 'tshark -i '+self.device_id+' -f "tcp dst port 80 or udp src port 5353 or udp src port 138"'
        cmd = 'tshark -i '+self.device_id+' -f "tcp dst port 80 or udp src port 5353 or udp src port 138" -T "fields" -e "eth.src" -e "wlan.sa" -e "ip.src" -e "ipv6.src" -e "tcp.srcport" -e "tcp.dstport" -e "udp.srcport" -e "udp.dstport" -e "browser.command" -e "browser.server" -e "dns.resp.name" -e "http.host" -e "http.request.uri" -e "http.accept" -e "http.accept_encoding" -e "http.user_agent" -e "http.referer" -e "http.cookie" -e "http.authorization" -e "http.authbasic"'
        #print cmd
        lines = os.popen(cmd)
        while True:
            if self.end:
                print 'end'
                return
            output = lines.readline()[0:-1]
            if len(output)==0:
                return ''
            if '\t' in output:
                value = output.split('\t')
                if len(value)<4:
                    continue
                else:
                    self.macAddressWired = value[0]
                    self.macAddressWireless = value[1]
                    if(self.macAddressWired):
                        self.macAddress = self.macAddressWired
                    elif(self.macAddressWireless):
                        self.macAddress = self.macAddressWireless
                    else:
                        self.macAddress = 'Unknown'
                    track_info={}
                    track_info['mac'] = self.macAddress
                    ipv4Address=value[2]
                    track_info['ipv4'] = ipv4Address
                    ipv6Address=value[3]
                    track_info['ipv6'] = ipv6Address
                    #value[5] none
                    tcpDestination=value[5]
                    track_info['tcp'] = tcpDestination
                    udpSource=value[6]
                    track_info['udp'] =udpSource
                    #value[7] none
                    netbiosCommand=value[8]
                    track_info['netbiosCommand'] = netbiosCommand
                    netbiosName=value[9]
                    track_info['netbiosName'] = netbiosName
                    mdnsName=value[10]
                    track_info['mdnsName'] = mdnsName
                    requestHost=value[11]
                    track_info['requestHost'] = requestHost
                    requestUri=value[12]
                    track_info['requestUri'] = requestUri
                    accept=value[13]
                    track_info['accept'] = accept
                    acceptEncoding=value[14]
                    track_info['acceptEncoding'] = acceptEncoding
                    userAgent=value[15]
                    track_info['userAgent'] = userAgent
                    refererUri=value[16]
                    track_info['refererUrl'] = refererUri
                    cookieData=value[17]
                    track_info['cookieData'] = cookieData
                    authorization=value[18]
                    track_info['authorization'] = authorization
                    authBasic=value[19]
                    track_info['authBasic'] =authBasic
                    
                    if len(track_info['requestUri'])>0:
                        print track_info
                        self.track_datas.append(track_info);
if __name__ == '__main__':
    print "init system"
    num = '5'
    device = Tracking(num)
    device.get_datas()
