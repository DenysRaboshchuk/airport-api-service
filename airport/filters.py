import django_filters
from django.db.models import ExpressionWrapper, F, IntegerField

from airport.models import Flight, Airplane, Airport, Route, Order


class FlightFilter(django_filters.FilterSet):
    class Meta:
        model = Flight
        fields = {
            "route__source": ["exact"],
            "route__destination": ["exact"],
            "departure_time": ["date"],
        }


class AirplaneFilter(django_filters.FilterSet):
    amount_of_seats_gte = django_filters.NumberFilter(
        method="filter_amount_of_seats_gte",
    )
    amount_of_seats_lte = django_filters.NumberFilter(
        method="filter_amount_of_seats_lte",
    )

    class Meta:
        model = Airplane
        fields = {"name": ["icontains"], "airplane_type__name": ["icontains"]}

    def get_annotated_queryset(self, queryset):
        return queryset.annotate(
            amount_of_seats=ExpressionWrapper(
                F("rows") * F("seats_in_row"), output_field=IntegerField()
            )
        )

    def filter_amount_of_seats_gte(self, queryset, name, value):
        return self.get_annotated_queryset(queryset).filter(amount_of_seats__gte=value)

    def filter_amount_of_seats_lte(self, queryset, name, value):
        return self.get_annotated_queryset(queryset).filter(amount_of_seats__lte=value)


class AirportFilter(django_filters.FilterSet):
    class Meta:
        model = Airport
        fields = {"name": ["icontains"], "closest_big_city": ["icontains"]}
