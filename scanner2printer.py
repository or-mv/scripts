import time
from PyRingIt import RingIT
from utils.record import Record
import serial
import json
from utils.config_manager import DEFAULT_CONFIG_FILE_LOCATION
import os

with open(DEFAULT_CONFIG_FILE_LOCATION, "r") as config_file:
    config_data = json.load(config_file)
port, baudrate, prefix  = config_data["devices"]["qr_scanner"]["port"], config_data["devices"]["qr_scanner"]["baudrate"], config_data["devices"]["qr_scanner"]["prefix"]


class BarcodeScanner:
    def __init__(self):
        self.ser = serial.Serial(timeout=0.01)
        self.first_scan_result = None

    def start_scanning(self):
        if self.init_ser() != 0:
            print("Couldn't open serial port due to an error")
            self.ser.close()
            return

        print("Scanning for barcodes...")
        while self.first_scan_result is None:
            ret_val = self.listen_to_port()
            if isinstance(ret_val, str):
                self.handle_scan_result(ret_val)
            elif ret_val in [-1, -2]:
                print("Invalid QR code" if ret_val == -1 else "Serial port read exception")
            time.sleep(0.1)
        self.ser.close()
        print("Scan Finished")

    def init_ser(self):
        self.ser.close()
        self.ser.port, self.ser.baudrate = port, int(baudrate)
        try:
            self.ser.open()
        except Exception as e:
            print(f"Couldn't open serial port due to an error {e}")
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
            full_str_qr_output = qr_output.decode('utf-8')
            str_qr_output = full_str_qr_output.replace(prefix, "")
            return str_qr_output
        return 0

    def handle_scan_result(self, result):
        print("Scan Result:", result)
        if self.first_scan_result is None:
            self.first_scan_result = result


def main_menu():
    rit = RingIT("video")
    scanner = BarcodeScanner()
    # quality = 'hq'  # change as needed

    while True:
        print("\033[4mGenerate and print QR code:\033[0m")
        print("1. Scan")
        print("2. Manually input a UUID")
        print("3. Exit")

        choice = input("Enter your choice (1/2/3): ")
        if choice == '1':
            # Option 1: Scan and print barcode
            scanner.start_scanning()
            r = Record(rit.ring_it_params, rit.mv_session, 25, scan=scanner.first_scan_result)
        elif choice == '2':
            # Option 2: Manually input a UUID, generate a barcode, and then print it
            uuid_input = input("Enter a UUID: ")
            r = Record(rit.ring_it_params, rit.mv_session, 25, scan=uuid_input)
        elif choice == '3':
            print("\n Exiting... \n")
            break
        else:
            print("Invalid choice. Please choose a valid option (1/2/3)")
            continue

        # Generate the QR image without specifying quality 
        barcode = rit.create_clean_qr_image(r)
        print("Creating QR image...")
        rit.print_qr(barcode)
        print("\n The path to access your barcode is:", os.path.normpath(r.hq_qrimage) + "\n")


if __name__ == "__main__":
    main_menu()
