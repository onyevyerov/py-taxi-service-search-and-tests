from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer

CAR_LIST_URL = reverse("taxi:car-list")


class PublicCarTest(TestCase):
    def test_login_required(self):
        response = self.client.get(CAR_LIST_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.force_login(self.user)
        self.manufacturer1 = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        self.car1 = Car.objects.create(
            model="Boomer",
            manufacturer=self.manufacturer2
        )
        self.car2 = Car.objects.create(
            model="Supra",
            manufacturer=self.manufacturer1
        )

    def test_retrieve_car_list(self):
        response = self.client.get(CAR_LIST_URL)
        self.assertEqual(response.status_code, 200)

        cars = Car.objects.all()
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )

        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_get_context_data(self):
        response = self.client.get(CAR_LIST_URL, {"model": "Supra"})
        search_form = response.context["search_form"]
        self.assertEqual(search_form.initial["model"], "Supra")

    def test_get_queryset_with_search(self):
        response = self.client.get(CAR_LIST_URL, {"model": "Boomer"})
        car = Car.objects.filter(model__icontains="Boomer")
        self.assertEqual(
            list(response.context["car_list"]),
            list(car)
        )
