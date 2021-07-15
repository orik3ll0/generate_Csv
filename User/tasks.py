from __future__ import absolute_import, unicode_literals
from faker import Faker
from celery import shared_task
from datetime import datetime
from User.models import Generated_csv
import time
import csv
import random
import os.path


@shared_task
def create_task(dict, separator, stringCharacter, row, row_id):
    fake = Faker('en_US')

    list_of_headers = []
    for key in dict:
        list_of_headers.append(dict[key]['columnName'])

    filename = f'{time.mktime(datetime.now().timetuple())}{row}.csv'        #creating file name

    with open(f'static/files/{filename}', 'wt') as csvFile:
        writer = csv.DictWriter(csvFile, delimiter=separator, quotechar=stringCharacter, quoting=csv.QUOTE_ALL, fieldnames=list_of_headers)
        writer.writeheader()

        for i in range(int(row)):

            dict_for_writerow = {}

            for key in dict:
                if dict[key]['type'] == 1:
                    dict_for_writerow.update({dict[key]['columnName']: fake.name()})
                elif dict[key]['type'] == 2:
                    dict_for_writerow.update({dict[key]['columnName']: fake.job()})
                elif dict[key]['type'] == 3:
                    dict_for_writerow.update({dict[key]['columnName']: fake.email()})
                elif dict[key]['type'] == 4:
                    dict_for_writerow.update({dict[key]['columnName']: fake.domain_name()})
                elif dict[key]['type'] == 5:
                    dict_for_writerow.update({dict[key]['columnName']: fake.phone_number()})
                elif dict[key]['type'] == 6:
                    dict_for_writerow.update({dict[key]['columnName']: fake.company()})
                elif dict[key]['type'] == 7:
                    sentences = [fake.sentence() for i in range(dict[key]['sentence'])]
                    sen_new = ' '.join([str(cimi) for cimi in sentences])
                    dict_for_writerow.update({dict[key]['columnName']: sen_new})
                elif dict[key]['type'] == 8:
                    dict_for_writerow.update(
                        {dict[key]['columnName']: random.randint(dict[key]['from_int'], dict[key]['to_int'])})
                elif dict[key]['type'] == 9:
                    dict_for_writerow.update({dict[key]['columnName']: fake.address()})
                elif dict[key]['type'] == 10:
                    dict_for_writerow.update({dict[key]['columnName']: fake.date()})

            writer.writerow(dict_for_writerow)

    if(os.path.isfile(f'static/files/{filename}')):
        Generated_csv.objects.filter(id=row_id).update(path=filename, status="Ready")

        return True
    else:
        Generated_csv.objects.filter(id=row_id).update(status="Failure")

        return False


