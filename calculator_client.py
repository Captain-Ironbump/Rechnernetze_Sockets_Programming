import socket
import struct

class CalculatorClient:
    def __init__(self, host, port) -> None:
        self.host = host
        self.port = port
        self.socket = None
        
    def connect(self):
        # Connect to the server
        self.socket = socket.create_connection((self.host, self.port))
        print('Connected to server')
    
    def send_calculation(self, operation: str, numbers: [int]):
        # Send a calculation to the server
        # ID: unsigned Int (4 bytes)
        # Operation: example -> "Summe", UTF-8 encoded
        # N: Unsigned Char (1 byte)
        # z1 ... 1N: signed Int (4 bytes)
        data: bytes = struct.pack('i', 1) + struct.pack('s', operation) + struct.pack('c', len(numbers))
        for number in numbers:
            data += struct.pack('i', number)
        self.socket.send(data)
        print('Sent data')
        response = self.socket.recv(1024).decode('utf-8')
        print(f'Response: {response}')
        
if __name__ == '__main__':
    client = CalculatorClient(host='127.0.0.1', port=50000)
    client.connect()
    client.send_calculation(operation='Summe', numbers=[1, 2, 3, 4, 5])
    client.send_calculation(operation='Produkt', numbers=[1, 2, 3, 4, 5])
    client.send_calculation(operation='Minimum', numbers=[1, 2, 3, 4, 5])
    client.send_calculation(operation='Maximum', numbers=[1, 2, 3, 4, 5])
    client.socket.close()