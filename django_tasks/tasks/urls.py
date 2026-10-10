from django.urls import path, include
from .views import add_numbers, TaskViewSet
from rest_framework.routers import DefaultRouter

# urlpatterns is a list of paths that the server will listen to

router = DefaultRouter()
router.register(r"task", TaskViewSet, basename="task")
# basename is used to avoid conflicts with other views.

urlpatterns = [
    path("add-numbers/", add_numbers), 
    path("", include(router.urls)),
]
