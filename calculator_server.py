import socket
import struct
import calculator

class CalculatorServer:
    def __init__(self, host, port) -> None:
        self._calc = calculator.Calculator()
        self._calculation_functions = {
            'Summe': lambda x: self._calc.summation(x),
            'Produkt': lambda x: self._calc.product(x),
            'Minimum': lambda x: self._calc.minimum(x),
            'Maximum': lambda x: self._calc.maximum(x),
        }
        self.functions_name = {
            'Summe': 5,
            'Produkt': 7,
            'Minimum': 7,
            'Maximum': 7
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
        
        while True:
            conn, addr = self.socket.accept()  # Accept a connection
            print(f'Connection from {addr}')

            # Handle the connection in a separate function
            self.handle_connection(conn)

    def handle_connection(self, conn: socket.socket):
        try:
            while True:
                data = conn.recv(1024)
                print(f'Received data: {data}')
                if not data:
                    break
                result = self.calculate(data)
                conn.send(result)
        except Exception as e:
            print(f"Error handling connection: {e}")
        finally:
            conn.close()
        

    def calculate(self, data: bytes) -> bytes:
        # ID: unsigned Int (4 bytes)
        # Operation: example -> "Summe", UTF-8 encoded
        # N: Unsigned Char (1 byte)
        # z1 ... 1N: signed Int (4 bytes)

        operation = data.decode('utf-8')
        # Define a set of valid characters
        valid_chars = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789")
        # Use a loop to filter out unwanted characters
        operation = ''.join(char for char in operation if char in valid_chars)
        print(f'Operation: {operation}')
        if operation not in self.functions_name:
            raise Exception(f'Unknown operation: {operation}; Operations: {self.functions_name.keys()} are allowed')

        message_id = struct.unpack('I', data[:4])[0]
        number = struct.unpack('c', data[self.functions_name[operation]+4:self.functions_name[operation]+5])
        number = struct.unpack('B', number[0])[0]
        number_list = []
        print(number)
        for index in range(number):
            number_list.append(struct.unpack('i', data[self.functions_name[operation]+5+index*4:self.functions_name[operation]+9+index*4])[0])

        calc_result = 0
        if operation in self._calculation_functions:
            calc_result = self._calculation_functions[operation](number_list)
        else:
            raise Exception(f'Unknown operation: {operation}')

        packed_result = struct.pack('I', message_id) + struct.pack('i', calc_result)
        return packed_result

if __name__ == '__main__':
    server = CalculatorServer(host='127.0.0.1', port=50000)
    server.start()

