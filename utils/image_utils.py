from PIL import Image
import numpy as np



def extract_colors(image_path, k=3):
    image = Image.open(image_path)
    image = image.resize((100, 100))  # resize for speed
    pixels = np.array(image).reshape(-1, 3)

    # Get unique colors and their frequency
    unique, counts = np.unique(pixels, axis=0, return_counts=True)
    dominant = unique[counts.argsort()[-k:]]

    colors = []
    for color in dominant:
        colors.append(rgb_to_name(color))

    # Remove duplicates while preserving order
    unique_colors = []
    for c in colors:
        if c not in unique_colors:
            unique_colors.append(c)

    return unique_colors

def rgb_to_name(rgb):
    r, g, b = rgb

    # Simple rules (can improve later)
    if r > 240 and g > 240 and b > 240:
        return "white"
    elif r > 200 and g > 200 and b > 200:
        return "light grey"
    elif r > 180 and g > 170 and b > 140:
        return "beige"
    elif r < 100 and g < 100 and b < 100:
        return "dark grey"
    elif r > g and r > b:
        return "warm tone"
    elif b > r and b > g:
        return "cool blue tone"
    else:
        return "neutral tone"