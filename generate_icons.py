#!/usr/bin/env python3
"""
Generate PWA icons for NeverForget
This script creates placeholder icons in various sizes required for PWA
"""

try:
    from PIL import Image, ImageDraw, ImageFont
    import os
except ImportError:
    print("Pillow is required. Install it with: pip install Pillow")
    exit(1)

def create_icon(size, filename):
    """Create a simple icon with the given size"""
    # Create a new image with a gradient background
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Create gradient background
    for y in range(size):
        # Gradient from purple to blue
        r = int(99 + (y / size) * 56)  # 99 to 155
        g = int(110 + (y / size) * 46)  # 110 to 156
        b = int(241 + (y / size) * 14)  # 241 to 255
        draw.line([(0, y), (size, y)], fill=(r, g, b, 255))
    
    # Add a simple birthday cake icon
    # Cake base
    cake_width = int(size * 0.6)
    cake_height = int(size * 0.3)
    cake_x = (size - cake_width) // 2
    cake_y = size - cake_height - int(size * 0.2)
    
    # Cake layers
    draw.rectangle([cake_x, cake_y, cake_x + cake_width, cake_y + cake_height], 
                   fill=(255, 255, 255, 200), outline=(200, 200, 200, 255), width=max(1, int(size * 0.01)))
    
    # Cake top layer
    top_height = int(cake_height * 0.4)
    top_margin = max(2, int(size * 0.02))  # Ensure minimum margin
    draw.rectangle([cake_x + top_margin, cake_y - top_height, cake_x + cake_width - top_margin, cake_y], 
                   fill=(255, 182, 193, 200), outline=(200, 150, 160, 255), width=max(1, int(size * 0.01)))
    
    # Candles
    candle_width = max(1, int(size * 0.02))
    candle_height = int(size * 0.15)
    candle_spacing = max(1, cake_width // 4)
    
    for i in range(3):
        candle_x = cake_x + candle_spacing + (i * candle_spacing)
        candle_y = cake_y - top_height - candle_height
        
        # Candle
        draw.rectangle([candle_x, candle_y, candle_x + candle_width, candle_y + candle_height], 
                       fill=(255, 255, 0, 255))
        
        # Flame
        flame_size = max(2, int(size * 0.03))
        flame_points = [
            (candle_x + candle_width//2, candle_y - flame_size),
            (candle_x, candle_y),
            (candle_x + candle_width, candle_y)
        ]
        draw.polygon(flame_points, fill=(255, 165, 0, 255))
    
    # Save the icon
    icons_dir = "static/icons"
    os.makedirs(icons_dir, exist_ok=True)
    img.save(os.path.join(icons_dir, filename), "PNG")
    print(f"Created {filename} ({size}x{size})")

def main():
    """Generate all required PWA icons"""
    icon_sizes = [
        (16, "icon-16x16.png"),
        (32, "icon-32x32.png"),
        (72, "icon-72x72.png"),
        (96, "icon-96x96.png"),
        (128, "icon-128x128.png"),
        (144, "icon-144x144.png"),
        (152, "icon-152x152.png"),
        (192, "icon-192x192.png"),
        (384, "icon-384x384.png"),
        (512, "icon-512x512.png"),
    ]
    
    print("Generating PWA icons for NeverForget...")
    
    for size, filename in icon_sizes:
        create_icon(size, filename)
    
    print("\nAll icons generated successfully!")
    print("Icons saved in: static/icons/")
    print("\nNote: These are placeholder icons. Consider replacing them with professional designs.")

if __name__ == "__main__":
    main() 