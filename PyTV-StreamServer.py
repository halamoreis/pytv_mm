import socket
import os.path
import sys, time



#Variaveis
CODIGO = 1
RESOLUCAO = 1
ARRAY_RESOLUCAO = ["160x90_250k","320x180_500k","640x360_750k"]
BUFSIZE = 1024

REQ = ["","",""]

TIME_SLEEP = 2

#Criando o canal TCP de comunicacao servidor Cliente
# Create a TCP/IP socket
sockCTL = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to the port
server_address = ('localhost', 20000)
print >>sys.stderr, 'Iniciando o canal de controle em  %s porta %s' % server_address
sockCTL.bind(server_address)

# Listen for incoming connections
sockCTL.listen(1)

while True:
    # Wait for a connection
    print >>sys.stderr, 'waiting for a connection'
    connection, client_address = sockCTL.accept()
    try:
        print >>sys.stderr, 'connection from', client_address

        # Receive the data in small chunks and retransmit it

        data = connection.recv(BUFSIZE)
        print >>sys.stderr, 'received "%s"' % data
        if data != "":
            i=0
            req = data.split(";")
            # Loop and print each city name.
            for element in req:
                REQ[i] = element
                #print str(i)+"-"+REQ[i]
                i = i + 1

            videofile = "videos/"+REQ[0].zfill(3)+"-"+ARRAY_RESOLUCAO[int(REQ[1])]+"_"+REQ[2].zfill(3)+".webm"
            #videofile = "videos/"+REQ[0].zfill(3)+ARRAY_RESOLUCAO[int(REQ[1])]+REQ[2].zfill(3)+".webm"
            #print videofile

            if (os.path.exists(videofile) is True ):
                VidFILE = open(videofile).read()
                #print videofile
                #print len(VidFILE)
                connection.sendall(VidFILE)
                connection.send("AAAAFFFFFFGGGGGGQQQQQQQQQ") #tag de final de arquivo
                print "Arquivo : "+videofile+" Tamanho : "+str(len(VidFILE))+" Enviado !"
                time.sleep(TIME_SLEEP)

    finally:
        # Clean up the connection
        connection.close()




#client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#client.connect(ADDR)

#client.send(bytes)

#client.close()