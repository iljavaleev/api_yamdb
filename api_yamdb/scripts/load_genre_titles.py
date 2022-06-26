import csv
# python3 manage.py runscript scripts.{file_name}
from actions.models import Genre, Title, GenreTitle


def run():
    fhand = open('static/data/genre_title.csv')
    reader = csv.reader(fhand)
    next(reader)

    for row in reader:
        print(row)
        genre, created = Genre.objects.get_or_create(id=row[2])
        title, created = Title.objects.get_or_create(id=row[1])
        genre_title = GenreTitle(
            id=row[0],
            title_id=title.id,
            genre_id=genre.id,
        )
        genre_title.save()
