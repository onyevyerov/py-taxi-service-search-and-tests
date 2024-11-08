from django import forms
from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
    DriverLicenseUpdateForm,
    ManufacturerSearchForm,
    CarModelSearchForm,
    DriverUsernameSearchForm,
)


class DriverCreationFormTest(TestCase):
    def test_driver_creation_form_valid(self):
        form_data = {
            "username": "testdriver",
            "password1": "testpass123",
            "password2": "testpass123",
            "license_number": "ABC12345",
            "first_name": "Test",
            "last_name": "Driver",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class DriverLicenseUpdateFormTest(TestCase):
    def test_driver_license_update_form_valid(self):
        form_data = {"license_number": "AAA12345"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_license_update_invalid_format(self):
        form_data = {"license_number": "1234567"}
        form = DriverLicenseUpdateForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

        form_data = {"license_number": "ABC123A5"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class DriverUsernameSearchFormTest(TestCase):
    def test_driver_username_search_form_valid(self):
        form_data = {"username": "testuser"}
        form = DriverUsernameSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_username_search_empty(self):
        form_data = {"username": ""}
        form = DriverUsernameSearchForm(data=form_data)
        self.assertTrue(form.is_valid())


class ManufacturerSearchFormTest(TestCase):
    def test_manufacturer_search_form_valid(self):
        form_data = {"manufacturer": "test"}
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_manufacturer_search_empty(self):
        form_data = {"manufacturer": ""}
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())


class CarModelSearchFormTest(TestCase):
    def test_car_model_search_form_valid(self):
        form_data = {"car_model": "test"}
        form = CarModelSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_car_model_search_empty(self):
        form_data = {"car_model": ""}
        form = CarModelSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
