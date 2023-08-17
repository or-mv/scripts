import time
from PyRingIt import RingIT
# from PyRingIt import create_qr_image
# from PyRingIt import print_qr
from utils.record import Record
import serial
import json
from utils.config_manager import DEFAULT_CONFIG_FILE_LOCATION

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
            # att_id_prefix = 'attId='
            # if att_id_prefix in str_qr_output:
            #     att_id_start = str_qr_output.index(att_id_prefix) + len(att_id_prefix)
            #     return str_qr_output[att_id_start:].strip()
        return 0

    def handle_scan_result(self, result):
        print("Scan Result:", result)
        if self.first_scan_result is None:
            self.first_scan_result = result


# Initialize the barcode scanner
scanner = BarcodeScanner()

# Start the barcode scanning process
scanner.start_scanning()

# Initialize RingIT
rit = RingIT("video")
rit = Record(rit.ring_it_params, rit.mv_session, 25, scan=scanner.first_scan_result, ssd_session=rit.ssd_session)

# Create QR image
rit.create_qr_image(rit, "hq")

#  r = Record(video_rit.ring_it_params, video_rit.mv_session, 25)
#     video_rit.create_qr_image(r, 'hq')

# Print QR image
rit.print_qr(rit.hq_qrimage)
