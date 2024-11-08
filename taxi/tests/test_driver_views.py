from django.test import TestCase
from django.contrib.auth import get_user_model
from taxi.models import Driver

from django.urls import reverse

DRIVER_URL = reverse("taxi:driver-list")


class PublicDriverTest(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )

    def test_login_required(self):
        response = self.client.get(DRIVER_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_detailed_login_required(self):
        response = self.client.get(
            reverse(
                "taxi:driver-detail", args=[self.driver.id]
            )
        )
        self.assertNotEqual(response.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.force_login(self.driver)

        self.driver1 = Driver.objects.create(
            username="driver1",
            password="testpass123",
            first_name="First",
            last_name="Driver",
            license_number="ABC12345"
        )
        self.driver2 = Driver.objects.create(
            username="driver2",
            password="testpass123",
            first_name="Second",
            last_name="Driver",
            license_number="XYZ67890"
        )

    def test_retrieve_driver_list(self):
        response = self.client.get(DRIVER_URL)
        drivers = Driver.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_retrieve_drivers_details(self):
        response = self.client.get(
            reverse(
                "taxi:driver-detail", args=[self.driver.id]
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_get_context_data(self):
        response = self.client.get(DRIVER_URL, {"username": "test"})
        search_form = response.context["search_form"]
        self.assertEqual(search_form.initial["username"], "test")

    def test_get_queryset_with_search(self):
        response = self.client.get(DRIVER_URL, {"username": "test"})
        driver = Driver.objects.filter(username__icontains="test")
        self.assertEqual(list(response.context["driver_list"]), list(driver))
