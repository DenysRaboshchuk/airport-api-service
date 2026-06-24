from rest_framework import serializers

from django.db import transaction
from airport.models import AirplaneType, Airplane, Airport, Route, Crew, Flight, Order, Ticket


class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = '__all__'

class AirplaneListSerializer(serializers.ModelSerializer):
    airplane_type_name = serializers.CharField(source='airplane_type.name', read_only=True)
    amount_of_seats = serializers.SerializerMethodField()
    class Meta:
        model = Airplane
        fields = ('id', 'name', 'amount_of_seats', 'airplane_type_name')

    def get_amount_of_seats(self, obj) -> int:
        return obj.rows * obj.seats_in_row

class AirplaneCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = ('name', 'rows', 'seats_in_row', 'airplane_type')

class AirplaneDetailSerializer(serializers.ModelSerializer):
    airplane_type = AirplaneTypeSerializer(read_only=True)
    class Meta:
        model = Airplane
        fields = ('id', 'name', 'rows', 'seats_in_row', 'airplane_type')

class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ('id', 'name', 'closest_big_city')

class RouteSerializer(serializers.ModelSerializer):
    source = serializers.SerializerMethodField()
    destination = serializers.SerializerMethodField()
    class Meta:
        model = Route
        fields = ('id', 'source', 'destination')

    def get_source(self, obj) -> str:
        return f"{obj.source.name} ({obj.source.closest_big_city})"

    def get_destination(self, obj) -> str:
        return f"{obj.destination.name} ({obj.destination.closest_big_city})"

class RouteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ('source', 'destination', 'distance')

class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = '__all__'

class FlightListSerializer(serializers.ModelSerializer):
    route = serializers.SerializerMethodField()
    airplane = serializers.CharField(source='airplane.name', read_only=True)
    crew = serializers.SlugRelatedField(many=True, read_only=True, slug_field='full_name')
    tickets_available = serializers.SerializerMethodField()
    class Meta:
        model = Flight
        fields = ('id', 'departure_time', 'arrival_time', 'route', 'airplane', 'crew', 'tickets_available',)

    def get_route(self, obj) -> str:
        return f"{obj.route.source} -> {obj.route.destination}"

    def get_tickets_available(self, obj) -> int:
        return obj.airplane.rows * obj.airplane.seats_in_row - obj.tickets.count()

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ('row', 'seat')

class TicketCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ('row', 'seat', 'flight', 'order')

class TicketCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ('row', 'seat', 'flight')

class FlightDetailSerializer(FlightListSerializer):
    bought_tickets = TicketSerializer(many=True, read_only=True, source='tickets')

    class Meta(FlightListSerializer.Meta):
        fields = FlightListSerializer.Meta.fields + ('bought_tickets',)

class FlightCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = ('route', 'departure_time', 'arrival_time', 'airplane', 'crew')

class OrderSerializer(serializers.ModelSerializer):
    tickets_count = serializers.SerializerMethodField()
    class Meta:
        model = Order
        fields = ('id', 'created_at', 'tickets_count')

    def get_tickets_count(self, obj) -> int:
        return obj.tickets.count()

class OrderDetailSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ('id', 'created_at', 'tickets')

class OrderCreateSerializer(serializers.ModelSerializer):
    tickets = TicketCreateSerializer(many=True)

    class Meta:
        model = Order
        fields = ('tickets',)

    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop('tickets')
            user = self.context['request'].user
            order = Order.objects.create(user=user)
            for ticket in tickets_data:
                Ticket.objects.create(order=order, **ticket)
            return order
