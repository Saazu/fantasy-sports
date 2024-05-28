from rest_framework import routers
from .views import UserViewset, ProfileViewset, TotalWinningsViewset

router = routers.DefaultRouter()
router.register("profile", ProfileViewset, basename="profile")
router.register("total_winnings", TotalWinningsViewset, basename="total_winnings")

urlpatterns = router.urls
