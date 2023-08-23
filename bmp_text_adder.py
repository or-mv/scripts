from PIL import Image, ImageDraw, ImageFont

def add_text_to_barcode(input_path, output_path):
    # Load the barcode image
    barcode_image = Image.open(input_path)

    # Get image dimensions
    width, height = barcode_image.size

    # Increase the image height to accommodate the text and space
    new_height = height + 120  # You can adjust this value as needed
    new_image = Image.new('RGB', (width, new_height), color='white')
    new_image.paste(barcode_image, (0, 0))

    # Create a drawing context
    draw = ImageDraw.Draw(new_image)

    # Define font and text for above and below the barcode
    above_text = "SCAN TO DISPLAY HOLOGRAM"
    below_text = "Having issues? Visit Summitov.com/portal."

    # Use the default system font (often Arial)
    font_above = ImageFont.load_default()
    font_below = ImageFont.load_default()

    # Calculate text size and position
    above_text_size = draw.textsize(above_text, font=font_above)
    below_text_size = draw.textsize(below_text, font=font_below)
    above_text_position = ((width - above_text_size[0]) / 2, 10)  # Adjust Y coordinate for space above
    below_text_position = ((width - below_text_size[0]) / 2, height + 40)  # Adjust Y coordinate for space below

    # Add text above and below the barcode
    draw.text(above_text_position, above_text, font=font_above, fill="black")
    draw.text(below_text_position, below_text, font=font_below, fill="black")

    # Save the new image with text
    new_image.save(output_path)

    # Check for success and print a message
    if os.path.exists(output_path):
        print("Text added successfully. Output image saved as:", output_path)
    else:
        print("Text addition failed.")

if __name__ == "__main__":
    import os

    input_file = "C:/Users/user/Desktop/bmp/dfg.bmp"  # Replace with your input barcode image path
    output_file = "C:/Users/user/Desktop/bmp/dfg_text.bmp"  # Replace with your desired output image path
    add_text_to_barcode(input_file, output_file)
