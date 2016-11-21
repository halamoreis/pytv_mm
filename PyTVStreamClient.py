#!/usr/bin/python2.7
import socket
import sys, time

#To use Thread
from threading import Thread

#Variaveis Globais
global TAMANHO_BUFFER
TAMANHO_BUFFER = 5
#Indexador do Buffer de videos Requisitados
global IDX_REQ
IDX_REQ = 0
#Indexador do Buffer de videos Recebidos
global IDX_REC
IDX_REC = 0

#Valor do Jitter Calculado
global JITTER
JITTER = 0

#BUFFER onde o player vai solicitar o download de videos do servidor
global BUFFER_REQUISITADOS
BUFFER_REQUISITADOS = [ 3*[0] for i in range(TAMANHO_BUFFER) ]
#BUFFER onde o player verifica os arquivos baixados pelo servidor
global BUFFER_RECEBIDOS
BUFFER_RECEBIDOS    = [ 3*[0] for i in range(TAMANHO_BUFFER) ]

#Preenche os buffers com valores -1
for i in range(TAMANHO_BUFFER):
    for j in range(3):
        BUFFER_REQUISITADOS[i][j] = -1
        BUFFER_RECEBIDOS[i][j]    = -1


int(round(time.time() * 1000))


class Client(Thread):
    def __init__ (self):
       Thread.__init__(self)

       #Variaveis
       self.BUFSIZE = 167535
       #global IDX_REQ

    def run(self):
       global IDX_REQ
       global IDX_REC
       global JITTER
       JITTER_MSeg_ARRAY = [0,0,0,0,0]

       try:
           #TESTE BUFFER
           BUFFER_REQUISITADOS[0][0] = 1
           BUFFER_REQUISITADOS[0][1] = 1
           BUFFER_REQUISITADOS[0][2] = 1

           BUFFER_REQUISITADOS[1][0] = 1
           BUFFER_REQUISITADOS[1][1] = 1
           BUFFER_REQUISITADOS[1][2] = 2

           while True:

               if (BUFFER_REQUISITADOS[IDX_REQ][0] == -1):
                   print "Verificando o BUFFER DE REQUISICOES..."
                   IDX_REQ = IDX_REQ +1
                   if(IDX_REQ == TAMANHO_BUFFER):
                       IDX_REQ =0
               else:
                   # Create a TCP/IP socket
                   self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                   # Connect the socket to the port where the server is listening
                   self.server_address = ('localhost', 10000)
                   print >>sys.stderr, 'connecting to %s port %s' % self.server_address
                   self.sock.connect(self.server_address)

                   # Send data
                   self.message =  str(BUFFER_REQUISITADOS[IDX_REQ][0])+";"+\
                                   str(BUFFER_REQUISITADOS[IDX_REQ][1])+";"+\
                                   str(BUFFER_REQUISITADOS[IDX_REQ][2])
                   print >>sys.stderr, 'sending "%s"' % self.message
                   self.sock.send(self.message)

                   i=0

                   self.vdo_file = "videosout/rcv_"+str(BUFFER_REQUISITADOS[IDX_REQ][0])+"_"+\
                                   str(BUFFER_REQUISITADOS[IDX_REQ][1])+"_"+\
                                   str(BUFFER_REQUISITADOS[IDX_REQ][2])+".webm"

                   self.myfile = open(self.vdo_file, 'w')
                   t = 0
                   while True:
                       self.data = self.sock.recv(self.BUFSIZE)
                       if not self.data:
                           print "No data"
                           break
                       JITTER_MSeg_ARRAY[t] = int(round(time.time() * 1000))
                       t = t + 1
                       #token que indica o fim de envio de um arquivo
                       if ("AAAAFFFFFFGGGGGGQQQQQQQQQ" in self.data):
                           print "Arquivo "+self.vdo_file+" Recebido !"
                           self.myfile.close()
                           while (BUFFER_RECEBIDOS[IDX_REC][0] != -1):
                               IDX_REC = IDX_REC +1
                               if(IDX_REC == TAMANHO_BUFFER):
                                   IDX_REC =0
                           BUFFER_RECEBIDOS[IDX_REC][0] = BUFFER_REQUISITADOS[IDX_REQ][0]
                           BUFFER_RECEBIDOS[IDX_REC][1] = BUFFER_REQUISITADOS[IDX_REQ][1]
                           BUFFER_RECEBIDOS[IDX_REC][2] = BUFFER_REQUISITADOS[IDX_REQ][2]

                           BUFFER_REQUISITADOS[IDX_REQ][0] = -1
                           BUFFER_REQUISITADOS[IDX_REQ][1] = -1
                           BUFFER_REQUISITADOS[IDX_REQ][2] = -1
                           IDX_REQ = IDX_REQ + 1
                           break
                       else:
                           self.myfile.write(self.data)
                           print 'writing file %s....' % i

       finally:
           print >>sys.stderr, 'closing socket'
           self.sock.close()


client = Client();
client.start();