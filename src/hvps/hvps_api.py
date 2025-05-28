import socket


class HVPS:
    def __init__(self, ip: str, port: str, timeout: float = 5.0) -> None:
        self.ip = ip
        self.port = port
        self.timeout = timeout
        self.sock = None
        self._channels = ('BM', 'EX', 'L1', 'L2', 'L3', 'L4', 'SL')

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

    def set_solenoid_current(self, current: str) -> str | None:
        """Sets the solenoid current. Max current is 3.0 A"""
        num = float(current)
        current = f'{num:.2f}'
        command = f'STSLT00{current}'
        response = self.send_query(command)
        print(f'Solenoid current set to: {response}')

    def set_voltage(self, channel: str, voltage: str) -> str:
        """Sets the voltage of the specified channel in the HVPS"""
        if channel not in self._channels:
            raise ValueError(
                f'"{channel}" is not a valid channel. Valid channels: {self._channels}'
            )
        command_prefix = f'ST{channel}T'

        if '-' in voltage:
            sign = '-'
            voltage = voltage.replace('-', '')
        else:
            sign = '+'
            voltage = voltage.replace('+', '')

        voltage = voltage.zfill(5)

        command = f'{command_prefix}{sign}{voltage}'
        response = self.send_query(command)
        print(f'Response: {response}')
        return response

    def get_voltage(self, channel: str) -> str:
        "Queries the current voltage of a channel in the HVPS"
        if channel not in self._channels:
            raise ValueError(
                f'"{channel}" is not a valid channel. Valid channels: {self._channels}'
            )
        command = f'RD{channel}V'
        response = self.send_query(command)
        print(f'Current {channel} voltage: {response}')
        return response

    def get_current(self, channel: str) -> str:
        "Queries the current electric-current of a channel in the HVPS"
        if channel not in self._channels:
            raise ValueError(
                f'"{channel}" is not a valid channel. Valid channels: {self._channels}'
            )
        command = f'RD{channel}C'
        response = self.send_query(command)
        print(f'Current {channel} current: {response}')
        return response
