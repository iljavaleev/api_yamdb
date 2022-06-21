from django.contrib.auth import get_user_model
# python3 manage.py runscript name
import csv

from api.models import Comment, Review
from api.exceptions import UserNotFoundError

User = get_user_model()


def run():
    fhand = open('static/data/comments.csv')
    reader = csv.reader(fhand)
    next(reader)

    Comments.objects.all().delete()

    for row in reader:
        print(row)
        r, created = Review.objects.get_or_create(name=row[1])
        try:
            author = User.objects.get(id=[3])
        except Exception as ex:
            raise UserNotFoundError

        c = Comment(id=row[0],
                    review_id=r,
                    text=row[2],
                    author=author,
                    pub_date=row[4]
                    )
        c.save()
