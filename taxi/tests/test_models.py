from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car

MANUFACTURER = Manufacturer(
    name="TestName",
    country="TestCountry",
)
DRIVER = Driver(
    username="TestUsername",
    password="password",
    first_name="TestFirstName",
    last_name="TestLastName",
)

CAR = Car(
    model="TestModel",
    manufacturer=MANUFACTURER,
)


class ModelTests(TestCase):
    def test_manufacturer_str(self):
        self.assertEqual(str(MANUFACTURER), "TestName TestCountry")

    def test_driver_str(self):

        self.assertEqual(
            str(DRIVER),
            "TestUsername (TestFirstName TestLastName)"
        )

    def test_car_str(self):

        self.assertEqual(str(CAR), "TestModel")
