from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

def add_text_to_image(input_image_path, output_image_path, above_text, below_text, below_text_size=12):
    # Open an Image
    img = Image.open(input_image_path)

    # Calculate the text dimensions and the new image dimensions
    original_width, original_height = img.size
    font_above = ImageFont.truetype("arial.ttf", 16, encoding="unic")
    font_below = ImageFont.truetype("arial.ttf", below_text_size, encoding="unic")

    above_text_width, above_text_height = font_above.getsize(above_text)
    below_text_width, below_text_height = font_below.getsize(below_text)

    new_width = original_width + 80  # Increase width by 80 pixels
    new_height = original_height + 80 + above_text_height + below_text_height  # Include space for text

    # Create a new image with the calculated width and height
    new_img = Image.new("RGB", (new_width, new_height), color=(255, 255, 255))

    # Paste the original image in the center of the new image
    new_img.paste(img, ((new_width - original_width) // 2, (new_height - original_height) // 2))

    # Call draw Method to add 2D graphics in the new image
    draw = ImageDraw.Draw(new_img)

    # Custom font styles and sizes
    font_above = ImageFont.truetype("arial.ttf", 16, encoding="unic")
    font_below = ImageFont.truetype("arial.ttf", below_text_size, encoding="unic")

    # Add above text to the image
    draw.text(((new_width - above_text_width) // 2, 10), above_text, font=font_above, fill='black')

    # Add below text to the image
    draw.text(((new_width - below_text_width) // 2, new_height - below_text_height - 10), below_text, font=font_below, fill='black')

    # Save the edited image
    new_img.save(output_image_path)

    # Display edited image
    new_img.show()

    # Return the path of the saved image
    return output_image_path

# Define input and output paths
input_image_path = r"C:\Users\user\Desktop\bmp\dfg.bmp"
output_image_path = r"C:\Users\user\Desktop\bmp\dfg_text.png"

# Texts to add above and below the image
above_text = "SCAN TO DISPLAY HOLOGRAM"
below_text = "Having issues? Visit Summitov.com/portal."

# Add text above and below the image and get the path of the saved image
saved_image_path = add_text_to_image(input_image_path, output_image_path, above_text, below_text)

# Print the path of the saved image for the user
print("Image saved at:", saved_image_path)
