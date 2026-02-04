#!/usr/bin/env python
"""
Script to add placeholder images to cars that are missing them.
"""
import os
import sys
import django
from io import BytesIO

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OnlineCarRecommendationSystem.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from myapp.models import Car
from django.core.files.base import ContentFile

def create_placeholder_image(car_name):
    """Create a simple colored placeholder image."""
    try:
        from PIL import Image, ImageDraw, ImageFont
        import random
        
        # Random background color
        color = (random.randint(50, 200), random.randint(50, 200), random.randint(50, 200))
        img = Image.new('RGB', (800, 600), color=color)
        
        # Add text
        d = ImageDraw.Draw(img)
        try:
            # Try to use a basic font
            font = ImageFont.load_default()
            # If possible scale it up (PIL default font is tiny)
        except:
            pass
            
        # Draw text in center (approximate centering for default font)
        d.text((400, 300), car_name, fill=(255, 255, 255), anchor="mm")
        
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        return ContentFile(buffer.getvalue(), name=f"{car_name.replace(' ', '_').lower()}.png")
    except ImportError:
        print("PIL not installed, using minimal fallback image")
        # Minimal 1x1 PNG blue pixel
        png_data = bytes([
            0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A, 0x00, 0x00, 0x00, 0x0D,
            0x49, 0x48, 0x44, 0x52, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01,
            0x08, 0x02, 0x00, 0x00, 0x00, 0x90, 0x77, 0x53, 0xDE, 0x00, 0x00, 0x00,
            0x0C, 0x49, 0x44, 0x41, 0x54, 0x08, 0xD7, 0x63, 0xF8, 0xCF, 0x00, 0x00,
            0x02, 0x01, 0x01, 0x00, 0x43, 0x96, 0x50, 0x05, 0x00, 0x00, 0x00, 0x00,
            0x49, 0x45, 0x4E, 0x44, 0xAE, 0x42, 0x60, 0x82
        ])
        return ContentFile(png_data, name=f"{car_name.replace(' ', '_').lower()}.png")

def fix_images():
    cars = Car.objects.all()
    count = 0
    for car in cars:
        has_image = False
        try:
            if car.image and car.image.name and os.path.exists(car.image.path):
                has_image = True
        except:
            pass
            
        if not has_image:
            print(f"Adding image for: {car.year} {car.make} {car.model}")
            car_name = f"{car.make} {car.model}"
            car.image = create_placeholder_image(car_name)
            car.save()
            count += 1
            
    print(f"\nFixed {count} cars with missing images.")

if __name__ == "__main__":
    fix_images()
