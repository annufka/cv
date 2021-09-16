from django.contrib import admin

from app.account.models import ColumnSchema, Schema, DataSet


class ColumnSchemaInLine(admin.StackedInline):
    model = ColumnSchema

@admin.register(Schema)
class SchemaAdmin(admin.ModelAdmin):
    inlines = [ColumnSchemaInLine,]
    list_display = ['name', 'modified_date']

@admin.register(DataSet)
class DataSetAdmin(admin.ModelAdmin):
    list_display = ['create_date', ]
