import csv

from actions.models import Genre


def run():
    fhand = open('static/data/genre.csv')
    reader = csv.reader(fhand)
    next(reader)

    Genre.objects.all().delete()

    for row in reader:
        print(row)
        genre = Genre(
            id=row[0],
            name=row[1],
            slug=row[2],
            )
        genre.save()
