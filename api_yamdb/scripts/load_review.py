from django.contrib.auth import get_user_model
# python3 manage.py runscript name
import csv

from api.models import Comment, Title
from api.exceptions import UserNotFoundError

User = get_user_model()


def run():
    fhand = open('static/data/comments.csv')
    reader = csv.reader(fhand)
    next(reader)

    Comments.objects.all().delete()

    for row in reader:
        print(row)
        t, created = Title.objects.get_or_create(name=row[1])
        try:
            author = User.objects.get(id=[3])
        except Exception as ex:
            raise UserNotFoundError

        review = Review(
            id=row[0],
            title_id=t,
            text=row[2],
            author=author,
            score=row[4],
            pub_date=row[5]
            )
        review.save()
