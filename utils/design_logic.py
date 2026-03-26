def get_design(style, room_type):
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

    default_design = {
        "colors": ["cream", "brown"],
        "furniture": ["standard bed", "wooden table"]
    }

    style_data = design_knowledge.get(style, {})
    return style_data.get(room_type, default_design)