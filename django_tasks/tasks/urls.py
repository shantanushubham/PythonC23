from django.urls import path, include
from .views import add_numbers, TaskViewSet, UserViewSet
from rest_framework.routers import DefaultRouter

# urlpatterns is a list of paths that the server will listen to

router = DefaultRouter()
router.register(r"task", TaskViewSet, basename="task")
router.register(r"user", UserViewSet, basename="user")
# basename is used to avoid conflicts with other views.

urlpatterns = [
    path("add-numbers/", add_numbers),
    # path("tasks-with-filter/", get_tasks_with_filter), 
    path("", include(router.urls)),
]
