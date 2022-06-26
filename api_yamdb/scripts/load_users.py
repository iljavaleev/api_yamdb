from django.contrib.auth import get_user_model
# python3 manage.py runscript scripts.{file_name}
import csv

User = get_user_model()


def run():
    fhand = open('static/data/users.csv')
    reader = csv.reader(fhand)
    next(reader)

    for row in reader:
        print(row)
        user, created = User.objects.get_or_create(
            id=row[0],
            username=row[1],
            email=row[2],
            role=row[3],
            bio=row[4],
            first_name=row[5],
            last_name=row[6],
        )
        user.save()
