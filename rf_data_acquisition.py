import traceback # Used for printing stack traces in case of exceptions.
import threading # Used to run the data acquisition process in a separate thread
import time # Used to introduce delays between data fetches.
from datetime import datetime # Used to capture timestamps for the data.

class DataAcquisition:
    def __init__(self, rf_generator, interval: float=1) -> None:
        """
        Initialize the DataAcquisition class.

        :param rf_generator: An instance of the RFGenerator class (or similar device).
        :param interval: Time interval (in seconds) between data fetches.
        """
        self.rf_generator = rf_generator
        self.interval: float = interval
        self.running: bool = False

        # Store the latest fetched values
        self.timestamp: datetime = datetime.now()
        self.forward_power: float = 0.0
        self.refl_power: float = 0.0
        self.absorbed_power: float = 0.0
        self.frequency: float = 0.0

        # Background thread for fetching data
        self.thread = None

    def start(self) -> None:
        """
        Start the data acquisition process.
        """
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._run)
            self.thread.start()
            self.rf_generator.ping_device()

    def stop(self) -> None:
        """
        Stop the data acquisition process.
        """
        self.running = False
        if self.thread is not None:
            self.thread.join()

    def _run(self) -> None:
        """
        Run the data acquisition loop in the background.
        """
        while self.running:
            self._fetch_data()
            time.sleep(self.interval)

    def _fetch_data(self) -> None:
        """
        Fetch data from the RF generator and update the internal state.
        """
        if not self.rf_generator:
            return

        try:
            self.timestamp = datetime.now()
            self.forward_power = self.rf_generator.get_forward_power()
            self.reflected_power = self.rf_generator.get_refl_power()
            self.absorbed_power = self.rf_generator.get_absorbed_power()
            self.frequency = self.rf_generator.get_frequency()

        except Exception as e:
            traceback.print_exc()
            print(f'\nError while fetching data: {e}\n')

    def get_data(self) -> dict:
        """
        Get the latest fetched data.

        :return: A dictionary containing a timestamp, forward power, reflected power, absorbed power, and frequency.
        """

        return {
            'time': self.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'forward_power': self.forward_power,
            'reflected_power': self.reflected_power,
            'absorbed_power': self.absorbed_power,
            'frequency': self.frequency
        }
