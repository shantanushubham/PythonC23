from django_filters import CharFilter, FilterSet
from .models import Task

# class TaskFilter(FilterSet):

#     title = CharFilter(field_name="title", lookup_expr="icontains")
#     description = CharFilter(field_name="description", lookup_expr="icontains")

#     class Meta:
#         model = Task
#         fields = ["title", "description", "completed"]

    # SELECT * FROM tasks_task WHERE title ILIKE '%django%' AND description ILIKE '%milk%' AND completed = true;


# class TaskFilter(FilterSet):

#     class Meta:
#         model = Task
#         fields = {
#             "completed": ["exact"],
#             "title": ["icontains"],
#             "description": ["icontains"],
#             "user": ["exact"],
#         }
