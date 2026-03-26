from flask import Flask, request, jsonify
import os

from utils.image_utils import extract_colors
from utils.design_logic import get_design

app = Flask(__name__)


@app.route("/")
def home():
    return "Interior Designer AI is running 🚀"


@app.route("/design", methods=["POST"])
def design():
    data = request.form

    # Handle image upload
    image = request.files.get("image")
    if image:
        os.makedirs("uploads", exist_ok=True)
        image_path = os.path.join("uploads", image.filename)
        image.save(image_path)
    else:
        image_path = None

    # Validate input
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

    # Get base design
    room_data = get_design(style, room_type)
    colors = room_data["colors"].copy()
    furniture = room_data["furniture"].copy()

    # Override colors using image
    if image_path:
        try:
            colors = extract_colors(image_path)
        except Exception as e:
            print("Image processing error:", e)

    # Budget logic
    if budget < 15000:
        furniture.append("budget decor items")
    else:
        furniture.append("premium decor pieces")

    # 👉 Reasoning engine
    reason = ""

    if image_path:
        if "white" in colors or "light grey" in colors:
            if style == "minimal":
                reason = "Your room already has neutral tones, which aligns well with minimal design."
            elif style == "modern":
                reason = "Neutral tones provide a strong base for a modern aesthetic."

        elif "beige" in colors:
            reason = "Warm tones in your room make it suitable for cozy or boho styles."

        else:
            reason = "Your room has diverse tones, allowing flexibility in design styles."
    else:
        reason = "Design is based on your selected preferences."

    # Final output
    output = {
        "style": style,
        "room_type": room_type,
        "colors": colors,
        "furniture": furniture,
        "description": description,
        "image_uploaded": image_path is not None,
        "explanation": f"{reason} Designed as a {style} {room_type} within ₹{budget} budget."
    }

    return jsonify({
        "success": True,
        "design": output
    })


if __name__ == "__main__":
    app.run(debug=True)