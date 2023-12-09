import socket
import struct
import calculator

class CalculatorServer:
    def __init__(self, port, host) -> None:
        self._calc = calculator.Calculator()
        self._calculation_functions = {
            b'Summe': lambda x: self._calc.summation(x),
            b'Produkt': lambda x: self._calc.product(x),
            b'Minimum': lambda x: self._calc.minimum(x),
            b'Maximum': lambda x: self._calc.maximum(x),
        }
        self.host = host
        self.port = port
        self.socket = None
        
    def start(self):
        # Start the server
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        
        self.socket.listen(1)
        print(f'Listening on port {self.port}')
        conn, addr = self.socket.accept() # Accept a connection
        print(f'Connection from {addr}')
        
        while True:
            data = conn.recv(1024).decode('utf-8')
            print(f'Received data: {data}')
            result = self.calculate(data)
            conn.send(str(result).encode('utf-8'))
            
            
    def calculate(self, data: bytes) -> bytes:
        # ID: unsigned Int (4 bytes)
        # Operation: example -> "Summe", UTF-8 encoded
        # N: Unsigned Char (1 byte)
        # z1 ... 1N: signed Int (4 bytes)
        operation_buffer = 7 
        message_id = struct.unpack('i', data[:4])
        operation_first = struct.unpack('c', data[4:5])
        if operation_first == 'S':
            operation_buffer = 5
        operation = struct.unpack('s', data[4:operation_buffer+4])
        numbers = struct.unpack('c', data[operation_buffer+4:operation_buffer+5])
        number_list = []
        for i in range(numbers):
            number_list.append(struct.unpack('i', data[operation_buffer+5+i*4:operation_buffer+9+i*4]))
        
        calc_result = 0
        if operation in self._calculation_functions:
            calc_result = self._calculation_functions[operation](number_list)
        else:
            raise Exception(f'Unknown operation: {operation}')
        
        packed_result = struct.pack('i', message_id) + struct.pack('i', calc_result)
        return packed_result


        