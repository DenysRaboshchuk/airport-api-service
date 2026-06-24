from django.db import models

from django.conf import settings
from rest_framework.exceptions import ValidationError


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

    class Meta:
        ordering = ('last_name',)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

class Flight(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='flights')
    airplane = models.ForeignKey(Airplane, on_delete=models.CASCADE, related_name='flights')
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    crew = models.ManyToManyField(Crew, related_name='flights')

    class Meta:
        ordering = ('departure_time',)

    def __str__(self):
        return f"Flight from {self.route.source} to {self.route.destination} at {self.departure_time}"

class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return f"Order by {self.user} on {self.created_at}"

class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='tickets')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='tickets')

    class Meta:
        unique_together = ('row', 'seat', 'flight',)

    def __str__(self):
        return f"Ticket for {self.flight} on row {self.row}, seat {self.seat}"

    def clean(self):
        airplane = self.flight.airplane
        errors = {}

        if self.row > airplane.rows:
            errors['row'] = f"Row {self.row} is invalid. Airplane has only {airplane.rows} rows."
        if self.seat > airplane.seats_in_row:
            errors['seat'] = f"Seat {self.seat} is invalid. Airplane has only {airplane.seats_in_row} seats."

        if errors:
            raise ValidationError(errors)


    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

