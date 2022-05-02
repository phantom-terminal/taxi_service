from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from taxi.models import Driver, Manufacturer, Car

CARS_LIST_URL = reverse("taxi:car-list")
CAR_CREATE_URL = reverse("taxi:car-create")
DRIVER_LIST_URL = reverse("taxi:driver-list")
DRIVER_CREATE_URL = reverse("taxi:driver-create")
MANUFACTURERS_LIST_URL = reverse("taxi:manufacturer-list")
MANUFACTURER_CREATE_URL = reverse("taxi:manufacturer-create")


class PublicDriverTests(TestCase):
    def test_login_not_required(self):
        response = self.client.get(DRIVER_LIST_URL)
        self.assertEqual(response.status_code, 200)


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "driver",
            "drivEr123"
        )
        self.client.force_login(self.user)

    def test_retrieve_driver(self):
        response = self.client.get(DRIVER_LIST_URL)
        drivers = Driver.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["driver_list"]), list(drivers))
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_create_driver(self):
        form_data = {
            "username": "test_driver",
            "password1": "drivEr123",
            "password2": "drivEr123",
            "first_name": "First",
            "last_name": "Last",
            "license_number": "ABC12345"
        }

        self.client.post(DRIVER_CREATE_URL, data=form_data)

        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])


class PublicManufacturerTests(TestCase):
    def test_login_not_required(self):
        response = self.client.get(MANUFACTURERS_LIST_URL)

        self.assertEqual(response.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="driver",
            password="driver123"
        )

        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(name="Nissan", country="Japan")
        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="Honda", country="Japan")

        response = self.client.get(MANUFACTURERS_LIST_URL)
        manufacturers = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_create_manufacturer(self):
        form_data = {"name": "Audi", "country": "Germany"}

        self.client.post(MANUFACTURER_CREATE_URL, data=form_data)
        new_manufacturer = Manufacturer.objects.get(name=form_data["name"])

        self.assertEqual(new_manufacturer.name, form_data["name"])
        self.assertEqual(new_manufacturer.country, form_data["country"])

    def test_delete_manufacturer(self):
        new_manufacturer = Manufacturer.objects.create(
            name="Ford",
            country="USA"
        )
        self.client.post(reverse(
            "taxi:manufacturer-delete",
            kwargs={"pk": new_manufacturer.id}
        )
        )
        self.assertEqual(Manufacturer.objects.count(), 0)

    def test_update_manufacturer(self):
        new_manufacturer = Manufacturer.objects.create(
            name="Auudi",
            country="Germani"
        )
        update_data = {"name": "Audi", "country": "Germany"}
        self.client.post(reverse("taxi:manufacturer-update",
                                 kwargs={"pk": new_manufacturer.id}),
                         data=update_data
                         )
        manufacturer = Manufacturer.objects.get(pk=new_manufacturer.id)
        self.assertEqual(manufacturer.name, update_data["name"])
        self.assertEqual(manufacturer.country, update_data["country"])


class PublicCarTests(TestCase):
    def test_login_required(self):
        response = self.client.get(CARS_LIST_URL)
        self.assertEqual(response.status_code, 200)


class PrivateCarTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="testtest12"
        )

        self.client.force_login(self.user)

    def test_retrieve_car(self):
        manufacturer1 = Manufacturer.objects.create(
            name="Audi",
            country="Germany"
        )
        manufacturer2 = Manufacturer.objects.create(
            name="Chery",
            country="China"
        )
        Car.objects.create(model="TT", manufacturer=manufacturer1)
        Car.objects.create(model="Amulet", manufacturer=manufacturer2)
        response = self.client.get(CARS_LIST_URL)
        cars = Car.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["car_list"]), list(cars))
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_delete_car(self):
        manufacturer = Manufacturer.objects.create(
            name="Ford",
            country="USA"
        )
        car = Car.objects.create(
            model="Focus",
            manufacturer=manufacturer
        )
        self.assertEqual(Car.objects.count(), 1)
        self.client.post(reverse("taxi:car-delete", kwargs={"pk": car.id}))
        self.assertEqual(Car.objects.count(), 0)
