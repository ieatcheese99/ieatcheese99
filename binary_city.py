import random
import math

# ============================================================
#  Binary City Skyline - SVG Generator
#  Generates a cityscape made of 0s and 1s as an SVG image
#  Perfect for GitHub profile README
# ============================================================

WIDTH = 120       # columns
HEIGHT = 45       # rows
CHAR_W = 9        # character width in SVG
CHAR_H = 14       # character height in SVG
FONT_SIZE = 12
BG_COLOR = "#0D1117"       # GitHub dark background
TEXT_COLOR = "#00FF99"     # Neon green (matching profile theme)
TEXT_COLOR_DIM = "#1a5c3a" # dimmed green variant

# Define building positions: (x_start, x_end, height)
buildings = [
    (1, 4, 8),
    (5, 8, 14),
    (9, 13, 10),
    (14, 17, 19),
    (18, 22, 25),
    (23, 27, 15),
    (28, 32, 34),
    (33, 37, 28),
    (38, 42, 38),
    (43, 47, 22),
    (48, 52, 30),
    (53, 58, 42),
    (59, 63, 26),
    (64, 68, 20),
    (69, 74, 36),
    (75, 79, 17),
    (80, 84, 29),
    (85, 89, 40),
    (90, 94, 23),
    (95, 99, 33),
    (100, 104, 18),
    (105, 109, 27),
    (110, 114, 12),
    (115, 118, 21),
]

# Add antenna/spire details on top of some buildings
antennas = [
    (20, 27),
    (35, 30),
    (40, 40),
    (55, 44),
    (71, 38),
    (87, 42),
    (97, 35),
]

# Create height map
height_map = [0] * WIDTH
for x_start, x_end, h in buildings:
    for x in range(x_start, min(x_end + 1, WIDTH)):
        height_map[x] = max(height_map[x], h)

# Add antennas (single column, extra height)
for ax, ah in antennas:
    if ax < WIDTH:
        height_map[ax] = max(height_map[ax], ah)

# Add ground wave
ground_curve = []
for x in range(WIDTH):
    curve = int(2 * math.sin(x * math.pi / WIDTH))
    ground_curve.append(curve)

# Generate grid
grid = []
for y in range(HEIGHT):
    row_from_bottom = HEIGHT - y
    row = []
    for x in range(WIDTH):
        ground = 1 + ground_curve[x]
        if row_from_bottom <= ground or row_from_bottom <= height_map[x]:
            row.append(random.choice(['0', '1']))
        else:
            row.append(' ')
    grid.append(row)

# Build SVG
svg_width = WIDTH * CHAR_W + 40
svg_height = HEIGHT * CHAR_H + 40

svg_lines = []
svg_lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{svg_width}" height="{svg_height}" viewBox="0 0 {svg_width} {svg_height}">')
svg_lines.append(f'  <rect width="100%" height="100%" fill="{BG_COLOR}" rx="12"/>')

# Add subtle glow filter
svg_lines.append('  <defs>')
svg_lines.append('    <filter id="glow">')
svg_lines.append('      <feGaussianBlur stdDeviation="1.5" result="coloredBlur"/>')
svg_lines.append('      <feMerge>')
svg_lines.append('        <feMergeNode in="coloredBlur"/>')
svg_lines.append('        <feMergeNode in="SourceGraphic"/>')
svg_lines.append('      </feMerge>')
svg_lines.append('    </filter>')
svg_lines.append('  </defs>')

svg_lines.append(f'  <g font-family="Consolas, \'Courier New\', monospace" font-size="{FONT_SIZE}" filter="url(#glow)">')

for y, row in enumerate(grid):
    for x, ch in enumerate(row):
        if ch != ' ':
            # Vary color: brighter for '1', dimmer for '0'
            if ch == '1':
                color = TEXT_COLOR
                opacity = round(random.uniform(0.7, 1.0), 2)
            else:
                color = TEXT_COLOR_DIM
                opacity = round(random.uniform(0.5, 0.9), 2)

            px = 20 + x * CHAR_W
            py = 20 + y * CHAR_H + CHAR_H
            svg_lines.append(f'    <text x="{px}" y="{py}" fill="{color}" opacity="{opacity}">{ch}</text>')

svg_lines.append('  </g>')
svg_lines.append('</svg>')

svg_content = '\n'.join(svg_lines)

with open("binary_city.svg", "w", encoding="utf-8") as f:
    f.write(svg_content)

# Also generate text version
text_lines = []
for row in grid:
    text_lines.append(''.join(row).rstrip())

with open("binary_city.txt", "w", encoding="utf-8") as f:
    f.write('\n'.join(text_lines))

print("binary_city.svg generated!")
print("binary_city.txt generated!")
print(f"SVG size: {svg_width}x{svg_height}")
print(f"Grid: {WIDTH}x{HEIGHT}")
