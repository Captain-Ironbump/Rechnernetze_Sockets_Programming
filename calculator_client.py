import socket
import struct

class CalculatorClient:
    def __init__(self, host, port) -> None:
        self.host = host
        self.port = port
        self.socket = None
        self.functions_name = {
            'Summe': 5,
            'Produkt': 7,
            'Minimum': 7,
            'Maximum': 7
        }
        
    def connect(self):
        # Connect to the server
        self.socket = socket.create_connection((self.host, self.port))
        print('Connected to server')
    
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
        self.socket.send(data)
        print('Sent data to server with value: ', data)
        response = self.socket.recv(1024)
        print(f'Response: {response}')
        result: tuple[int, int] = struct.unpack('<Ii', response)
        print(f'Result: {result}')
        return result
        
if __name__ == '__main__':
    client = CalculatorClient(host='127.0.0.1', port=50000)
    client.connect()
    client.send_calculation(operation='Summe', numbers=[1, 2, 3, 4, 5])
    client.send_calculation(operation='Produkt', numbers=[1, 2, 3, 4, 5])
    client.send_calculation(operation='Minimum', numbers=[1, 2, 3, 4, 5])
    client.send_calculation(operation='Maximum', numbers=[1, 2, 3, 4, 5])
    client.socket.close()