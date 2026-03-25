from flask import Flask, request, jsonify
import os
from PIL import Image
import numpy as np

app = Flask(__name__)

# 👉 Extract dominant colors from image
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

@app.route("/")
def home():
    return "Interior Designer AI is running 🚀"


@app.route("/design", methods=["POST"])
def design():
    data = request.form  # for file uploads

    # Handle image upload
    image = request.files.get("image")
    if image:
        os.makedirs("uploads", exist_ok=True)
        image_path = os.path.join("uploads", image.filename)
        image.save(image_path)
    else:
        image_path = None

    # Required fields
    required_fields = ["room_type", "budget", "style"]

    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({
                "success": False,
                "error": f"Missing field: {field}"
            }), 400

    room_type = data["room_type"]
    budget = int(data["budget"])
    style = data["style"].lower()
    description = data.get("description", "")

    # 👉 Knowledge base
    design_knowledge = {
        "minimal": {
            "bedroom": {
                "colors": ["white", "beige", "light grey"],
                "furniture": ["simple bed", "compact wardrobe", "floating shelves"]
            },
            "living_room": {
                "colors": ["white", "soft grey", "cream"],
                "furniture": ["minimal sofa", "coffee table", "TV unit"]
            }
        },
        "modern": {
            "bedroom": {
                "colors": ["grey", "black", "white"],
                "furniture": ["platform bed", "LED lighting", "side tables"]
            },
            "living_room": {
                "colors": ["black", "white", "metallic"],
                "furniture": ["modern sofa", "glass table", "TV panel"]
            }
        },
        "boho": {
            "bedroom": {
                "colors": ["earthy brown", "mustard", "olive green"],
                "furniture": ["low bed", "macrame decor", "plants"]
            },
            "living_room": {
                "colors": ["terracotta", "beige", "green"],
                "furniture": ["rattan sofa", "floor cushions", "woven decor"]
            }
        }
    }

    # Default fallback
    default_design = {
        "colors": ["cream", "brown"],
        "furniture": ["standard bed", "wooden table"]
    }

    # Get style + room data
    style_data = design_knowledge.get(style, {})
    room_data = style_data.get(room_type, default_design)

    colors = room_data["colors"].copy()
    furniture = room_data["furniture"].copy()

    # 👉 Override colors using image if available
    if image_path:
        try:
            image_colors = extract_colors(image_path)
            colors = image_colors
        except Exception as e:
            print("Image processing error:", e)

    # Budget logic
    if budget < 15000:
        furniture.append("budget decor items")
    else:
        furniture.append("premium decor pieces")

    output = {
        "style": style,
        "room_type": room_type,
        "colors": colors,
        "furniture": furniture,
        "description": description,
        "image_uploaded": image_path is not None,
        "explanation": f"A {style} {room_type} optimized for a budget of ₹{budget}"
    }

    return jsonify({
        "success": True,
        "design": output
    })


if __name__ == "__main__":
    app.run(debug=True)