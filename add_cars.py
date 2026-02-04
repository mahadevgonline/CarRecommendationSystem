#!/usr/bin/env python
"""
Django script to add 10 sample cars to the database.
Run with: python manage.py shell < add_cars.py
Or: python add_cars.py (after setting up Django environment)
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OnlineCarRecommendationSystem.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from myapp.models import Car
from django.core.files.base import ContentFile
import urllib.request

# Sample car data - 10 diverse vehicles
CARS_DATA = [
    {
        "make": "Ford",
        "model": "Mustang GT",
        "year": 2024,
        "price": 55000,
        "category": "Sports Car",
        "fuel_type": "Gasoline",
        "description": "The iconic Ford Mustang GT delivers exhilarating performance with its 5.0L Ti-VCT V8 engine producing 480 horsepower. This American muscle car combines classic styling with modern technology, featuring a 12-inch digital instrument cluster and SYNC 4 infotainment system.",
        "engine": "5.0L Ti-VCT V8",
        "horse_power": 480,
        "transmission": "10-Speed Automatic",
        "mpg_city": "15",
        "mpg_hway": "24",
        "features": ["Premium Audio", "Leather Seats", "Apple CarPlay", "Android Auto", "Brembo Brakes", "Launch Control"]
    },
    {
        "make": "Toyota",
        "model": "Camry XSE",
        "year": 2024,
        "price": 32000,
        "category": "Sedan",
        "fuel_type": "Hybrid",
        "description": "The Toyota Camry XSE Hybrid combines fuel efficiency with sporty aesthetics. With a combined 208 horsepower from its hybrid powertrain, it offers exceptional fuel economy without sacrificing performance. Features include a panoramic sunroof and JBL premium audio.",
        "engine": "2.5L 4-Cylinder Hybrid",
        "horse_power": 208,
        "transmission": "CVT",
        "mpg_city": "51",
        "mpg_hway": "53",
        "features": ["Hybrid Technology", "Panoramic Sunroof", "JBL Audio", "Wireless Charging", "Blind Spot Monitor", "Adaptive Cruise Control"]
    },
    {
        "make": "BMW",
        "model": "M4 Competition",
        "year": 2024,
        "price": 84000,
        "category": "Sports Car",
        "fuel_type": "Gasoline",
        "description": "The BMW M4 Competition is a high-performance coupe featuring a twin-turbo 3.0L inline-6 engine. With 503 horsepower and M-specific tuning, it delivers thrilling acceleration and precise handling. Carbon fiber components reduce weight for enhanced agility.",
        "engine": "3.0L Twin-Turbo Inline-6",
        "horse_power": 503,
        "transmission": "8-Speed M Steptronic",
        "mpg_city": "16",
        "mpg_hway": "23",
        "features": ["M Carbon Bucket Seats", "Head-Up Display", "Harman Kardon Audio", "M Drive Professional", "Carbon Roof", "Launch Control"]
    },
    {
        "make": "Tesla",
        "model": "Model 3 Performance",
        "year": 2024,
        "price": 52000,
        "category": "Electric",
        "fuel_type": "Electric",
        "description": "The Tesla Model 3 Performance is an all-electric sports sedan with dual motor all-wheel drive. It accelerates 0-60 mph in just 3.1 seconds and offers up to 315 miles of range. Features include Autopilot, full self-driving capability, and over-the-air updates.",
        "engine": "Dual Motor Electric",
        "horse_power": 455,
        "transmission": "Single-Speed Direct Drive",
        "mpg_city": "134",
        "mpg_hway": "126",
        "features": ["Autopilot", "Full Self-Driving", "Glass Roof", "Premium Audio", "Wireless Charging", "Sentry Mode"]
    },
    {
        "make": "Porsche",
        "model": "911 Carrera S",
        "year": 2024,
        "price": 128000,
        "category": "Sports Car",
        "fuel_type": "Gasoline",
        "description": "The Porsche 911 Carrera S continues the legendary 911 lineage with a 3.0L twin-turbo flat-six engine producing 443 horsepower. Rear-wheel drive and PDK transmission deliver the quintessential sports car experience with German precision engineering.",
        "engine": "3.0L Twin-Turbo Flat-6",
        "horse_power": 443,
        "transmission": "8-Speed PDK",
        "mpg_city": "18",
        "mpg_hway": "24",
        "features": ["Sport Chrono Package", "PASM Sport Suspension", "Bose Audio", "Sport Exhaust", "Porsche Active Suspension", "PCM Navigation"]
    },
    {
        "make": "Honda",
        "model": "CR-V Hybrid",
        "year": 2024,
        "price": 38000,
        "category": "SUV",
        "fuel_type": "Hybrid",
        "description": "The Honda CR-V Hybrid is a versatile compact SUV combining practicality with efficiency. Its 2.0L Atkinson-cycle hybrid system delivers 204 horsepower with excellent fuel economy. Spacious interior and Honda Sensing safety suite make it perfect for families.",
        "engine": "2.0L Atkinson-Cycle Hybrid",
        "horse_power": 204,
        "transmission": "E-CVT",
        "mpg_city": "40",
        "mpg_hway": "35",
        "features": ["Honda Sensing", "Wireless Apple CarPlay", "Heated Seats", "Power Tailgate", "Panoramic Sunroof", "AWD"]
    },
    {
        "make": "Mercedes-Benz",
        "model": "E-Class 450",
        "year": 2024,
        "price": 72000,
        "category": "Luxury Sedan",
        "fuel_type": "Gasoline",
        "description": "The Mercedes-Benz E-Class 450 exemplifies luxury and technology. Its 3.0L turbocharged inline-6 with mild hybrid technology produces 375 horsepower. MBUX infotainment with augmented reality navigation and Burmester audio create an unparalleled driving experience.",
        "engine": "3.0L Turbo Inline-6 Mild Hybrid",
        "horse_power": 375,
        "transmission": "9G-TRONIC Automatic",
        "mpg_city": "22",
        "mpg_hway": "30",
        "features": ["MBUX Infotainment", "Burmester 3D Audio", "Air Suspension", "Ambient Lighting", "Massage Seats", "Driver Assistance Package"]
    },
    {
        "make": "Chevrolet",
        "model": "Corvette Stingray",
        "year": 2024,
        "price": 68000,
        "category": "Sports Car",
        "fuel_type": "Gasoline",
        "description": "The mid-engine Chevrolet Corvette Stingray redefines American performance. Its 6.2L LT2 V8 engine delivers 495 horsepower through an 8-speed dual-clutch transmission. Exotic supercar performance at an accessible price with stunning looks.",
        "engine": "6.2L LT2 V8",
        "horse_power": 495,
        "transmission": "8-Speed Dual-Clutch",
        "mpg_city": "15",
        "mpg_hway": "27",
        "features": ["Performance Data Recorder", "Bose Audio", "Magnetic Ride Control", "Head-Up Display", "GT2 Bucket Seats", "Front Lift System"]
    },
    {
        "make": "Audi",
        "model": "Q7 Premium Plus",
        "year": 2024,
        "price": 65000,
        "category": "SUV",
        "fuel_type": "Gasoline",
        "description": "The Audi Q7 Premium Plus is a three-row luxury SUV with sophisticated styling and quattro all-wheel drive. Its 3.0L turbocharged V6 produces 335 horsepower. Virtual cockpit, Bang & Olufsen audio, and advanced driver assistance make every journey exceptional.",
        "engine": "3.0L Turbocharged V6",
        "horse_power": 335,
        "transmission": "8-Speed Tiptronic",
        "mpg_city": "18",
        "mpg_hway": "23",
        "features": ["Quattro AWD", "Virtual Cockpit Plus", "Bang & Olufsen 3D Audio", "Air Suspension", "Matrix LED Headlights", "Panoramic Sunroof"]
    },
    {
        "make": "Jeep",
        "model": "Wrangler Rubicon",
        "year": 2024,
        "price": 52000,
        "category": "SUV",
        "fuel_type": "Gasoline",
        "description": "The Jeep Wrangler Rubicon is the ultimate off-road SUV with legendary 4x4 capability. Its 3.6L Pentastar V6 provides 285 horsepower while Dana 44 axles and electronic locking differentials conquer any terrain. Removable top and doors offer open-air freedom.",
        "engine": "3.6L Pentastar V6",
        "horse_power": 285,
        "transmission": "8-Speed Automatic",
        "mpg_city": "17",
        "mpg_hway": "22",
        "features": ["Rock-Trac 4x4", "Dana 44 Heavy-Duty Axles", "Electronic Locking Differentials", "Removable Top", "Uconnect 5", "Trail Rated Badge"]
    }
]

def create_placeholder_image(car_name):
    """Create a simple placeholder image file."""
    # Use a colored rectangle as placeholder
    try:
        from PIL import Image
        img = Image.new('RGB', (800, 600), color=(100, 100, 100))
        from io import BytesIO
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        return ContentFile(buffer.getvalue(), name=f"{car_name.replace(' ', '_').lower()}.png")
    except ImportError:
        # If PIL not available, create minimal PNG
        # Minimal 1x1 PNG
        png_data = bytes([
            0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A, 0x00, 0x00, 0x00, 0x0D,
            0x49, 0x48, 0x44, 0x52, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01,
            0x08, 0x02, 0x00, 0x00, 0x00, 0x90, 0x77, 0x53, 0xDE, 0x00, 0x00, 0x00,
            0x0C, 0x49, 0x44, 0x41, 0x54, 0x08, 0xD7, 0x63, 0xF8, 0x0F, 0x00, 0x00,
            0x01, 0x01, 0x01, 0x00, 0x18, 0xDD, 0x8D, 0xB4, 0x00, 0x00, 0x00, 0x00,
            0x49, 0x45, 0x4E, 0x44, 0xAE, 0x42, 0x60, 0x82
        ])
        return ContentFile(png_data, name=f"{car_name.replace(' ', '_').lower()}.png")


def add_cars():
    """Add all cars to the database."""
    added_count = 0
    skipped_count = 0
    
    for car_data in CARS_DATA:
        # Check if car already exists
        existing = Car.objects.filter(
            make=car_data["make"],
            model=car_data["model"],
            year=car_data["year"]
        ).exists()
        
        if existing:
            print(f"Skipping {car_data['year']} {car_data['make']} {car_data['model']} - already exists")
            skipped_count += 1
            continue
        
        try:
            car = Car(
                make=car_data["make"],
                model=car_data["model"],
                year=car_data["year"],
                price=car_data["price"],
                category=car_data["category"],
                fuel_type=car_data["fuel_type"],
                description=car_data["description"],
                engine=car_data["engine"],
                horse_power=car_data["horse_power"],
                transmission=car_data["transmission"],
                mpg_city=car_data["mpg_city"],
                mpg_hway=car_data["mpg_hway"],
                features=car_data["features"]
            )
            
            # Create placeholder image
            image_name = f"{car_data['make']}_{car_data['model']}".replace(' ', '_').lower()
            car.image = create_placeholder_image(image_name)
            car.save()
            
            print(f"Added: {car_data['year']} {car_data['make']} {car_data['model']}")
            added_count += 1
            
        except Exception as e:
            print(f"Error adding {car_data['make']} {car_data['model']}: {e}")
    
    print(f"\n{'='*50}")
    print(f"Summary: Added {added_count} cars, Skipped {skipped_count} (already exist)")
    print(f"Total cars in database: {Car.objects.count()}")


if __name__ == "__main__":
    print("Adding 10 sample cars to the database...")
    print("="*50)
    add_cars()
