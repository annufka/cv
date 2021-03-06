# Generated by Django 3.2.7 on 2021-09-15 18:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Schema',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('column_separator', models.CharField(choices=[('comma', 'Comma (,)'), ('semicolon', 'Semicolon(;)'), ('dash', 'Dash(-)')], default='comma', max_length=10)),
                ('string_character', models.CharField(choices=[('double', 'Double-quote(")'), ('single', "Single-quote(')")], default='double', max_length=10)),
                ('modified_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='DataSet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('path_to_file', models.FilePathField(blank=True, null=True, path='media')),
                ('status', models.CharField(choices=[('nothing', 'Nothing'), ('progress', 'In progress'), ('ready', 'Ready')], default='nothing', max_length=10)),
                ('schema', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.schema')),
            ],
        ),
        migrations.CreateModel(
            name='ColumnSchema',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('column_name', models.CharField(max_length=250)),
                ('type_of_data', models.CharField(choices=[('email', 'Email'), ('phone', 'Phone number'), ('company', 'Company name'), ('address', 'Address'), ('date', 'Date')], max_length=10)),
                ('order', models.PositiveIntegerField()),
                ('schema', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.schema')),
            ],
        ),
    ]
