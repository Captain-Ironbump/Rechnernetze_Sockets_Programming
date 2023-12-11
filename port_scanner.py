import socket
from threading import Thread
import time
from multiprocessing import Value

Server_IP = '141.37.168.26'
MESSAGE = 'hello'

def scan_port(port):
    
    tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_client.settimeout(10)
    
    try:
        print('Connecting to TCP server with IP ', Server_IP, ' on Port ', port)
        #tcp_client.connect((Server_IP, port))
        result = tcp_client.connect_ex((Server_IP, port))
        
        if result == 0:
            with count_open.get_lock():
                count_open.value += 1
            print('Connection established at',time.asctime(), ' on port', port)
        elif result == 10061:
            print('Connection refused [WinEr: 10061] at',time.asctime() , ' on port', port)
        elif result == 10060:
            print('Connection timed out at',time.asctime(), " on port", port)
        elif result == 10051:
            print('Network is unreachable at',time.asctime(), " on port", port)
        else:
            print('Unknown error at',time.asctime(), " on port", port)
            print(result)
            with count_unkown.get_lock():
                count_unkown.value += 1
        
    except socket.timeout:
        print("Connection timed out at",time.asctime(), "on port", port)
    except ConnectionRefusedError:
        print('Connection refused [WinEr: 10061] at',time.asctime() , 'on port', port)
    except socket.error:
        print('Socket error at',time.asctime(), 'on port', port)
    finally:
        tcp_client.close()

if __name__ == '__main__':
    count_open = Value('i', 0)
    count_unkown = Value('i', 0)
    threads = []
    for i in range(1, 51):
        t=Thread(target=scan_port, args=(i,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print('Number of open ports:', count_open.value)
    print('Number of unknown errors:', count_unkown.value)
    
    #scan_port(7)

