from typing import override
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
import json

from rest_framework.views import APIView

# views.py is the file that contains the views for the tasks app.
# A view is a function that returns a response to a request.

# Create your views here.

# A view function that adds two numbers
# The view function takes a request object as an argument

TASK_FILE_PATH = "tasks/files/tasks.json"


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
class TaskView(APIView):

    def __get_all_tasks(self):
        with open(TASK_FILE_PATH, "r") as file:
            return json.loads(file.read())  # Returns a list of tasks

    # GET request to get a task by id
    @override  # This is just a convention to override the method. It doesn't do anything.
    def get(self, request, id=None):
        # Read the tasks.json file
        tasks = self.__get_all_tasks()
        if id is None:
            return Response(tasks)
        # Find the task with the given id
        for task in tasks:
            if task["id"] == id:
                return Response(task)
        return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

    # POST request to create a new task
    @override  # This is just a convention to override the method. It doesn't do anything.
    def post(self, request):  # Cannot change the name of the method
        # Get the data from the request
        data = request.data
        # Read the tasks.json file
        tasks = self.__get_all_tasks()
        # Create a new task
        task = {
            "id": len(tasks) + 1,
            "title": data["title"],
            "description": data["description"],
            "completed": False,
        }
        # Add the task to the tasks.json file
        with open(TASK_FILE_PATH, "w") as file:
            tasks.append(task)
            json.dump(tasks, file, indent=2)

        return Response(task, status=status.HTTP_201_CREATED)

    # PUT request to update a task
    @override  # This is just a convention to override the method. It doesn't do anything.
    def put(self, request, id):
        # Get the data from the request body
        data = request.data
        # Read the tasks.json file
        tasks = self.__get_all_tasks()
        # Find the task with the given id
        for task in tasks:
            if task["id"] == id:
                task["title"] = data["title"]
                task["description"] = data["description"]
                task["completed"] = data["completed"]
                # Save the tasks.json file
                with open(TASK_FILE_PATH, "w") as file:
                    json.dump(tasks, file, indent=2)
                return Response(task)
        return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

    # DELETE request to delete a task
    @override  # This is just a convention to override the method. It doesn't do anything.
    def delete(self, request, id):
        # Read the tasks.json file
        tasks = self.__get_all_tasks()
        # Find the task with the given id
        for task in tasks:
            if task["id"] == id:
                tasks.remove(task)
                # Save the tasks.json file
                with open(TASK_FILE_PATH, "w") as file:
                    json.dump(tasks, file, indent=2)
                return Response(
                    {"message": "Task deleted successfully"}, status=status.HTTP_200_OK
                )
        return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
