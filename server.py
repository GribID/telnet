import socket


def read_code():
    data = ''
    all_data = ''
    conn.send('ДЛЯ ЗАВЕРШЕНИЯ\r\nНАЖМИТЕ ESC\r\nСканируйте номера:\r\n'.encode('cp1251'))
    while data != b'\x1b':
        data = conn.recv(50)
        all_data = all_data + data.decode()
        conn.send(data)
        if all_data[-1] == '\r':
            save_base(all_data)
            all_data = ''


def save_base(number):
    if len(number) > 1:
        conn.send('\r\nЗаписано в базу\r\n'.encode('cp1251'))
        print('Записано в базу:' + number[:-1])


if __name__ == '__main__':
    while True:
        print('Server started')
        try:
            sock = socket.socket()
            sock.bind(("", 14900))
            sock.listen(10)
            conn, addr = sock.accept()
            read_code()
        except:
            print('Error')
