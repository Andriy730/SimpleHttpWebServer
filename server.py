import socket

from datetime import datetime
from threading import Thread


class WebServer:

    def __init__(self, port=8080):
        self.port = port
        self.content_dir = 'public' # directory that contains webpages and files

    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('', self.port))
        self.socket.listen(5)
        print('-'*40)
        print("Start server")
        print('-'*40)
        self.work()

    def shutdown(self):
        """Shuts down the server"""

        try:
            print("Shutting down server")
            self.socket.shutdown(socket.SHUT_RDWR)

        except Exception as e:
            pass

    def work(self):
        """Listen on server port for request and start new thread to make response for client"""

        while True:
            client, address = self.socket.accept()
            client.settimeout(90)
            print("Connection with " + str(address))
            Thread(target=self.handle_client, args=(client, address)).start()

    def handle_client(self, client, address):
        """Main loop for handling connection with client and serving client's request"""
        while True:
            message = client.recv(1024)
            if not message:
                client.close()
                break
            message = message.decode()
            method = message.split()[0]
            print("message:")
            print(message)

            if method == "GET" or method == "HEAD":
                filename = message.split()[1]
                if filename == "/":
                    filename = "/index.html"
                path_to_file = self.content_dir + filename
                try:
                    with open(path_to_file, 'rb') as f:
                        response_data = f.readlines()
                    print("200 OK")
                    headers = self.generate_response_headers(200, filename.split('.')[1])
            
                except IOError:
                    response_data = '<html><body><center><h1>Error 404: File not found</h1></center></body></html>'.encode()
                    headers = self.generate_response_headers(404)
                    print("404 Not Found")
            
                response = headers.encode()
                client.send(response)
                if method == "GET":
                    if not isinstance(response_data, list):
                        client.send(response_data)
                    else:
                        for line in response_data:
                            client.send(line)

                client.close()
                break

            else:
                print("Method Not Allowed")

    def generate_response_headers(self, response_code, file_type="html"):
        """Generates HTTP headers for response"""

        if response_code == 200:
            header = "HTTP/1.1 200 OK\n"
        elif response_code == 404:
            header = "HTTP/1.1 404 Not Found\n"
        
        if file_type == "html":
            content_type = "text/html"
        elif file_type == "jpg":
            content_type = "image/jpg"
        elif file_type == "jpeg":
            content_type = "image/jpeg"
        elif file_type == "gif":
            content_type = "image/gif"
        elif file_type == "js":
            content_type = "application/javascript"
        elif file_type == "css":
            content_type = "text/css"
        else:
            content_type = "text/html"
        
        date = datetime.now().strftime("%a, %d %b %Y %H:%M:%S")
        header += "Date: " + date + "\n"
        header += "Server: Simple-Http-server\n"
        header += "Content-Type: " + content_type + "\n"
        header += "Connection: close\n\n"

        return header
