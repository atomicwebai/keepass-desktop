from pathlib import Path
from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parent
SCALE = 4
SIZE = 512
CANVAS_SIZE = SIZE * SCALE

# Geometry constants (at 1x scale, multiplied by SCALE at render time)
PADDING = 32
BADGE_RADIUS = 76
BADGE_INNER = 480

# Lock geometry
LOCK_TOP = 91
LOCK_BOTTOM = 286
LOCK_LEFT = 166
LOCK_RIGHT = 346
LOCK_STROKE = 25

SHACKLE_LEFT_X = 191
SHACKLE_RIGHT_X = 321
SHACKLE_TOP = 188
SHACKLE_BOTTOM = 224

BODY_LEFT = 119
BODY_RIGHT = 393
BODY_TOP = 207
BODY_BOTTOM = 393
BODY_RADIUS = 28

KEYHOLE_CX = 256
KEYHOLE_CY = 276
KEYHOLE_R = 11

KEYHOLE_STEM_LEFT = 252
KEYHOLE_STEM_RIGHT = 260
KEYHOLE_STEM_TOP = 279
KEYHOLE_STEM_BOTTOM = 324
KEYHOLE_STEM_RADIUS = 4

# Colors
BLUE_TOP = (56, 189, 248)
BLUE_BOTTOM = (2, 132, 199)
BLUE_SOLID = (2, 132, 199, 255)
WHITE = (255, 255, 255, 255)


canvas = Image.new("RGBA", (CANVAS_SIZE, CANVAS_SIZE), (0, 0, 0, 0))
draw = ImageDraw.Draw(canvas)


def scaled_box(box):
    return tuple(round(value * SCALE) for value in box)


def draw_vertical_gradient(draw, x0, y0, x1, y1, top_color, bottom_color):
    """Draw a vertical gradient using a single rectangle with interpolated colors."""
    height = y1 - y0
    for y in range(height):
        progress = y / height
        color = tuple(round(a + (b - a) * progress) for a, b in zip(top_color, bottom_color))
        draw.line((x0, y0 + y, x1, y0 + y), fill=color)


# Match the blue app badge and closed white lock used in the header.
draw_vertical_gradient(
    draw,
    PADDING * SCALE,
    PADDING * SCALE,
    BADGE_INNER * SCALE,
    BADGE_INNER * SCALE,
    BLUE_TOP,
    BLUE_BOTTOM
)

mask = Image.new("L", canvas.size, 0)
ImageDraw.Draw(mask).rounded_rectangle(scaled_box((PADDING, PADDING, BADGE_INNER, BADGE_INNER)), radius=BADGE_RADIUS * SCALE, fill=255)
canvas.putalpha(mask)

draw = ImageDraw.Draw(canvas)
draw.arc(scaled_box((LOCK_LEFT, LOCK_TOP, LOCK_RIGHT, LOCK_BOTTOM)), start=180, end=360, fill=WHITE, width=LOCK_STROKE * SCALE)
draw.line(scaled_box((SHACKLE_LEFT_X, SHACKLE_TOP, SHACKLE_LEFT_X, SHACKLE_BOTTOM)), fill=WHITE, width=LOCK_STROKE * SCALE)
draw.line(scaled_box((SHACKLE_RIGHT_X, SHACKLE_TOP, SHACKLE_RIGHT_X, SHACKLE_BOTTOM)), fill=WHITE, width=LOCK_STROKE * SCALE)
draw.rounded_rectangle(scaled_box((BODY_LEFT, BODY_TOP, BODY_RIGHT, BODY_BOTTOM)), radius=BODY_RADIUS * SCALE, fill=WHITE)
draw.ellipse(scaled_box((KEYHOLE_CX - KEYHOLE_R, KEYHOLE_CY - KEYHOLE_R, KEYHOLE_CX + KEYHOLE_R, KEYHOLE_CY + KEYHOLE_R)), fill=BLUE_SOLID)
draw.rounded_rectangle(scaled_box((KEYHOLE_STEM_LEFT, KEYHOLE_STEM_TOP, KEYHOLE_STEM_RIGHT, KEYHOLE_STEM_BOTTOM)), radius=KEYHOLE_STEM_RADIUS * SCALE, fill=BLUE_SOLID)

icon = canvas.resize((SIZE, SIZE), Image.Resampling.LANCZOS)
icon.save(ROOT / "icon.png")

sizes = (16, 32, 48, 64, 128, 256, 512)
for size in sizes:
    icon.resize((size, size), Image.Resampling.LANCZOS).save(ROOT / "icons" / f"{size}x{size}.png")
icon.save(ROOT / "icon.ico", sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
