from django.urls import path
from .views import add_numbers, TaskView

# urlpatterns is a list of paths that the server will listen to
urlpatterns = [
    path("add-numbers/", add_numbers), 
    path("task/", TaskView.as_view()),
    path("task/<int:id>/", TaskView.as_view()), # The <int:id> is a path parameter, it is used to get the id from the URL
]
