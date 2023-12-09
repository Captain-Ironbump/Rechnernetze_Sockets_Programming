import socket
import login
import sys
import configparser as cp

class SMTPClient:
    def __init__(self, server, port) -> None:
        self.server = server
        self.port = port
        self.socket = None
        
    def connect(self):
        # Connect to the SMTP server
        self.socket = socket.create_connection((self.server, self.port))
        response = self.receive_response()
        if not response.startswith('220'):
            raise Exception(f'Error connecting to SMTP server: {response}')
    
    def send_command(self, command: str):
        # Send a command to the SMTP server
        self.socket.send(f'{command}\r\n'.encode('utf-8'))
        response = self.receive_response()
        return response
       
    def receive_response(self) -> bytes:
        response = b''
        while True:
            data = self.socket.recv(1024)
            if not data:
                break
            response += data
            if data.endswith(b'\r\n'):
                break
        return response.decode('utf-8')
    
    def login(self, username: str, password: str):
        # Login to the SMTP server
        login_data = login.login(username, password)
        self.send_command(f'EHLO {self.server}')
        self.send_command('AUTH LOGIN')
        self.send_command(login_data[0])
        self.send_command(login_data[1])
        
    def send_email(self, sender: str, recipient: str, subject: str, message: str):
        # Send an email to the SMTP server
        self.send_command(f'MAIL FROM: <{sender}>')
        self.send_command(f'RCPT TO: <{recipient}>')
        self.send_command('DATA')
        self.send_command(f'Subject: {subject}\r\n\r\n{message}\r\n.')
        self.send_command('QUIT')
        
    def close(self):
        # Close the connection to the SMTP server
        if self.socket:
            self.socket.close()
            

if __name__ == '__main__':
    
    if len(sys.argv) != 8:
        print('Usage: SMTPClient.py <server> <port> <username> <password> <sender> <reciever> <message.txt>')
        sys.exit(1)
    
    config = cp.ConfigParser()
    config.read(sys.argv[7])
    
    client = SMTPClient(sys.argv[1], sys.argv[2])
    client.connect()
    client.login(sys.argv[3], sys.argv[4])
    client.send_email(sys.argv[5], sys.argv[6], config['email']['subject'], config['email']['message'])
    client.close()
    
    
    