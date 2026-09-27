from django.urls import path
from .views import add_numbers, get_all_tasks, get_task_by_id, create_task

# urlpatterns is a list of paths that the server will listen to
urlpatterns = [
    path("add-numbers/", add_numbers),
    path("get-all-tasks/", get_all_tasks),
    # The <int:id> is a path parameter, it is used to get the id from the URL
    path("get-task-by-id/<int:id>/", get_task_by_id),
    path("create-task/", create_task),
]
