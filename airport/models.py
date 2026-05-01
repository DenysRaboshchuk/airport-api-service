from django.db import models

from django.conf import settings


# Create your models here.
class AirplaneType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Airplane(models.Model):
    name = models.CharField(max_length=255)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()
    airplane_type = models.ForeignKey(AirplaneType, on_delete=models.CASCADE, related_name='airplanes')

    def __str__(self):
        return f"Airplane: {self.name}"

class Airport(models.Model):
    name = models.CharField(max_length=255)
    closest_big_city = models.CharField(max_length=255)

    def __str__(self):
        return f"Airport: {self.name} ({self.closest_big_city})"

class Route(models.Model):
    source = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='outgoing_routes')
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='incoming_routes')
    distance = models.IntegerField()

    def __str__(self):
        return f"Route from {self.source} to {self.destination}. Distance: {self.distance} km"

class Crew(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Flight(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='flights')
    airplane = models.ForeignKey(Airplane, on_delete=models.CASCADE, related_name='flights')
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    crew = models.ManyToManyField(Crew, related_name='flights')

    def __str__(self):
        return f"Flight from {self.route.source} to {self.route.destination} at {self.departure_time}"

class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')

    def __str__(self):
        return f"Order by {self.user} on {self.created_at}"

class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='tickets')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='tickets')

    def __str__(self):
        return f"Ticket for {self.flight} on row {self.row}, seat {self.seat}"