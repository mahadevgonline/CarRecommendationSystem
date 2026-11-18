import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OnlineCarRecommendationSystem.settings')
django.setup()

from django.contrib.auth.hashers import make_password
from myapp.models import Register, Seller, Car, VehiclePart

def seed():
    print("==> Checking and seeding database...")

    # 1. Seed Accounts
    admin_user, created = Register.objects.get_or_create(
        email='admin@classicauto.com',
        defaults={
            'name': 'System Administrator',
            'phone': '9876543210',
            'password': make_password('Admin@1234'),
            'rights': 'Admin'
        }
    )
    if created:
        print("  [+] Admin created: admin@classicauto.com / Admin@1234")

    user_demo, created = Register.objects.get_or_create(
        email='user@classicauto.com',
        defaults={
            'name': 'John Doe',
            'phone': '9876543211',
            'password': make_password('User@1234'),
            'rights': 'User'
        }
    )
    if created:
        print("  [+] User created: user@classicauto.com / User@1234")

    seller_demo, created = Seller.objects.get_or_create(
        email='seller@classicauto.com',
        defaults={
            'name': 'Robert Taylor',
            'phone': '9876543212',
            'address': '456 Heritage Boulevard, Detroit, MI',
            'password': make_password('Seller@1234'),
            'rights': 'Seller'
        }
    )
    if created:
        print("  [+] Seller created: seller@classicauto.com / Seller@1234")

    # 2. Seed Cars if none exist
    if Car.objects.count() == 0:
        cars_data = [
            {
                "make": "Ford",
                "model": "Mustang Fastback GT",
                "year": 1967,
                "price": 68000,
                "category": "Muscle",
                "fuel_type": "Gasoline",
                "description": "The timeless 1967 Ford Mustang Fastback GT powered by a 390 cu in (6.4L) FE V8 engine. Featuring classic Wimbledon white with blue Le Mans stripes, dual exhaust, and immaculate black interior.",
                "engine": "6.4L V8",
                "horse_power": 320,
                "transmission": "4-Speed Manual",
                "mpg_city": "11",
                "mpg_hway": "16",
                "image": "images/mustang67.jpg"
            },
            {
                "make": "Chevrolet",
                "model": "Corvette Sting Ray Split-Window",
                "year": 1963,
                "price": 145000,
                "category": "Sports Car",
                "fuel_type": "Gasoline",
                "description": "One of the most revered collector cars in American history. The iconic 1963 split-window coupe equipped with a numbers-matching 327 cu in (5.4L) V8 and 4-speed manual gearbox.",
                "engine": "5.4L V8 L76",
                "horse_power": 360,
                "transmission": "4-Speed Manual",
                "mpg_city": "12",
                "mpg_hway": "17",
                "image": "images/corvette63.jpg"
            },
            {
                "make": "Porsche",
                "model": "911 Carrera RS 2.7",
                "year": 1973,
                "price": 280000,
                "category": "Sports Car",
                "fuel_type": "Gasoline",
                "description": "The quintessential collector 911. Lightweight homologation special featuring the iconic ducktail rear spoiler, flared wheel arches, and a screaming 2.7L air-cooled flat-six.",
                "engine": "2.7L Flat-6",
                "horse_power": 210,
                "transmission": "5-Speed Manual",
                "mpg_city": "16",
                "mpg_hway": "22",
                "image": "images/porsche911.jpg"
            },
            {
                "make": "Mercedes-Benz",
                "model": "300 SL Gullwing",
                "year": 1955,
                "price": 1250000,
                "category": "Vintage",
                "fuel_type": "Gasoline",
                "description": "Widely considered the world's first true supercar. The 300 SL Gullwing introduced mechanical direct fuel injection and iconic upward-opening doors on a tubular spaceframe chassis.",
                "engine": "3.0L Inline-6 Direct Injection",
                "horse_power": 240,
                "transmission": "4-Speed Manual",
                "mpg_city": "14",
                "mpg_hway": "19",
                "image": "images/mercedes300sl.jpg"
            },
            {
                "make": "Jaguar",
                "model": "E-Type Series 1 3.8",
                "year": 1961,
                "price": 185000,
                "category": "Vintage",
                "fuel_type": "Gasoline",
                "description": "Enzo Ferrari called it 'the most beautiful car ever made.' Triple-SU carbureted 3.8L straight-six engine with independent rear suspension and four-wheel disc brakes.",
                "engine": "3.8L Inline-6 DOHC",
                "horse_power": 265,
                "transmission": "4-Speed Manual",
                "mpg_city": "15",
                "mpg_hway": "21",
                "image": "images/jaguaretype.jpg"
            },
            {
                "make": "Dodge",
                "model": "Charger R/T 440 Magnum",
                "year": 1969,
                "price": 89000,
                "category": "Muscle",
                "fuel_type": "Gasoline",
                "description": "The quintessential high-impact muscle car with hidden headlights, coke-bottle side contours, and a ferocious 440 cu in Magnum V8 under the hood.",
                "engine": "7.2L 440 Magnum V8",
                "horse_power": 375,
                "transmission": "3-Speed TorqueFlite",
                "mpg_city": "10",
                "mpg_hway": "14",
                "image": "images/charger69.jpg"
            },
            {
                "make": "BMW",
                "model": "M4 Competition Coupe",
                "year": 2024,
                "price": 84500,
                "category": "Sports Car",
                "fuel_type": "Gasoline",
                "description": "Modern precision and twin-turbo performance. 3.0L BMW M TwinPower Turbo inline 6-cylinder developing 503 HP, M xDrive with active M differential, and carbon fiber roof.",
                "engine": "3.0L Twin-Turbo I6",
                "horse_power": 503,
                "transmission": "8-Speed M Steptronic",
                "mpg_city": "16",
                "mpg_hway": "23",
                "image": "images/bmwm4.jpg"
            },
            {
                "make": "Toyota",
                "model": "Camry XSE Hybrid",
                "year": 2024,
                "price": 34500,
                "category": "Sedan",
                "fuel_type": "Hybrid",
                "description": "The premier hybrid executive sedan blending sleek aerodynamic lines with 52 combined MPG and a tech-forward cabin featuring a 12.3-inch touchscreen and wireless CarPlay.",
                "engine": "2.5L 4-Cylinder Hybrid",
                "horse_power": 225,
                "transmission": "eCVT",
                "mpg_city": "51",
                "mpg_hway": "53",
                "image": "images/camry.jpg"
            },
            {
                "make": "Tesla",
                "model": "Model S Plaid",
                "year": 2024,
                "price": 89990,
                "category": "Electric",
                "fuel_type": "Electric",
                "description": "Hypercar acceleration with tri-motor all-wheel drive delivering 1,020 horsepower. 0-60 mph in 1.99 seconds, 359 miles of EPA range, and full self-driving capability.",
                "engine": "Tri-Motor Electric AWD",
                "horse_power": 1020,
                "transmission": "Single-Speed Fixed Gear",
                "mpg_city": "124 MPGe",
                "mpg_hway": "115 MPGe",
                "image": "images/models.jpg"
            },
            {
                "make": "Land Rover",
                "model": "Range Rover SV Autobiography",
                "year": 2024,
                "price": 142000,
                "category": "Luxury SUV",
                "fuel_type": "Gasoline",
                "description": "The pinnacle of British luxury SUV refinement. Twin-turbocharged V8 engine, active noise cancellation, executive class rear seating, and all-wheel steering.",
                "engine": "4.4L Twin-Turbo V8",
                "horse_power": 523,
                "transmission": "8-Speed Automatic",
                "mpg_city": "16",
                "mpg_hway": "23",
                "image": "images/rangerover.jpg"
            }
        ]

        for item in cars_data:
            car = Car.objects.create(**item)
            print(f"  [+] Car added: {car.year} {car.make} {car.model}")

    # 3. Seed Vehicle Parts if none exist
    if VehiclePart.objects.count() == 0:
        first_car = Car.objects.first()
        parts_data = [
            {
                "part_name": "Holley 4-Barrel 650 CFM Carburetor",
                "part_number": "HLY-0-80457S",
                "category": "Engine",
                "price": 489.99,
                "stock": 14,
                "description": "Classic gold dichromate finish with electric choke and vacuum secondaries for smooth, responsive muscle car power delivery.",
                "vehicle": first_car,
                "seller": seller_demo
            },
            {
                "part_name": "Wilwood Dynalite Front Disc Brake Conversion Kit",
                "part_number": "WIL-140-11071",
                "category": "Brakes",
                "price": 899.00,
                "stock": 8,
                "description": "4-piston forged billet aluminum calipers with 11-inch slotted rotors for modern stopping power on classic spindles.",
                "vehicle": first_car,
                "seller": seller_demo
            },
            {
                "part_name": "Moto-Lita Classic 15-inch Wood Rim Steering Wheel",
                "part_number": "ML-W15-CL",
                "category": "Interior",
                "price": 320.00,
                "stock": 12,
                "description": "Handcrafted mahogany rim with polished aluminum spokes and period-correct horn push button.",
                "vehicle": first_car,
                "seller": seller_demo
            },
            {
                "part_name": "Borla S-Type Cat-Back Stainless Exhaust System",
                "part_number": "BOR-140742",
                "category": "Exhaust",
                "price": 1240.00,
                "stock": 5,
                "description": "Aerospace-grade T-304 austenitic stainless steel with aggressive muscle sound and zero cabin drone.",
                "vehicle": first_car,
                "seller": seller_demo
            },
            {
                "part_name": "Bilstein B6 Performance Shock Absorbers (Set of 4)",
                "part_number": "BIL-B6-SET",
                "category": "Suspension",
                "price": 640.00,
                "stock": 9,
                "description": "Monotube gas-pressure dampers engineered for maximum road adhesion and spirited touring stability.",
                "vehicle": first_car,
                "seller": seller_demo
            }
        ]

        for item in parts_data:
            part = VehiclePart.objects.create(**item)
            print(f"  [+] Vehicle Part added: {part.part_name}")

    print("==> Database seeding complete!")

if __name__ == '__main__':
    seed()
