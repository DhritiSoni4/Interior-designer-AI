from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Interior Designer AI is running 🚀"

@app.route("/design", methods=["POST"])
def design():
    data = request.get_json()

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
    # 👉 Knowledge base (data-driven system)
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

    # Get style data
    style_data = design_knowledge.get(style, {})
    room_data = style_data.get(room_type, default_design)

    colors = room_data["colors"].copy()
    furniture = room_data["furniture"].copy()

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
    "explanation": f"A {style} {room_type} optimized for a budget of ₹{budget}"
}

    return jsonify({
        "success": True,
        "design": output
    })


if __name__ == "__main__":
    app.run(debug=True)