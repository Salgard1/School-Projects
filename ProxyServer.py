from socket import *
import sys

# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)

# Fill in start. 
tcpSerPort = 8888
tcpSerSock.bind(("", tcpSerPort))
tcpSerSock.listen(5)
# Fill in end.

while 1:
    # Start receiving data from the client
    print('Ready to serve...')
    tcpCliSock, addr = tcpSerSock.accept()
    print('Received a connection from:', addr)

    # Fill in start.
    message = tcpCliSock.recv(2048)
    if str(message, encoding='utf8') != '':
    # Fill in end.
        print(message)

        # Extract the filename from the given message
        print(message.split()[1])
        file = str(message, encoding='utf8')
        filename = file.split()[1].partition("/")[2]
        print(filename)
        fileExist = "false"
        filetouse = "/" + filename
        print(filetouse)
        try:
            # Check whether the file exist in the cache
            f = open(filetouse[1:], "rb")
            outputdata = f.readlines()
            fileExist = "true"
            # ProxyServer finds a cache hit and generates a response message
            tcpCliSock.send(bytes("HTTP/1.0 200 OK\r\n"))
            tcpCliSock.send(bytes("Content-Type:text/html\r\n"))
            # Fill in start.
            for i in range(0, len(outputdata)):
                tcpCliSock.send(outputdata[i])
            # Fill in end.
                f.close()
                print('Read from cache')
        # Error handling for file not found in cache
        except IOError:
            if fileExist == "false":
                # Create a socket on the proxy server
                c = socket(AF_INET, SOCK_STREAM)
                hostn = filename.replace("www.","",1)
                print(hostn)
                try:
                        # Connect to the socket to port 80
                        # Fill in start.
                        c.connect((hostn, 80))
                        print('Socket connected to host port 80')
                        # Fill in end.

                        # Create a temporary file on this socket and ask port 80 for the file requested by the client
                        fileobj = c.makefile('r', 0)
                        fileobj.write("GET "+"https://" + filename + "HTTP/1.0\n\n")

                        # Read the response into buffer
                        # Fill in start.
                        buff = fileobj.readlines()
                        # Fill in end.

                        # Create a new file in the cache for the requested file.
                        # Also send the response in the buffer to client socket and the corresponding file in the cache
                        tmpFile = open("./" + filename,"wb")

                        # Fill in start
                        for i in range(0, len(buff)):
                            tmpFile.write(buff[i])
                            tcpCliSock.send(buff[i])
                            tmpFile.close()
                        # Fill in end.

                except:
                        print("Illegal request")
                else:
                    # HTTP response message for file not found
                    # Fill in start.
                    print("ERROR file not found")
                    # Fill in end.

    # Close the client and the server sockets
    tcpCliSock.close()

# Fill in start
tcpSerSock.close()
# Fill in end.