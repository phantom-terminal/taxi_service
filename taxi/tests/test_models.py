from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelTests(TestCase):
    def test_manufacturer_str(self):
        """ Test manufacturer string representation """
        manufacturer = Manufacturer.objects.create(
            name="Ford",
            country="USA"
        )
        self.assertEqual(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        """ Test driver string representation """
        driver = get_user_model().objects.create_user(
            username="driver",
            password="drivEr12345",
            first_name="Driver1",
            last_name="Driver2"
        )
        self.assertEqual(
            str(driver), f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        """ Test car string representation """
        manufacturer = Manufacturer.objects.create(
            name="Audi",
            country="Germany")
        car = Car.objects.create(
            model="TT",
            manufacturer=manufacturer
        )

        self.assertEqual(str(car), car.model)

    def test_create_driver_with_license_number(self):
        """ Test creating a driver with a license number """
        username = "driver"
        password = "drivEr123"
        license_number = "AAA11111"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )
        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.license_number, license_number)