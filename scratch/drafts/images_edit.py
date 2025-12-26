#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  6 11:46:57 2025

@author: claudia
"""

from PIL import Image, ImageDraw, ImageFont

# Open the two images
img1 = Image.open("thermal_highlands.png")
img2 = Image.open("thermal_kenya.png")

# Ensure they have the same height (optional)
img1 = img1.resize((img1.width, img1.height))
img2 = img2.resize((img1.width, img1.height))

# Define text labels
label1 = "(a) "
label2 = "(b) "

# Define font
try:
    font = ImageFont.truetype("arial.ttf", 40)  # Increase size to 40
except IOError:
    # Fallback to a commonly available font in Linux systems
    try:
        font = ImageFont.truetype("LiberationSerif-Regular.ttf", 120)
    except IOError:
        print("Warning: Falling back to default font (small and unscalable)")
        font = ImageFont.load_default()


# Create draw object just to compute text size
dummy_img = Image.new("RGB", (10, 10))
draw = ImageDraw.Draw(dummy_img)

# Measure text height
bbox1 = draw.textbbox((0, 0), label1, font=font)
bbox2 = draw.textbbox((0, 0), label2, font=font)
text_height = max(bbox1[3] - bbox1[1], bbox2[3] - bbox2[1])
padding = 20

# Create a new image with extra height for labels
combined_width = img1.width + img2.width
combined_height = img1.height + text_height + padding
new_img = Image.new("RGB", (combined_width, combined_height), "white")

# Paste the images
new_img.paste(img1, (0, 0))
new_img.paste(img2, (img1.width, 0))

# Draw the text labels
draw = ImageDraw.Draw(new_img)

# Compute label widths
label1_width = bbox1[2] - bbox1[0]
label2_width = bbox2[2] - bbox2[0]

# Label positions
label1_x = img1.width // 2 - label1_width // 2
label2_x = img1.width + img2.width // 2 - label2_width // 2
label_y = img1.height + padding // 2

# Draw the labels
draw.text((label1_x, label_y), label1, fill="black", font=font)
draw.text((label2_x, label_y), label2, fill="black", font=font)

# Save and show
new_img.save("combined_figure.png")
new_img.show()