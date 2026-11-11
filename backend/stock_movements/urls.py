from rest_framework.routers import DefaultRouter
from .views import StockMovementViewSet

router = DefaultRouter()

router.register(
    prefix="stock-movements",
    viewset=StockMovementViewSet,
    basename="stock-movement"
)

urlpatterns = router.urls