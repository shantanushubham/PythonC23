from typing import override
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ViewSet

from tasks.serializers import TaskSerializer
from .models import Task

# views.py is the file that contains the views for the tasks app.
# A view is a function that returns a response to a request.

# Create your views here.

# A view function that adds two numbers
# The view function takes a request object as an argument

@api_view(["GET"])
# localhost:8000/api/add-numbers/
def add_numbers(request):
    # Get the query parameters from the request
    try:
        a = float(request.query_params["a"])
        b = float(request.query_params["b"])
        # Add the numbers
        result = a + b
        # Returns a response object
        return Response({"sum": result})  # Creating a response object
    except:
        return Response(
            {"error": "Invalid numbers"}, status=status.HTTP_400_BAD_REQUEST
        )


# ******** TASKS - FILE READING ********

class TaskViewSet(ModelViewSet):

    queryset = Task.objects.all() # SELECT * FROM tasks WHERE completed = false;
    serializer_class = TaskSerializer

    @action(detail=False, methods=["GET"], url_path="completed")
    # detail=False means that the action is not associated with a specific task.
    # detail=True means that the action is associated with a specific task.
    def get_only_completed_tasks(self, request):
        tasks = Task.objects.filter(completed=True)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["GET"], url_path="specific")
    def get_a_specific_task(self, request, pk=None):
        task = Task.objects.get(id=pk)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

# class TaskViewSet(ViewSet):

#     # queryset = Task.objects.all()
#     # # queryset is basically the DB query that will be executed to get the data on top of which any operation will happen.
#     # serializer_class = TaskSerializer
#     # serializer_class is the serializer that will be used to serialize the data.

#     @override
#     def list(self, request): # GET request to get all tasks
#         tasks = Task.objects.all()
#         serializer = TaskSerializer(tasks, many=True) # many=True is used because we are serializing multiple tasks.
#         return Response(serializer.data)


#     @override
#     def retrieve(self, request, pk=None): # GET request to get a task by id && pk = primary key (id)
#         try:
#             task = Task.objects.get(id=pk)
#             serializer = TaskSerializer(task)
#             return Response(serializer.data)
#         except Task.DoesNotExist:
#             return Response(
#                 {"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND
#             )

#     @override
#     def create(self, request): # POST request to create a new task
#         serializer = TaskSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     @override
#     def update(self, request, pk=None): # PUT request to update a task
#         try:
#             task = Task.objects.get(id=pk)
#             serializer = TaskSerializer(task, data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#         except Task.DoesNotExist:
#             return Response(
#                 {"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND
#             )
        
#     @override
#     def destroy(self, request, pk=None): # DELETE request to delete a task
#         try:
#             task = Task.objects.get(id=pk)
#             task.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         except Task.DoesNotExist:
#             return Response(
#                 {"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND
#             )

#     @override
#     def partial_update(self, request, pk=None): # PATCH request to update a task partially
#         try:
#             task = Task.objects.get(id=pk)
#             serializer = TaskSerializer(task, data=request.data, partial=True)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#         except Task.DoesNotExist:
#             return Response(
#                 {"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND
#             )