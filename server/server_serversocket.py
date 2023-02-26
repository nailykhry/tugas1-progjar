import socketserver
import os


def send_file(conn, file_name):
    with open(file_name, 'rb') as f:
        data = f.read(1024)
        while data:
            conn.send(data)
            data = f.read(1024)


def include_word(word, string):
    if word in string:
        return True
    return False


def check_file(path):
    if os.path.exists(path):
        return True
    return False


def substring_after(s, delim):
    return s.partition(delim)[2]


class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()

        command = self.data.decode()
        if command:
            if include_word('download', command):
                file_name = command[command.find(
                    'download ')+len('download '):]

                if check_file(file_name):
                    file_size = os.path.getsize(file_name)
                    header = f'file-name: {file_name},\nfile-size: {file_size},\n\n\n'.encode()
                    self.request.sendall(header)
                    send_file(self.request, file_name)
                    print('SUCCESS SENDING FILE...')

                else:
                    header = 'FILE DOES NOT EXIST'.encode()
                    self.request.sendall(header)
                    print('FILE DOES NOT EXIST...')

            else:
                header = 'COMMAND NOT FOUND'.encode()
                self.request.sendall(header)
                print('COMMAND NOT FOUND...')


if __name__ == "__main__":
    HOST, PORT = "192.168.1.21", 9999

    # Create the server, binding to 127.0.0.1 on port 9009
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
