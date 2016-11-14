import socket
import os.path
import sys, time



#Variaveis
CODIGO = 1
RESOLUCAO = 1
ARRAY_RESOLUCAO = {"160x90_250k","320x180_500k","640x360_750k"}
BUFSIZE = 1024

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
        while True:
            data = connection.recv(BUFSIZE)
            print >>sys.stderr, 'received "%s"' % data
            if data == "true":
                i=0
                videofile = "videos/"+str(CODIGO).zfill(3)+"-640x360_750k_"+str(i).zfill(3)+".webm"
                while (os.path.exists(videofile) is True ):
                    VidFILE = open(videofile).read()
                    print videofile
                    print len(VidFILE)
                    connection.sendall(VidFILE)
                    connection.send("AAAAFFFFFFGGGGGGQQQQQQQQQ") #tag de final de arquivo
                    i = i + 1
                    videofile = "videos/"+str(CODIGO).zfill(3)+"-640x360_750k_"+str(i).zfill(3)+".webm"
                    #raw_input("Press Enter to continue...")
                    time.sleep(5)
                break
            else:
                print >>sys.stderr, 'no more data from', client_address
                break

    finally:
        # Clean up the connection
        connection.close()




#client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#client.connect(ADDR)

#client.send(bytes)

#client.close()