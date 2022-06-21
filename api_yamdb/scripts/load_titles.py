import csv
from api.models import Category, Title
# python3 manage.py runscript scripts.{file_name}


def run():
    fhand = open('static/data/titles.csv')
    reader = csv.reader(fhand)
    next(reader)

    Title.objects.all().delete()

    for row in reader:
        print(row)
        category, created = Category.objects.get_or_create(id=row[3])
        title = Title(id=row[0], name=row[1], year=row[2], category=category)
        title.save()
