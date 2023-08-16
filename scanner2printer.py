import time
import serial
import json
from utils.config_manager import DEFAULT_CONFIG_FILE_LOCATION


config_path = DEFAULT_CONFIG_FILE_LOCATION
with open(config_path, "r") as config_file:
    config_data = json.load(config_file)

# Extract port and baudrate values from the ring_gui_config.json
port = config_data["devices"]["qr_scanner"]["port"]
baudrate = config_data["devices"]["qr_scanner"]["baudrate"]


class BarcodeScanner:
    def __init__(self):
        self.ser = serial.Serial(timeout=0.01)
        self.url_prefix = 'DFHF-SFGD-SEHJ-'  # Adjust as needed
        self.first_scan_result = None

    def start_scanning(self):
        if self.init_ser() != 0:
            print("Couldn't open serial port because of an error")
            self.ser.close()
            return

        print("Scanning for barcodes...")

        while self.first_scan_result is None:
            ret_val = self.listen_to_port()

            if isinstance(ret_val, str):
                self.handle_scan_result(ret_val)
            elif ret_val == -1:
                print("Invalid QR code")
            elif ret_val == -2:
                print("Serial port read exception")

            time.sleep(0.1)

        self.ser.close()
        print("Scan Finished")

    def init_ser(self):
        if self.ser.is_open:
            self.ser.close()

        # Set serial port and baudrate here ---- HARD CODED! -----
        self.ser.port = port
        self.ser.baudrate = int(baudrate)
        self.ser.port = port

        try:
            self.ser.open()
        except Exception as e:
            print(f"Couldn't open serial port because of an error {e}")
            return 1

        return 0

    def listen_to_port(self):
        try:
            qr_output = self.ser.readline()
        except Exception as e:
            print(f"QR scanner read exception {e}")
            qr_output = b''
            self.ser.close()
            return -2

        if len(qr_output) > 1:
            str_qr_output = qr_output.decode('utf-8')
            print("Decoded data:", str_qr_output)

            att_id_prefix = 'attId='
            if att_id_prefix in str_qr_output:
                att_id_start = str_qr_output.index(att_id_prefix) + len(att_id_prefix)
                att_id = str_qr_output[att_id_start:].strip()
                return att_id

        return 0

    def handle_scan_result(self, result):
        print("Scan Result:", result)
        if self.first_scan_result is None:
            self.first_scan_result = result
            # print("First Scan Result:", self.first_scan_result)


scanner = BarcodeScanner()
scanner.start_scanning()
