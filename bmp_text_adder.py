from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

def add_text_to_image(input_image_path, output_image_path, above_text, below_text, below_text_size=12):
    # Open an Image
    img = Image.open(input_image_path)

    # Calculate the new width and height to accommodate the additional text
    original_width, original_height = img.size
    new_width = original_width + 80  # Increase width by 80 pixels
    new_height = original_height + 80  # Increase height by 80 pixels

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
    text_width, text_height = draw.textsize(above_text, font=font_above)
    draw.text(((new_width - text_width) // 2, 7), above_text, font=font_above, fill='black')

    # Add below text to the image
    text_width, text_height = draw.textsize(below_text, font=font_below)
    draw.text(((new_width - text_width) // 2, new_height - text_height - 10), below_text, font=font_below, fill='black')

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

# Add text above and below the image with smaller below text and get the path of the saved image
saved_image_path = add_text_to_image(input_image_path, output_image_path, above_text, below_text, below_text_size=10)

# Print the path of the saved image for the user
print("Image saved at:", saved_image_path)
