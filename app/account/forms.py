from django import forms
from django.forms import inlineformset_factory

from app.account.models import Schema, ColumnSchema


class SchemeForm(forms.ModelForm):
    class Meta:
        model = Schema
        fields = ('name', 'column_separator', 'string_character',)


# class SchemeRowForm(forms.ModelForm):
#
#     class Meta:
#         model = ColumnSchema
#         fields = ('schema', 'column_name', 'type_of_data', 'order', )

RowFormSet = inlineformset_factory(Schema, ColumnSchema, fields=('column_name', 'type_of_data', 'order'), extra=1,
                                   can_delete=True)
