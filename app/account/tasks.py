from celery import shared_task
import csv
import datetime
import random
import string

from app.account.models import DataSet, ColumnSchema


@shared_task

def generate_csv(set_id, number):
    data_set = DataSet.objects.get(pk=set_id)
    column = ColumnSchema.objects.filter(schema_id=data_set.schema.pk).order_by("order")
    column_sep = data_set.schema.column_separator
    # честно было лень переделывать модель, возможно, я тут вообще все неправильно трактовала. Поэтому тут много условий
    if column_sep == "comma":
        column_symb = ","
    elif column_sep == "semicolon":
        column_symb = ";"
    else:
        column_symb = "-"
    head_of_table = []
    type_of_data = []
    for item in column:
        head_of_table.append(item.column_name)
        type_of_data.append(item.type_of_data)
    with open('media/' + data_set.schema.name + '.csv', 'w+') as f:
        file_writer = csv.writer(f, delimiter=column_symb, lineterminator="\r")
        file_writer.writerow(head_of_table)
        for i in range(int(number)):
            row = []
            for j in type_of_data:
                if j == 'email':
                    mail = ''.join(random.choice(string.ascii_letters) for _ in range(8))
                    email = mail + "@gmail.com"
                    row.append(email)
                elif j == 'phone':
                    phone = ''.join(str(random.randint(0,9)) for _ in range(7))
                    row.append(phone)
                elif j =='company':
                    # from random_word import RandomWords
                    # r = RandomWords()
                    # row.append(r.get_random_word())
                    word = ''.join(random.choice(string.ascii_letters) for _ in range(8))
                    row.append(word)
                elif j == 'address':
                    from faker import Faker
                    fake = Faker()
                    row.append(fake.address())
                elif j == 'date':
                    timestamp = ''.join(str(random.randint(0,9)) for _ in range(10))
                    row.append(datetime.datetime.fromtimestamp(int(timestamp)))