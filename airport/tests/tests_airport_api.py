from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from airport.models import (
    Airport,
    AirplaneType,
    Airplane,
    Route,
    Flight,
    Order,
    Ticket, Crew,
)

ORDER_LIST_URL = reverse("airport:order-list")
ORDER_DETAIL_URL = reverse("airport:order-detail", args=[1])
AIRPLANE_LIST_URL = reverse("airport:airplane-list")
FLIGHT_LIST_URL = reverse("airport:flight-list")


def create_airport(name="Test Airport", city="Test City"):
    return Airport.objects.create(name=name, closest_big_city=city)


def create_crew(first_name = "TestName", last_name = "TestLastName"):
    return Crew.objects.create(first_name=first_name, last_name=last_name)

def create_airplane_type(name="Boeing 77777"):
    return AirplaneType.objects.create(name=name)


def create_airplane(name="TEST-Airplane", rows=30, seats_in_row=5, airplane_type=None):
    if airplane_type is None:
        airplane_type = create_airplane_type()
    return Airplane.objects.create(
        name=name, rows=rows, seats_in_row=seats_in_row, airplane_type=airplane_type
    )


def create_route(source=None, destination=None, distance=500):
    if source is None:
        source = create_airport(name="Source Airport", city="Source City")
    if destination is None:
        destination = create_airport(name="Destination Airport", city="Dest City")
    return Route.objects.create(source=source, destination=destination, distance=distance)


def create_flight(route=None, airplane=None):
    if route is None:
        route = create_route()
    if airplane is None:
        airplane = create_airplane()
    return Flight.objects.create(
        route=route,
        airplane=airplane,
        departure_time="2026-06-01T08:00:00Z",
        arrival_time="2026-06-01T09:30:00Z",
    )


def create_order(user, flight=None):
    if flight is None:
        flight = create_flight()
    order = Order.objects.create(user=user)
    Ticket.objects.create(row=1, seat=1, flight=flight, order=order)
    return order


# ============================================================
# Unauthenticated tests
# ============================================================

class UnauthenticatedOrderTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required_for_order_list(self):
        response = self.client.get(ORDER_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_auth_required_for_order_detail(self):
        response = self.client.get(ORDER_DETAIL_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_auth_required_for_order_create(self):
        response = self.client.post(ORDER_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_auth_required_for_order_update(self):
        response = self.client.put(ORDER_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_auth_required_for_order_delete(self):
        response = self.client.delete(ORDER_DETAIL_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UnauthenticatedFlightTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_unauthenticated_can_view_flights(self):
        response = self.client.get(FLIGHT_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated_cannot_create_flight(self):
        response = self.client.post(FLIGHT_LIST_URL, {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


# ============================================================
# Authenticated user tests
# ============================================================

class AuthenticatedOrderTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.test", password="testpassword"
        )
        self.client.force_authenticate(self.user)

    def test_get_auth_user_order_list(self):
        response = self.client.get(ORDER_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_sees_only_own_orders(self):
        other_user = get_user_model().objects.create_user(
            email="other@test.test", password="testpassword"
        )
        create_order(user=self.user)
        create_order(user=other_user)

        response = self.client.get(ORDER_LIST_URL)
        self.assertEqual(len(response.data["results"]), 1)

    def test_create_order_with_tickets(self):
        flight = create_flight()
        payload = {
            "tickets": [
                {"row": 5, "seat": 3, "flight": flight.id}
            ]
        }
        response = self.client.post(ORDER_LIST_URL, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.filter(user=self.user).count(), 1)

    def test_create_order_assigns_current_user(self):
        flight = create_flight()
        payload = {
            "tickets": [
                {"row": 5, "seat": 3, "flight": flight.id}
            ]
        }
        self.client.post(ORDER_LIST_URL, payload, format="json")
        order = Order.objects.get(user=self.user)
        self.assertEqual(order.user, self.user)

    def test_ticket_unique_together_validation(self):
        flight = create_flight()
        order = create_order(user=self.user, flight=flight)
        taken_ticket = order.tickets.first()

        payload = {
            "tickets": [
                {"row": taken_ticket.row, "seat": taken_ticket.seat, "flight": flight.id}
            ]
        }
        response = self.client.post(ORDER_LIST_URL, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_ticket_row_validation(self):
        flight = create_flight()
        payload = {
            "tickets": [
                {"row": 999, "seat": 1, "flight": flight.id}
            ]
        }
        response = self.client.post(ORDER_LIST_URL, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_ticket_seat_validation(self):
        flight = create_flight()
        payload = {
            "tickets": [
                {"row": 1, "seat": 999, "flight": flight.id}
            ]
        }
        response = self.client.post(ORDER_LIST_URL, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# ============================================================
# Admin tests
# ============================================================

class AdminFlightTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = get_user_model().objects.create_user(
            email="admin@test.test", password="adminpassword", is_staff=True
        )
        self.client.force_authenticate(self.admin)

    def test_admin_can_create_flight(self):
        route = create_route()
        airplane = create_airplane()
        crew = create_crew()
        payload = {
            "route": route.id,
            "airplane": airplane.id,
            "departure_time": "2024-07-01T10:00:00Z",
            "arrival_time": "2024-07-01T12:00:00Z",
            "crew": [crew.id],
        }
        response = self.client.post(FLIGHT_LIST_URL, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_can_delete_flight(self):
        flight = create_flight()
        url = reverse("airport:flight-detail", args=[flight.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class NonAdminFlightTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="user@test.test", password="userpassword"
        )
        self.client.force_authenticate(self.user)

    def test_non_admin_cannot_create_flight(self):
        route = create_route()
        airplane = create_airplane()
        payload = {
            "route": route.id,
            "airplane": airplane.id,
            "departure_time": "2024-07-01T10:00:00Z",
            "arrival_time": "2024-07-01T12:00:00Z",
            "crew": [],
        }
        response = self.client.post(FLIGHT_LIST_URL, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_non_admin_cannot_delete_flight(self):
        flight = create_flight()
        url = reverse("airport:flight-detail", args=[flight.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)