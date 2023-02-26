import socket
import sys

HOST, PORT = "127.0.0.1", 9009


def receive_file(sock, file_name):
    with open(file_name, 'wb') as file:
        data = sock.recv(1024)
        while data:
            file.write(data)
            data = sock.recv(1024)


def file_exist(header):
    if(header == 'FILE DOES NOT EXIST' or header == 'COMMAND NOT FOUND'):
        return False
    return True


# Create a socket (SOCK_STREAM means a TCP socket)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Connect to server and send data
    sock.connect((HOST, PORT))

    sys.stdout.write('Enter a command: \n>> ')
    command = input()

    sock.sendall(bytes(command + "\n", "utf-8"))

    header = str(sock.recv(1024), "utf-8")
    if file_exist(header):
        file_name = header.split('file-name: ')[1].split(',')[0]
        file_size = header.split('file-size: ')[1].split(',')[0]
        receive_file(sock, file_name)
        print(
            f'File {file_name} - {file_size} bytes has been successfully downloaded...')
    else:
        print(header)
