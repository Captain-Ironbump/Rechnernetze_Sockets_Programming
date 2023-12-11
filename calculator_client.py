import socket
import struct
import sys

class CalculatorClient:
    def __init__(self, host, port) -> None:
        self.host = host
        self.port = port
        self.tcp_socket = None
        self.udp_socket = None
        self.functions_name = {
            'Summe': 5,
            'Produkt': 7,
            'Minimum': 7,
            'Maximum': 7
        }
        
    def connect_tcp(self):
        # Connect to the server
        self.tcp_socket = socket.create_connection((self.host, self.port))
        print('Connected to server')
        
    def create_udp(self):
        # Create a UDP socket
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print('Created UDP socket')
    
    def send_calculation(self, operation: str, numbers: [int]) -> tuple[int, int]:
        # Send a calculation to the server
        # ID: unsigned Int (4 bytes)
        # Operation: example -> "Summe", UTF-8 encoded
        # N: Unsigned Char (1 byte)
        # z1 ... 1N: signed Int (4 bytes)
        if operation not in self.functions_name:
            raise Exception(f'Unknown operation: {operation}; Operations: {self.functions_name.keys()} are allowed')
        format_string = str(self.functions_name[operation]) + 's'
        data: bytes = struct.pack('I', 1) + struct.pack(format_string, operation.encode('UTF-8')) + struct.pack('c', chr(len(numbers)).encode('utf-8'))
        for number in numbers:
            data += struct.pack('i', number)
        if self.udp_socket is not None:
            self.udp_socket.sendto(data, (self.host, self.port))
            print('Sent data to server with value: ', data)
            response, addr = self.udp_socket.recvfrom(1024)
            print(f'Response: {response}')
            result: tuple[int, int] = struct.unpack('<Ii', response)
            print(f'Result: {result}')
            return result
        elif self.tcp_socket is not None:
            self.tcp_socket.send(data)
            print('Sent data to server with value: ', data)
            response = self.tcp_socket.recv(1024)
            print(f'Response: {response}')
            result: tuple[int, int] = struct.unpack('<Ii', response)
            print(f'Result: {result}')
            return result
        
if __name__ == '__main__':
    
    if len(sys.argv) != 3:
        print(f'Usage: {sys.argv[0]} <host> <port>')
        print(f'Example: {sys.argv[0]} 127.0.0.1 50000')
        sys.exit(1)
    
    client = CalculatorClient(host=str(sys.argv[1]), port=int(sys.argv[1]))
    client.connect_tcp()
    client.send_calculation(operation='Summe', numbers=[1, 2, 3, 4, 5])
    client.send_calculation(operation='Produkt', numbers=[1, 2, 3, 4, 5])
    client.send_calculation(operation='Minimum', numbers=[1, 2, 3, 4, 5])
    client.send_calculation(operation='Maximum', numbers=[1, 2, 3, 4, 5])
    client.tcp_socket.close()
    client.tcp_socket = None
    client.create_udp()
    client.send_calculation(operation='Summe', numbers=[1, 2, 3, 4, 5])
    client.send_calculation(operation='Produkt', numbers=[1, 2, 3, 4, 5])
    client.send_calculation(operation='Minimum', numbers=[1, 2, 3, 4, 5])
    client.send_calculation(operation='Maximum', numbers=[1, 2, 3, 4, 5])
    client.udp_socket.close()
    client.udp_socket = None