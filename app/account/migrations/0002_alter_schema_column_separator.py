# Generated by Django 3.2.7 on 2021-09-15 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schema',
            name='column_separator',
            field=models.CharField(choices=[(',', 'Comma (,)'), (';', 'Semicolon(;)'), ('-', 'Dash(-)')], default='comma', max_length=10),
        ),
    ]