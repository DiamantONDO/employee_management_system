from rest_framework.routers import DefaultRouter
from apps.attendance.views import AttendanceViewSet

#trailing_slash=True
router = DefaultRouter()
router.register(r'attendances', AttendanceViewSet, basename='attendance')
urlpatterns = router.urls

router.include_format_suffixes = False