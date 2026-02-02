from django.test import TestCase, Client
from .models import Car

class RecommendationPageTest(TestCase):
    def setUp(self):
        self.client = Client()
        # Create test cars with diverse attributes
        self.car1 = Car.objects.create(
            make="Toyota", model="Camry", year=2020, price=20000, 
            category="Sedan", fuel_type="Gas", description="Reliable daily driver",
            engine="V6", horse_power=300, transmission="Automatic", 
            mpg_city="22", mpg_hway="30", features=[], image="img1.jpg"
        )
        self.car2 = Car.objects.create(
            make="Honda", model="Accord", year=2021, price=25000, 
            category="Sedan", fuel_type="Hybrid", description="Efficient sedan",
            engine="I4", horse_power=200, transmission="CVT", 
            mpg_city="45", mpg_hway="40", features=[], image="img2.jpg"
        )
        self.car3 = Car.objects.create(
            make="Ford", model="F-150", year=2019, price=35000, 
            category="Truck", fuel_type="Gas", description="Heavy duty truck",
            engine="V8", horse_power=400, transmission="Automatic", 
            mpg_city="15", mpg_hway="20", features=[], image="img3.jpg"
        )
        self.car4 = Car.objects.create(
            make="Tesla", model="Model 3", year=2022, price=45000, 
            category="Sedan", fuel_type="Electric", description="Electric future",
            engine="Electric", horse_power=350, transmission="Automatic", 
            mpg_city="120", mpg_hway="110", features=[], image="img4.jpg"
        )

    def test_page_loads(self):
        response = self.client.get('/recommendations/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/recommendations.html')
        # Should show all cars initially
        self.assertEqual(len(response.context['cars']), 4)

    def test_search(self):
        # Search by Make
        response = self.client.get('/recommendations/?q=Toyota')
        self.assertEqual(len(response.context['cars']), 1)
        self.assertEqual(response.context['cars'][0], self.car1)
        
        # Search by Description
        response = self.client.get('/recommendations/?q=Heavy')
        self.assertEqual(len(response.context['cars']), 1)
        self.assertEqual(response.context['cars'][0], self.car3)

    def test_filter_category(self):
        # Filter by Sedan (Should get 3: Camry, Accord, Model 3)
        response = self.client.get('/recommendations/?category=Sedan')
        self.assertEqual(len(response.context['cars']), 3)
        
        # Filter by Truck (Should get 1: F-150)
        response = self.client.get('/recommendations/?category=Truck')
        self.assertEqual(len(response.context['cars']), 1)

    def test_filter_price_range(self):
        # Price <= 25000 (Camry, Accord)
        response = self.client.get('/recommendations/?max_price=25000')
        self.assertEqual(len(response.context['cars']), 2)
        
        # Price >= 30000 (F-150, Model 3)
        response = self.client.get('/recommendations/?min_price=30000')
        self.assertEqual(len(response.context['cars']), 2)

    def test_filter_year_range(self):
        # Year >= 2021 (Accord, Model 3)
        response = self.client.get('/recommendations/?min_year=2021')
        self.assertEqual(len(response.context['cars']), 2)

    def test_sort_price(self):
        # Low to High
        response = self.client.get('/recommendations/?sort=price_low')
        cars = list(response.context['cars'])
        self.assertEqual(cars, [self.car1, self.car2, self.car3, self.car4]) # 20k, 25k, 35k, 45k
        
        # High to Low
        response = self.client.get('/recommendations/?sort=price_high')
        cars = list(response.context['cars'])
        self.assertEqual(cars, [self.car4, self.car3, self.car2, self.car1])

    def test_combined_filters(self):
        # Category=Sedan AND Price < 30000 (Camry, Accord)
        response = self.client.get('/recommendations/?category=Sedan&max_price=29999')
        self.assertEqual(len(response.context['cars']), 2)
