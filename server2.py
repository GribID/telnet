import socket
import pyodbc
import time


def read_code():
    all_data = ''
    while True:
        data = conn.recv(50)
        if data == b'\x1b':  # Нажатие ESC
            all_data = 'ESC'
            break
        elif data == b'\r':  # Нажатие ENTER
            break
        all_data = all_data + data.decode()
        conn.send(data)
        if all_data[-1] == '\r':  # Чтение штрихкода
            all_data = all_data[0:-1]
            break
    return all_data


def sql_command(sql_req):
    cnxn = pyodbc.connect('DRIVER={SQL Server};'
                          'SERVER=10.120.52.101;'
                          'DATABASE=RKV;'
                          'UID=it;'
                          'PWD=it')
    cursor = cnxn.cursor()
    cursor.execute(sql_req)
    cnxn.commit()
    cnxn.close()


if __name__ == '__main__':
    while True:
        try:
            sock = socket.socket()
            sock.bind(("", 14900))
            sock.listen(10)
            conn, addr = sock.accept()
            print('Connected IP: %s' % addr[0])
            conn.send('ВВЕДИТЕ ЛОГИН\r\n'.encode('cp1251'))
            login = read_code()
            print('Login: %s' % login)
            conn.send('\r\n'.encode('cp1251'))
            conn.send('ДЛЯ ЗАВЕРШЕНИЯ\r\nНАЖМИТЕ ESC\r\nСканируйте номера:\r\n'.encode('cp1251'))
            serial = ''
            while serial != 'ESC':
                serial = read_code()
                if serial != 'ESC':
                    print('Serial data: %s' % serial)
                    conn.send('\r\nЗаписано\r\n'.encode('cp1251'))
                    sql_command('INSERT INTO GID_Serial (s_Serial, s_Login, s_Date) VALUES (\'%s\', \'%s\', GETDATE())'
                                % (serial, login))
                else:
                    conn.send('\r\nСЕАНС ЗАВЕРШЕН\r\n'.encode('cp1251'))
            time.sleep(1)
            conn.close()
        except:
            print('Error')
