# -*- coding: utf-8 -*- 
import os
import BaseHTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
import urllib2
import urllib
import cookielib
import re
class Spider():
    def __init__(self,input_url,input_anget):
        self.url = input_url
        self.user_anget = input_anget
        #self.cookie = cooielib.
class WebServer():
    def __init__(self,input_prot):
        self.HandlerClass = SimpleHTTPRequestHandler
        self.ServerClass = BaseHTTPServer.HTTPServer
        self.Protocol = "HTTP/1.0"
        if input_prot == '':
            self.port = 1234
            
        else:
            self.port = input_prot
    def start_server(self):
        server_address = ('',self.port)
        self.HandlerClass.protocol_version = self.Protocol
        httpd = self.ServerClass(server_address,self.HandlerClass)
        sa = httpd.socket.getsockname()
        print sa
        httpd.serve_forever()
if __name__ == "__main__":
    webserver = WebServer('')
    webserver.start_server()
        
    
