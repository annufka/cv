from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import post_save


class Schema(models.Model):
    COLUMN_SEPARATOR_CHOICES = (
        ('comma', 'Comma (,)'),
        ('semicolon', 'Semicolon(;)'),
        ('dash', 'Dash(-)')
    )
    STRING_CHARACTER_CHOICES = (
        ('double', 'Double-quote(")'),
        ("single", "Single-quote(')")
    )
    name = models.CharField(max_length=250)
    column_separator = models.CharField(max_length=10, choices=COLUMN_SEPARATOR_CHOICES, default="comma")
    string_character = models.CharField(max_length=10, choices=STRING_CHARACTER_CHOICES, default="double")
    modified_date = models.DateTimeField(auto_now=True)


class ColumnSchema(models.Model):
    TYPE_CHOICES = (
        ('email', 'Email'),
        ('phone', 'Phone number'),
        ('company', 'Company name'),
        ('address', 'Address'),
        ('date', 'Date')
    )
    # хотелось бы с range сделать, но что-то не выходит
    schema = models.ForeignKey(Schema, on_delete=models.CASCADE)
    column_name = models.CharField(max_length=250)
    type_of_data = models.CharField(max_length=10, choices=TYPE_CHOICES)
    order = models.PositiveIntegerField()

class DataSet(models.Model):
    # STATUS_CHOICE = (('nothing', 'Nothing'),
    #                  ('progress', 'In progress'),
    #                  ('ready', 'Ready')
    #                  )
    schema = models.ForeignKey(Schema, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    path_to_file = models.FilePathField(path='media', null=True, blank=True)
    # status = models.CharField(max_length=10, choices=STATUS_CHOICE, default="nothing")

@receiver(post_save, sender=Schema)
def create_data_set(sender, instance, created, **kwargs):
    if created:
        DataSet.objects.create(schema=instance)