#!/usr/bin/python2.7
import socket
import sys, time
import os

#To use Thread
from threading import Thread


class Client(Thread):
    def __init__ (self):
       Thread.__init__(self)

       #Variaveis
       self.BUFSIZE = 167535
       #Variaveis Globais
       self.TAMANHO_BUFFER = 5
       self.IDX_REQ = 0
       self.IDX_REC = 0
       self.JITTER = 0

       self.BUFFER_REQUISITADOS = [ 3*[0] for i in range(self.TAMANHO_BUFFER) ]
       #BUFFER onde o player verifica os arquivos baixados pelo servidor
       self.BUFFER_RECEBIDOS    = [ 3*[0] for i in range(self.TAMANHO_BUFFER) ]
       self.JITTER_MSeg_ARRAY = [3]

       #Preenche os buffers com valores -1
       for i in range(self.TAMANHO_BUFFER):
           for j in range(3):
               self.BUFFER_REQUISITADOS[i][j] = -1
               self.BUFFER_RECEBIDOS[i][j]    = -1

    def reqVideo(self, codigo, resolucao, fragmento):
        sum = 0
        tIDX = -2
        print "entrei aqui !"
        self.IDX_REQ =0

        while (sum < self.TAMANHO_BUFFER):
            if(self.BUFFER_REQUISITADOS[self.IDX_REQ][0] == -1):
                self.BUFFER_REQUISITADOS[self.IDX_REQ][0] = codigo
                self.BUFFER_REQUISITADOS[self.IDX_REQ][1] = resolucao
                self.BUFFER_REQUISITADOS[self.IDX_REQ][2] = fragmento
                tIDX = self.IDX_REQ
                print "Adicionado em : "+str(self.IDX_REQ)
                break
            else:
                self.IDX_REQ = self.IDX_REQ +1
                if(self.IDX_REQ == self.TAMANHO_BUFFER):
                    self.IDX_REQ =0
            sum = sum + 1
        return tIDX

    def recVideo(self, codigo, resolucao, fragmento):
        sum = 0
        tFIND = -1
        for i in range(0, self.TAMANHO_BUFFER):
            if( (self.BUFFER_RECEBIDOS[i][0] == codigo) and
                (self.BUFFER_RECEBIDOS[i][1] == resolucao) and
                (self.BUFFER_RECEBIDOS[i][2] == fragmento) ):
                    tFIND = i
        return tFIND

    def watchedVideo(self, idx):
        sum = 0
        if(self.BUFFER_RECEBIDOS[idx][0] != -1):
            vdo_file = "videosout/rcv_"+str(self.BUFFER_RECEBIDOS[idx][0])+"_"+\
                                   str(self.BUFFER_RECEBIDOS[idx][1])+"_"+\
                                   str(self.BUFFER_RECEBIDOS[idx][2])+".webm"
            os.remove(vdo_file)
            self.BUFFER_RECEBIDOS[idx][0] == -1
            self.BUFFER_RECEBIDOS[idx][1] == -1
            self.BUFFER_RECEBIDOS[idx][2] == -1


    def run(self):
       try:

          self.IDX_REQ =0

          while True:

               if (self.BUFFER_REQUISITADOS[self.IDX_REQ][0] == -1):
                   #print "."
                   self.IDX_REQ = self.IDX_REQ +1
                   if(self.IDX_REQ == self.TAMANHO_BUFFER):
                       self.IDX_REQ =0
               else:
                   # Create a TCP/IP socket
                   self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                   # Connect the socket to the port where the server is listening
                   self.server_address = ('localhost', 20000)
                   print >>sys.stderr, 'connecting to %s port %s' % self.server_address
                   self.sock.connect(self.server_address)

                   # Send data
                   self.message =  str(self.BUFFER_REQUISITADOS[self.IDX_REQ][0])+";"+\
                                   str(self.BUFFER_REQUISITADOS[self.IDX_REQ][1])+";"+\
                                   str(self.BUFFER_REQUISITADOS[self.IDX_REQ][2])
                   print >>sys.stderr, 'sending "%s"' % self.message
                   self.sock.send(self.message)

                   i=0

                   self.vdo_file = "videosout/rcv_"+str(self.BUFFER_REQUISITADOS[self.IDX_REQ][0])+"_"+\
                                   str(self.BUFFER_REQUISITADOS[self.IDX_REQ][1])+"_"+\
                                   str(self.BUFFER_REQUISITADOS[self.IDX_REQ][2])+".webm"

                   self.myfile = open(self.vdo_file, 'w')
                   t = 0
                   while True:
                       self.data = self.sock.recv(self.BUFSIZE)
                       if not self.data:
                           print "No data"
                           break
                       #self.JITTER_MSeg_ARRAY[t] = int(round(time.time() * 1000))
                       #t = t + 1
                       #token que indica o fim de envio de um arquivo
                       if ("AAAAFFFFFFGGGGGGQQQQQQQQQ" in self.data):
                           print "Arquivo "+self.vdo_file+" Recebido !"
                           self.myfile.close()
                           while (self.BUFFER_RECEBIDOS[self.IDX_REC][0] != -1):
                               self.IDX_REC = self.IDX_REC +1
                               if(self.IDX_REC == self.TAMANHO_BUFFER):
                                   self.IDX_REC =0
                           self.BUFFER_RECEBIDOS[self.IDX_REC][0] = self.BUFFER_REQUISITADOS[self.IDX_REQ][0]
                           self.BUFFER_RECEBIDOS[self.IDX_REC][1] = self.BUFFER_REQUISITADOS[self.IDX_REQ][1]
                           self.BUFFER_RECEBIDOS[self.IDX_REC][2] = self.BUFFER_REQUISITADOS[self.IDX_REQ][2]

                           self.BUFFER_REQUISITADOS[self.IDX_REQ][0] = -1
                           self.BUFFER_REQUISITADOS[self.IDX_REQ][1] = -1
                           self.BUFFER_REQUISITADOS[self.IDX_REQ][2] = -1
                           self.IDX_REQ = self.IDX_REQ + 1
                           break
                       else:
                           self.myfile.write(self.data)
                           print 'writing file %s....' % i

       finally:
           print >>sys.stderr, 'closing socket'
           self.sock.close()

#Como Usar a Classe
#client = Client()
#client.start()

#client.reqVideo( 1, 1, 1)
#client.reqVideo( 1, 1, 2)
#client.reqVideo( 1, 1, 3)
#time.sleep(5)
#vd1 = client.recVideo( 1, 1, 1)
#vd2 = client.recVideo( 1, 1, 2)
#vd3 = client.recVideo( 1, 1, 3)

#print "vd 1 : "+str(vd1)
#print "vd 2 : "+str(vd2)
#print "vd 3 : "+str(vd3)

#client.watchedVideo(vd1)
#client.watchedVideo(vd2)
#client.watchedVideo(vd3)