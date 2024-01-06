from django.contrib import admin
from .models import BankingStatus_Model

# Register your models here.
admin.site.register(BankingStatus_Model)


# After that, we'll have to run some commands in the terminal.
# python manage.py makemigrations
# python manage.py migrate
# python manage.py shell
# from banking_status_app.models import BankingStatus_Model
# BankingStatus_Model.objects.create()

"""
So the story is, we've created a new BankingStatus app, created a model, registered into the database, and then created
a single row instance of the BankingStatus model.

For this instance creation, we didn't used any forms.py/views.py/urls.py or any template. Rather we've used some terminal
commands.

At can also be created from the admin panel.
"""
