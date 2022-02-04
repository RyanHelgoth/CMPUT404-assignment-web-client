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
        return None

    def get_headers(self,data):
        #TODO 
        # If \r\n\r\n reached, stop reading string
        # Else, append string to list when \r\n is reached.
            

        


        return None

    def get_body(self, data):
        return None
    
    def sendall(self, data):
        self.socket.sendall(data.encode('latin-1')) #TODO change back to utf-8
        
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
        return buffer.decode('latin-1') #TODO change back to utf-8

    def GET(self, url, args=None):
        #curl: url= http://www.google.com/ => path = /, host = www.google.com
        


        urlParts = parse.urlparse(url) 
        host = urlParts[1]
        path = urlParts[2]
        port = 80

        if ":" in host:
            hostPartition = host.partition(":") 
            host = hostPartition[0] #Gets host without port number
            port = int(hostPartition[2]) #Gets port number
            

        print(urlParts)
 
        request = "GET {0} HTTP/1.1\r\nHost: {1}\r\n\r\n".format(path, host)
        print(request)
       
        
        self.connect(host, port)
        self.sendall(request)
        self.socket.shutdown(socket.SHUT_WR)
        response = self.recvall(self.socket)
        self.close()

        #code = self.get_code(response)
        #body = self.get_body(response)
        #headers = self.get_headers(response)

        responsePartition = response.partition("\r\n\r\n")
        headers = responsePartition[0] + responsePartition[1]
        body = responsePartition[2]
        code = int(headers.partition("\r\n")[0].split(" ")[1])
        print(code)
        
        
    
        #body = response.split("\r\n") #TODO remove when done testing
        #print("CODE: " + code)
        #print("HEADERS:\n" + headers)
        #print("BODY:\n" + body)
        
        print(response)

        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        code = 500
        body = ""
        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )

    def cleanUrl(self, url):
        #Return url and https boolean
        return
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        #TODO print response 
        #print(client.command( sys.argv[2], sys.argv[1] ))
        client.command(sys.argv[2], sys.argv[1])



    else:
        #TODO print response
        print(client.command( sys.argv[1] ))


#Test run

'''
python3 freetests.py
HTTP UP!

E/usr/lib/python3.6/unittest/case.py:633: ResourceWarning: unclosed <socket.socket fd=4, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('0.0.0.0', 0)>
  outcome.errors.clear()
FEEAn Exception was thrown for http://www.cs.ualberta.ca/
FSending POST!
FFHTTP Shutdown in tearDown

HTTP has been shutdown!


======================================================================
ERROR: test404GET (__main__.TestHTTPClient)
Test against 404 errors
----------------------------------------------------------------------
Traceback (most recent call last):
  File "freetests.py", line 162, in test404GET
    req = http.GET("http://%s:%d/49872398432" % (BASEHOST,BASEPORT) )
  File "/home/student/Assignments/CMPUT404-assignment-web-client/httpclient.py", line 83, in GET
    self.connect(url, httpPort)
  File "/home/student/Assignments/CMPUT404-assignment-web-client/httpclient.py", line 40, in connect
    self.socket.connect((host, port))
socket.gaierror: [Errno -2] Name or service not known

======================================================================
ERROR: testGET (__main__.TestHTTPClient)
Test HTTP GET
----------------------------------------------------------------------
Traceback (most recent call last):
  File "freetests.py", line 180, in testGET
    req = http.GET( url )
  File "/home/student/Assignments/CMPUT404-assignment-web-client/httpclient.py", line 83, in GET
    self.connect(url, httpPort)
  File "/home/student/Assignments/CMPUT404-assignment-web-client/httpclient.py", line 40, in connect
    self.socket.connect((host, port))
socket.gaierror: [Errno -2] Name or service not known

======================================================================
ERROR: testGETHeaders (__main__.TestHTTPClient)
Test HTTP GET Headers
----------------------------------------------------------------------
Traceback (most recent call last):
  File "freetests.py", line 192, in testGETHeaders
    req = http.GET( url )
  File "/home/student/Assignments/CMPUT404-assignment-web-client/httpclient.py", line 83, in GET
    self.connect(url, httpPort)
  File "/home/student/Assignments/CMPUT404-assignment-web-client/httpclient.py", line 40, in connect
    self.socket.connect((host, port))
socket.gaierror: [Errno -2] Name or service not known

======================================================================
FAIL: test404POST (__main__.TestHTTPClient)
Test against 404 errors
----------------------------------------------------------------------
Traceback (most recent call last):
  File "freetests.py", line 172, in test404POST
    self.assertTrue(req.code == 404)
AssertionError: False is not true

======================================================================
FAIL: testInternetGets (__main__.TestHTTPClient)
Test HTTP Get in the wild, these webservers are far less
----------------------------------------------------------------------
Traceback (most recent call last):
  File "freetests.py", line 223, in testInternetGets
    req = http.GET( url )
socket.gaierror: [Errno -2] Name or service not known

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "freetests.py", line 226, in testInternetGets
    self.assertTrue( False, "An Exception was thrown for %s %s" % (url,e))
AssertionError: False is not true : An Exception was thrown for http://www.cs.ualberta.ca/ [Errno -2] Name or service not known

======================================================================
FAIL: testPOST (__main__.TestHTTPClient)
Test HTTP POST with an echo server
----------------------------------------------------------------------
Traceback (most recent call last):
  File "freetests.py", line 250, in testPOST
    self.assertTrue(req.code == 200)
AssertionError: False is not true

======================================================================
FAIL: testPOSTHeaders (__main__.TestHTTPClient)
Test HTTP POST Headers
----------------------------------------------------------------------
Traceback (most recent call last):
  File "freetests.py", line 205, in testPOSTHeaders
    self.assertTrue(req.code == 200,"Code is %s but I wanted a 200 OK" % req.code)
AssertionError: False is not true : Code is 500 but I wanted a 200 OK

----------------------------------------------------------------------
Ran 7 tests in 2.520s

FAILED (failures=4, errors=3)






'''