import socket


class HVPS:
    def __init__(self, ip: str, port: str, timeout: float = 5.0) -> None:
        self.ip = ip
        self.port = port
        self.timeout = timeout
        self.sock = None

    def connect(self) -> None:
        """Establishes a TCP connection to the HVPS"""
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(self.timeout)
            self.sock.connect((self.ip, self.port))
            print(f'Connected to HVPS at {self.ip}:{self.port}')
        except socket.error as e:
            print(f'Connection error: {e}')
            self.sock = None

    def disconnect(self) -> None:
        """Closes the socket connection"""
        if self.sock:
            self.sock.close()
            print('Disconnected from HVPS')
            self.sock = None

    def send_query(self, query: str) -> str:
        """Sends a command to the HVPS and returns the response"""
        if not self.sock:
            raise ConnectionError('Socket is not connected')

        try:
            if not query.endswith('/n'):
                query += '\n'
            self.sock.sendall(query.encode())

            response = self.sock.recv(1024)
            return response.decode().strip()
        except socket.error as e:
            raise ConnectionError(f'Socket communication error {e}')

    def set_voltage(self, voltage: float) -> str:
        """Sets the voltage of the HVPS"""
        query = f'SET_VOLTAGE {voltage}'
        response = self.send_query(query)
        print(f'Response: {response}')
        return response

    def get_voltage(self) -> str:
        "Queries the current voltage of the HVPS"
        response = self.send_query('GET_VOLTAGE')
        print(f'Current voltage: {response}')
        return response
