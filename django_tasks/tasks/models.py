from django.db import models

# Models are the way to define the structure of the data, which will be used as a standard/blueprint for the data.
# In Django, models are classes that inherit from the models.Model class.

# In Generalised Backend Development, a model may or may not be associated with a database.
# In Generalised Backend Development, if a class is associated with a database table, it is called an entity.
# Thus, a model may or may not be an entity.

# However, in Django, a model is always associated with a database. Thus, every model is an entity.

# Create your models here.


class Task(models.Model):

    # id is automatically created by Django as the primary key.
    # id is integer and is auto-incremented.
    title = models.CharField(max_length=200)  # VARCHAR(200) in SQL
    description = models.TextField()  # TEXT in SQL
    completed = models.BooleanField(default=False)  # BOOLEAN in SQL
    created_at = models.DateTimeField(auto_now_add=True)  # TIMESTAMP in SQL
    updated_at = models.DateTimeField(auto_now=True)  # TIMESTAMP in SQL

    """
        auto_now_add: Automatically set the field to the current date and time when the object is created.
        auto_now: Automatically set the field to the current date and time when the object is saved.

        CREATE TABLE tasks (
            id SERIAL PRIMARY KEY,
            title VARCHAR(200) NOT NULL,
            description TEXT NOT NULL,
            completed BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """
