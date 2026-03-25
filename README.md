# Interior Designer AI 🏡

An intelligent backend system that generates interior design recommendations using both user input and image analysis.

---

## 🚀 Features

- ✅ Style-based recommendations (minimal, modern, boho)
- ✅ Room-specific suggestions (bedroom, living room)
- ✅ Budget-aware furniture planning
- ✅ Image upload support
- ✅ Dominant color extraction from room images
- ✅ Human-friendly color interpretation

---

## 🧠 How It Works

1. User provides:
   - Room type
   - Budget
   - Style
   - Optional image

2. System:
   - Uses rule-based knowledge engine
   - Extracts dominant colors from uploaded image
   - Converts raw RGB → meaningful color names

3. Outputs:
   - 🎨 Color palette
   - 🪑 Furniture suggestions
   - 💡 Explanation

---

## 🛠 Tech Stack

- Python
- Flask
- NumPy
- Pillow (Image Processing)

---

## 📡 API Usage

### Endpoint:
POST /design

### Example Request:
```bash
curl -X POST http://127.0.0.1:5000/design \
-F "room_type=bedroom" \
-F "budget=20000" \
-F "style=minimal" \
-F "image=@room.jpg"