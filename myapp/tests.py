from django.test import TestCase, Client
from .models import Car

class SimilarCarsTest(TestCase):
    def setUp(self):
        self.client = Client()
        # Create test cars
        self.car1 = Car.objects.create(
            make="Toyota", model="Camry", year=2020, price=20000, 
            category="Sedan", fuel_type="Gas", description="A reliable sedan.",
            engine="V6", horse_power=300, transmission="Automatic", 
            mpg_city="22", mpg_hway="30", features=["Bluetooth"], image="test.jpg"
        )
        self.car2 = Car.objects.create(
            make="Honda", model="Accord", year=2021, price=22000, 
            category="Sedan", fuel_type="Gas", description="Another reliable sedan.",
            engine="I4", horse_power=190, transmission="CVT", 
            mpg_city="30", mpg_hway="38", features=["Backup Camera"], image="test2.jpg"
        )
        self.car3 = Car.objects.create(
            make="Ford", model="F-150", year=2021, price=35000, 
            category="Truck", fuel_type="Gas", description="A tough truck.",
            engine="V8", horse_power=400, transmission="Automatic", 
            mpg_city="15", mpg_hway="20", features=["Towing Package"], image="test3.jpg"
        )

    def test_similar_cars_logic(self):
        response = self.client.get(f'/car-detail/{self.car1.id}/')
        self.assertEqual(response.status_code, 200)
        
        similar_cars = response.context['similar_cars']
        
        # Should include car2 (Same category: Sedan)
        self.assertIn(self.car2, similar_cars)
        
        # Should NOT include car3 (Different category: Truck)
        self.assertNotIn(self.car3, similar_cars)
        
        # Should NOT include car1 (Self)
        self.assertNotIn(self.car1, similar_cars)
        
    def test_similar_cars_limit(self):
        # Create more sedans
        for i in range(5):
             Car.objects.create(
                make=f"Sedan{i}", model="Test", year=2022, price=20000, 
                category="Sedan", fuel_type="Gas", description="Test",
                engine="V6", horse_power=200, transmission="Auto", 
                mpg_city="20", mpg_hway="30", features=[], image="test.jpg"
            )
            
        response = self.client.get(f'/car-detail/{self.car1.id}/')
        similar_cars = response.context['similar_cars']
        
        # Limit is 4
        self.assertLessEqual(len(similar_cars), 4)
