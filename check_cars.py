#!/usr/bin/env python
"""Check database integrity for cars with missing images."""
import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OnlineCarRecommendationSystem.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import django
django.setup()

from myapp.models import Car

print("Checking car image integrity...")
print("=" * 60)

cars_with_issues = []
for car in Car.objects.all():
    image_exists = False
    image_path = ""
    
    try:
        if car.image and car.image.name:
            image_path = car.image.path
            image_exists = os.path.exists(image_path)
        else:
            image_path = "NO IMAGE SET"
    except Exception as e:
        image_path = f"ERROR: {e}"
    
    status = "OK" if image_exists else "MISSING"
    if not image_exists:
        cars_with_issues.append(car)
    
    print(f"ID:{car.id:3} | {car.year} {car.make} {car.model:20} | {status} | {car.image.name if car.image else 'None'}")

print("=" * 60)
print(f"Total cars: {Car.objects.count()}")
print(f"Cars with missing images: {len(cars_with_issues)}")

if cars_with_issues:
    print("\nCars needing image fix:")
    for c in cars_with_issues:
        print(f"  - ID {c.id}: {c.year} {c.make} {c.model}")
