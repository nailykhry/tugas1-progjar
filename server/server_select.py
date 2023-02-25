import socket
import select
import os
import sys


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


def main():
    server_address = ('127.0.0.1', 9009)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(server_address)
    server_socket.listen(5)

    inputs = [server_socket]
    outputs = []

    try:
        while True:
            readable, writable, exceptional = select.select(
                inputs, outputs, inputs)

            for sock in readable:
                if sock.fileno() == -1:
                    inputs.remove(sock)
                elif sock is server_socket:
                    conn, addr = sock.accept()
                    inputs.append(conn)
                else:
                    command = sock.recv(1024)
                    command = command.decode()
                    if command:
                        if include_word('download', command):
                            file_name = command[command.find(
                                'download ')+len('download '):]

                            if check_file(file_name):
                                file_size = os.path.getsize(file_name)
                                header = f'file-name: {file_name},\nfile-size: {file_size},\n\n\n'.encode(
                                )
                                sock.send(header)
                                send_file(sock, file_name)
                                sock.close()
                                inputs.remove(sock)
                                print('SUCCESS SENDING FILE...')

                            else:
                                header = 'FILE DOES NOT EXIST'.encode()
                                sock.send(header)
                                sock.close()
                                inputs.remove(sock)
                                print('FILE DOES NOT EXIST...')

                        else:
                            header = 'COMMAND NOT FOUND'.encode()
                            sock.send(header)
                            sock.close()
                            inputs.remove(sock)
                            print('COMMAND NOT FOUND...')

            for sock in exceptional:
                inputs.remove(sock)
                if sock in outputs:
                    outputs.remove(sock)
                sock.close()

    except KeyboardInterrupt:
        server_socket.close()
        sys.exit(0)


if __name__ == '__main__':
    main()
