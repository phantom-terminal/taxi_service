from django.test import TestCase
from taxi.forms import DriverCreationForm, DriverUpdateForm


class FormsTests(TestCase):
    def test_driver_creation_form_with_valid_data(self):
        """ Test for the creation form is valid with valid data """
        form_data = {
            "username": "test_driver",
            "password1": "driver123",
            "password2": "driver123",
            "first_name": "First",
            "last_name": "Last",
            "license_number": "ABC12345"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_for_valid_license_in_the_update_form(self):
        """ Test for the update form is valid with valid data """
        correct_license_data = {"license_number": "ABC12345"}
        correct_form = DriverUpdateForm(data=correct_license_data)
        self.assertTrue(correct_form.is_valid())
        self.assertEqual(correct_form.cleaned_data, correct_license_data)
