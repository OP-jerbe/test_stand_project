import threading
import time
from datetime import datetime

class DataAcquisition:
    def __init__(self, rf_generator, interval=0.5):
        """
        Initialize the DataAcquisition class.

        :param rf_generator: An instance of the RFGenerator class (or similar device).
        :param interval: Time interval (in seconds) between data fetches.
        """
        self.rf_generator = rf_generator
        self.interval = interval
        self.running = False

        # Store the latest fetched values
        self.forward_power = 0.0
        self.reflected_power = 0.0
        self.absorbed_power = 0.0
        self.frequency = 0.0

        # Background thread for fetching data
        self.thread = None

    def start(self):
        """
        Start the data acquisition process.
        """
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._run)
            self.thread.start()

    def stop(self):
        """
        Stop the data acquisition process.
        """
        self.running = False
        if self.thread is not None:
            self.thread.join()

    def _run(self):
        """
        Run the data acquisition loop in the background.
        """
        while self.running:
            self._fetch_data()
            time.sleep(self.interval)

    def _fetch_data(self):
        """
        Fetch data from the RF generator and update the internal state.
        """
        if not self.rf_generator:
            return

        try:
            self.forward_power = self.rf_generator.get_forward_power()
            self.reflected_power = self.rf_generator.get_refl_power()
            self.absorbed_power = self.forward_power - self.refl_power
            self.frequency = self.rf_generator.get_frequency()

        except Exception as e:
            print(f"Error while fetching data: {e}")

    def get_data(self):
        """
        Get the latest fetched data.

        :return: A dictionary containing forward power, reflected power, absorbed power, and frequency.
        """
        # Capture the current timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return {
            'timestamp': current_time,
            "forward_power": self.forward_power,
            "reflected_power": self.reflected_power,
            "absorbed_power": self.absorbed_power,
            "frequency": self.frequency
        }
