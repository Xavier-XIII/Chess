from PIL import Image

# Open the image
img = Image.open("images/pieces.png")

# Define the cropping box as a tuple: (left, upper, right, lower)
# These coordinates define the rectangle to be cropped.
# 'left' and 'upper' are the top-left corner, 'right' and 'lower' are the bottom-right.

y = 333
x = 0
for col in ["black"]:
    for piece in ["king", "queen", "bishop", "knight", "rook", "pawn"]:
        crop_box = (x, y, x + 333, y + 333)
        print(crop_box)
        cropped_img = img.crop(crop_box)
        print(cropped_img)

        cropped_img.save(f"images/{col}_{piece}.png")
        x += 333
