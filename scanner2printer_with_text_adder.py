import re
import os
import time
import json
import serial

from PIL import Image, ImageDraw, ImageFont
import sys
sys.path.append(r".")
from PyRingIt import RingIT  # noqa
from utils.record import Record  # noqa
from utils.config_manager import DEFAULT_CONFIG_FILE_LOCATION  # noqa


with open(DEFAULT_CONFIG_FILE_LOCATION, "r") as config_file:
    config_data = json.load(config_file)
port, baudrate, prefix = config_data["devices"]["qr_scanner"]["port"], config_data["devices"]["qr_scanner"]["baudrate"], \
                          config_data["devices"]["qr_scanner"]["prefix"]

class BarcodeScanner:
    def __init__(self):
        self.ser = serial.Serial(timeout=0.01)
        self.first_scan_result = None

    def start_scanning(self):
        if self.init_ser() != 0:
            print("Couldn't open serial port due to an error")
            self.ser.close()
            return

        while True:  # Continue scanning until the valid QR code is found
            self.first_scan_result = None  # Reset the previous result
            print("Scanning for barcodes...")
            while self.first_scan_result is None:
                ret_val = self.listen_to_port()
                if isinstance(ret_val, str):
                    self.handle_scan_result(ret_val)
                elif ret_val in [-1, -2]:
                    print("Invalid QR code" if ret_val == -1 else "Serial port read exception")
                time.sleep(0.1)

            print("Scan Finished")

            # Ask the user if they want to scan again
            choice = input("Scan again (y/n)? ").lower()
            if choice != 'y':
                break

        self.ser.close()

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

def add_text_to_image(input_image_path, output_image_path, above_text, below_text, below_text_size=12):
    img = Image.open(input_image_path)
    width, height = img.size

    # Create a new image with additional space for text
    new_width, new_height = width + 80, height + 80 + 2 * below_text_size
    new_img = Image.new("RGB", (new_width, new_height), color=(255, 255, 255))

    # Paste the original image in the center of the new image
    new_img.paste(img, ((new_width - width) // 2, (new_height - height) // 2))

    draw = ImageDraw.Draw(new_img)
    font_above = ImageFont.truetype("arial.ttf", 16, encoding="unic")
    font_below = ImageFont.truetype("arial.ttf", below_text_size, encoding="unic")

    # Add above text to the image
    above_text_width, above_text_height = draw.textsize(above_text, font=font_above)
    draw.text(((new_width - above_text_width) // 2, 10), above_text, font=font_above, fill='black')

    # Add below text to the image
    below_text_width, below_text_height = draw.textsize(below_text, font=font_below)
    draw.text(((new_width - below_text_width) // 2, new_height - below_text_height - 10), below_text, font=font_below,
              fill='black')

    # Save the edited image
    new_img.save(output_image_path)

    # Open the saved image with the default image viewer on Windows
    try:
        os.startfile(output_image_path)
    except Exception as e:
        print(f"Error opening image: {e}")

    return output_image_path

def main_menu():
    rit = RingIT("video")
    scanner = BarcodeScanner()

    while True:
        print("\033[4mGenerate and print QR code:\033[0m")
        print("1. Scan")
        print("2. Manually input a UUID")
        print("3. Exit")
        current_uuid = ""
        choice = input("Enter your choice (1/2/3): ")

        if choice == '1':
            # Option 1: Scan and print barcode
            scanner.start_scanning()
            current_uuid = scanner.first_scan_result
        elif choice == '2':
            # Option 2: Manually input a UUID, generate a barcode, and then print it
            current_uuid = input("Enter a UUID: ")
        elif choice == '3':
            print("\n Exiting... \n")
            break
        else:
            print("Invalid choice. Please choose a valid option (1/2/3)")
            continue

        # Generate the QR image with or without text based on user choice
        try:
            print("Creating QR image...")
            record = Record(rit.ring_it_params, rit.mv_session, 25, scan=current_uuid)
            if input("Add text to the image (y/n)? ").lower() == 'y':
                above_text = "SCAN TO DISPLAY HOLOGRAM"
                below_text = "Having issues? Visit Summitov.com/portal."
                user_directory = os.path.join(r"C:\Users\PortyOne\Desktop\qr_with_text", current_uuid)
                os.makedirs(user_directory, exist_ok=True)  # Create the user's directory
                saved_image_path = os.path.join(user_directory, f"{current_uuid}.png")  # Use the current_uuid as the filename
                saved_image_path_with_text = add_text_to_image(record.qrimage, saved_image_path, above_text, below_text)
            else:
                input_path = user_directory = os.path.join(r"C:\Users\PortyOne\Desktop\qr_with_text", current_uuid)
                match = re.match(r'^"(.*)"$', input_path)
                input_image_path = match.group(1) if match else input_path
                os.makedirs(input_image_path, exist_ok=True)  # Create the user's directory
                saved_image_path = input_image_path
                print("input_image_path ", input_image_path)
                bar = rit.create_qr_image(record)
                print("\n The path to access your barcode is:", os.path.normpath(saved_image_path) + "\n")
                ret = rit.print_qr(record.qrimage)
                if ret != 0:
                    raise ValueError("Couldn't print, check file path")
        except Exception as e:
            print(e)

                    # Generate the QR image without specifying quality
        # try:
        #     print("Creating QR image...")
        #     record = Record(rit.ring_it_params, rit.mv_session, 25, scan=current_uuid)
        #     rit.create_qr_image(record)
        #     print("\n The path to access your barcode is:", os.path.normpath(record.qrimage) + "\n")

        #     ret = rit.print_qr(record.qrimage)
        #     if ret != 0:
        #         raise ValueError("Couldn't print, check file path")
        # except Exception as e:
        #     print(e)

        # print("QR image printed successfully!")
# ---------------------------------------------------------------------------
        
    # input_path = input("Enter the input image path: ")

    # match = re.match(r'^"(.*)"$', input_path)
    # input_image_path = match.group(1) if match else input_path
    # output_image_path = input_image_path[:-4] + "_text.png"

    # above_text = "SCAN TO DISPLAY HOLOGRAM"
    # below_text = "Having issues? Visit Summitov.com/portal."

    # saved_image_path = add_text_to_image(input_image_path, output_image_path, above_text, below_text)
    # print("Image saved at:", saved_image_path)
    # rit.print_qr(saved_image_path)



      
        #     ret = rit.print_qr(r"C:\Users\PortyOne\Desktop\qr_with_text\dfg_text.png")
        #     if ret != 0:
        #         raise ValueError("Couldn't print, check file path")
        # except Exception as e:
        #     print(e)
# ---------------------------------------------------------------------------
    



   

if __name__ == "__main__":
    main_menu()

    # If you have issues with printing - check qr_printer configuration in ring_gui_config (label size, name of printer, etc)

    #  output_image_path = os.path.normpath(self.config['system']['shared_dir'])