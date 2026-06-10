from django.shortcuts import render
from rest_framework import viewsets

from airport.models import Flight, Airplane, Airport, Route, Crew, Order, Ticket
from airport.serializers import FlightListSerializer, AirplaneListSerializer, AirportSerializer, \
    RouteSerializer, CrewSerializer, OrderSerializer, TicketSerializer, AirplaneDetailSerializer, \
    AirplaneCreateSerializer, RouteCreateSerializer, FlightDetailSerializer, FlightCreateSerializer, \
    OrderDetailSerializer, OrderCreateSerializer


class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneListSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return AirplaneDetailSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return AirplaneCreateSerializer

        return self.serializer_class

class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer

class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return RouteCreateSerializer

        return self.serializer_class

class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer

class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all().select_related('airplane', 'route', 'route__source', 'route__destination').prefetch_related('crew', 'tickets')
    serializer_class = FlightListSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return FlightDetailSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return FlightCreateSerializer

        return FlightListSerializer

class OrderViewset(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return OrderDetailSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return OrderCreateSerializer
        return OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
