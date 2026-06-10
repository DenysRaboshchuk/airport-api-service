from rest_framework.routers import DefaultRouter

from airport.views import AirplaneViewSet, AirportViewSet, RouteViewSet, CrewViewSet, \
    FlightViewSet, OrderViewset

router = DefaultRouter()
router.register(r"airplane", AirplaneViewSet)
router.register(r"airport", AirportViewSet)
router.register(r"route", RouteViewSet)
router.register(r"crew", CrewViewSet)
router.register(r"flights", FlightViewSet)
router.register(r"orders", OrderViewset)


app_name = "airport"
urlpatterns = router.urls
