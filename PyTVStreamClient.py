#!/usr/bin/python2.7
# coding=utf-8
import socket
import sys, time
import os

#To use Thread
from threading import Thread

FILE_EXTENSION = ".mp4"

class Client(Thread):
    def __init__ (self):
       Thread.__init__(self)

       #Variaveis
       # self.BUFSIZE = 167535
       self.BUFSIZE = 1024
       # Representa a fila de pedidos
       self.fifoRequest = []
       # Representa a fila de fragmentos recebidos
       self.fifoReceived = []
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

    def requestVideo(self, codigo, resolucao, fragmento):
        sum = 0
        tIDX = -2
        # print "entrei aqui !"
        print ">>> >>>Solicitando vídeo [%d] resolução [%d] fragmento [%d]" % (codigo, resolucao, fragmento)
        self.IDX_REQ =0
        request = [codigo, resolucao, fragmento]
        self.fifoRequest.append(request)

        return request

        # while (sum < self.TAMANHO_BUFFER):
        #     if(self.BUFFER_REQUISITADOS[self.IDX_REQ][0] == -1):
        #         self.BUFFER_REQUISITADOS[self.IDX_REQ][0] = codigo
        #         self.BUFFER_REQUISITADOS[self.IDX_REQ][1] = resolucao
        #         self.BUFFER_REQUISITADOS[self.IDX_REQ][2] = fragmento
        #         tIDX = self.IDX_REQ
        #         print "Adicionado em : "+str(self.IDX_REQ)
        #         break
        #     else:
        #         self.IDX_REQ = self.IDX_REQ +1
        #         if(self.IDX_REQ == self.TAMANHO_BUFFER):
        #             self.IDX_REQ =0
        #     sum = sum + 1
        # return tIDX

    def wasReceivedVideo(self, codigo, resolucao, fragmento):
        sum = 0
        tFIND = -1
        for i in range(0, self.TAMANHO_BUFFER):
            if( (self.BUFFER_RECEBIDOS[i][0] == codigo) and
                (self.BUFFER_RECEBIDOS[i][1] == resolucao) and
                (self.BUFFER_RECEBIDOS[i][2] == fragmento) ):
                    tFIND = i
        return tFIND
    # end wasReceivedVideo



    def getNextReceived(self):
        print self.fifoReceived
        if(len(self.fifoReceived)):
            request = self.fifoReceived[0]
            self.fifoReceived.remove(request)
            return request
        return False
    # end getNextReceived

    def watchedVideo(self, idx):
        sum = 0
        foundFragment = False
        # Pesquisa o fragmento
        for i in range(0, self.TAMANHO_BUFFER-1):
            if(idx == self.BUFFER_RECEBIDOS[i][2]):
                print "[client] Encontrou fragmento %d na posição %d" % (idx, i)
                idx = i
                foundFragment = True
                break

        if(foundFragment):
            if(self.BUFFER_RECEBIDOS[idx][0] != -1):
                vdo_file = "videosout/rcv_"+str(self.BUFFER_RECEBIDOS[idx][0])+"_"+\
                                       str(self.BUFFER_RECEBIDOS[idx][1])+"_"+\
                                       str(self.BUFFER_RECEBIDOS[idx][2])+".webm"
                # os.remove(vdo_file)
                self.BUFFER_RECEBIDOS[idx][0] = -1
                self.BUFFER_RECEBIDOS[idx][1] = -1
                self.BUFFER_RECEBIDOS[idx][2] = -1
        else:
            print "Não encontrou o fragmento "+str(idx)
    # End watchedVideo


    """ Retorna a string correspondente ao path do vídeo solicitado.
    >>>
    """
    def getVideo(self, codigo, resolucao, fragmentNumber):
        # return "videosout/rcv_"+ str(codigo).zfill(3) + "_"+str(self.BUFFER_RECEBIDOS[idx][1]) + "_"+str(idx).zfill(3) + ".webm"
        vdo_file = "videosout/rcv_" + str(codigo) + "_" + \
                   str(resolucao) + "_" + \
                   str(fragmentNumber) + ".webm"
        return vdo_file

    def run(self):
        try:

            self.IDX_REQ =0

            while True:
                time.sleep(0.1)

                # Verifica se existem pedidos a serem processados na fila
                if (len(self.fifoRequest)):
                    # Desempacota o pedido (array contendo [codigo, resolucao, fragmento])
                    request = self.fifoRequest[0]
                    code = request[0]
                    resolution = request[1]
                    fragmentNumber = request[2]
                    print "[client] Vai processar a requisição [%d][%d][%d]" % (request[0],request[1],request[2])
                    # Create a TCP/IP socket
                    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    # Connect the socket to the port where the server is listening
                    self.server_address = ('localhost', 20000)
                    print >> sys.stderr, 'connecting to %s port %s' % self.server_address
                    self.sock.connect(self.server_address)

                    # Send data
                    self.message =  str(code)+";"+\
                                   str(resolution)+";"+\
                                   str(fragmentNumber)
                    print >>sys.stderr, 'sending "%s"' % self.message
                    self.sock.send(self.message)

                    i=0

                    vdo_file = "videosout/rcv_"+str(code)+"_"+\
                                   str(resolution)+"_"+\
                                   str(fragmentNumber)+FILE_EXTENSION

                    self.myfile = open(vdo_file, 'wb')
                    t = 0


                    self.data = self.sock.recv(self.BUFSIZE)
                    while (self.data):
                        if ("notfound" in self.data):
                            print "Fragmento não encontrado no servidor!"
                            break
                        self.myfile.write(self.data)
                        self.data = self.sock.recv(self.BUFSIZE)

                    self.myfile.close()
                    # Adiciona um novo arquivo recebido à fila de recebidos
                    self.fifoReceived.append((vdo_file + '.')[:-1])

                    # Remove a solicitação que foi concluída
                    self.fifoRequest.remove(request)
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