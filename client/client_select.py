import socket
import sys


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


def main():
    server_address = ('127.0.0.1', 9009)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(server_address)

    sys.stdout.write('Enter a command: \n>> ')
    command = input()

    client_socket.send(command.encode())

    try:
        header = client_socket.recv(1024).decode()
        if file_exist(header):
            file_name = header.split('file-name: ')[1].split(',')[0]
            file_size = header.split('file-size: ')[1].split(',')[0]
            receive_file(client_socket, file_name)
            print(
                f'File {file_name} - {file_size} bytes has been successfully downloaded...')
        else:
            print(header)

        client_socket.close()
    except KeyboardInterrupt:
        client_socket.close()
        sys.exit(0)


if __name__ == '__main__':
    main()
