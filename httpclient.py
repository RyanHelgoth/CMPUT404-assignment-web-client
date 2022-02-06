#!/usr/bin/env python3
# coding: utf-8
# Copyright 2022 Abram Hindle, Ryan Helgoth, https://github.com/tywtyw2002, and https://github.com/treedust
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib.parse as parse

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
        headers = self.get_headers(data)
        return int(headers.partition("\r\n")[0].split(" ")[1])
        
    def get_headers(self, data):
        return data[0] + data[1]
        
    def get_body(self, data):
        return data[2]
        
    def getResponseParts(self, response):
        return response.partition("\r\n\r\n")

    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8')) 
        
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8') 

    def getRequestInfo(self, url):
        urlParts = parse.urlparse(url) 
        host = urlParts[1]
        path = urlParts[2] 
        query = urlParts[4]
        fragment = urlParts[5]
        port = 80

        '''
        Depending on the format of the url, it will somtimes be
        split incorrectly.
        The check code below fixes this.

        Ex: url = coolbears.ca -->
            After url parse: host = "", path = "coolbears.ca" -->
            After code below: host = "coolbears.ca", path = "/"
        '''
        if host == "":
            host = path
            path = "/"

        if path == "":
            path = "/"

        if ":" in host:
            hostPartition = host.partition(":") 
            host = hostPartition[0] #Gets host without port number
            port = int(hostPartition[2]) #Gets port number

        if not query == "":
            path = path + "?" + query

        if not fragment == "":
            path = path + "#" + fragment
        return host, path, port
    
    def getResponse(self, host, port, request):
        self.connect(host, port)
        self.sendall(request)
        self.socket.shutdown(socket.SHUT_WR)
        response = self.recvall(self.socket)
        self.close()
        return response

    def constructPostRequest(self, args, path, host):
        length = 0 
        vals = []
        request = ""
    
        if not args is None:
            for arg in args:
                val = "{0}={1}&".format(arg, args[arg])
                ''' 
                Link: https://stackoverflow.com/a/30686735
                Author: Kris
                Date: Jun 6 '15 at 19:37
                License: SA 3.0
                '''
                length += len(val.encode("utf-8")) 
                vals.append(val)

        headers = [
            "POST {} HTTP/1.1\r\n".format(path),
            "Host: {}\r\n".format(host),
            "Content-Type: application/x-form-urlencoded; charset=UTF-8\r\n",
            "Content-Length: {}\r\n".format(length),
            "Connection: close\r\n",
            "\r\n"
        ]

        for header in headers:
            request += header

        for val in vals:
            request += val

        return request 

    def GET(self, url, args=None):
        host, path, port = self.getRequestInfo(url)
        
        request = "GET {0} HTTP/1.1\r\nHost: {1}\r\nConnection: close\r\n\r\n".format(path, host)
        
        response = self.getResponse(host, port, request)
        responsePartition = self.getResponseParts(response)
        
        body = self.get_body(responsePartition)
        code = self.get_code(responsePartition)

        print(body)
        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        host, path, port = self.getRequestInfo(url)
            
        request = self.constructPostRequest(args, path, host)
        
        response = self.getResponse(host, port, request)
        responsePartition = self.getResponseParts(response)
        
        body = self.get_body(responsePartition)
        code = self.get_code(responsePartition)

        print(body)
        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
   
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        client.command(sys.argv[2], sys.argv[1])
    else:
        client.command(sys.argv[1])




