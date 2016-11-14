#!/usr/bin/python2.7
import socket
import sys, time

#To use Thread
from threading import Thread

class Client(Thread):
    def __init__ (self):
       Thread.__init__(self)

       #Variaveis
       self.BUFSIZE = 167535
       
       # Create a TCP/IP socket
       self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       
       # Connect the socket to the port where the server is listening
       self.server_address = ('localhost', 20000)
       print >>sys.stderr, 'connecting to %s port %s' % self.server_address
       self.sock.connect(self.server_address)

    def run(self):

       try:
       
           # Send data
           self.message = '1,1'
           print >>sys.stderr, 'sending "%s"' % self.message
           self.sock.send(self.message)
       
           i=0
       
           self.myfile = open("videosout/testfile"+str(i).zfill(3)+".webm", 'w')
           while True:
               self.data = self.sock.recv(self.BUFSIZE)
               if not self.data: 
		   print "No data"
		   break
               if ("AAAAFFFFFFGGGGGGQQQQQQQQQ" in self.data):
                   self.myfile.close()
                   i = i + 1
                   self.myfile = open("videosout/testfile"+str(i).zfill(3)+".webm", 'w')
                   print 'Entrou Aqui !'
               else:
                   self.myfile.write(self.data)
               print 'writing file %s....' % i
       
           self.myfile.close()
       
       #    while amount_received < amount_expected:
       #        data = sock.recv(16)
       #        amount_received += len(data)
       #        print >>sys.stderr, 'received "%s"' % data
       
       finally:
           print >>sys.stderr, 'closing socket'
           self.sock.close()
