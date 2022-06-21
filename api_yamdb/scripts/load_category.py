import csv
from api.models import Category
# python3 manage.py runscript scripts.{file_name}


def run():
    fhand = open('static/data/category.csv')
    reader = csv.reader(fhand)
    next(reader)

    Category.objects.all().delete()

    for row in reader:
        print(row)
        category = Category(id=row[0], name=row[1], slug=row[2])
        category.save()
